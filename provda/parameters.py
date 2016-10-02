"""
This module is responsible for reading settings files and storing provenance.

It copies the pattern (and code) from the logging module so that
each client Python module can have a local settings object.
"""
import collections
import copy
import json
import logging
import os
import yaml
from .datatypes import Setting

__all__ = [ "get_parameters", "namespace_settings", "read_json" ]

__author__ = "Andrew Dolgert <adolgert@uw.edu>"
__status__ = "development"

logger = logging.getLogger("provda.parameters")

# Parameters behave like loggers in that there is a root
# and sub-parameter sets, delineated by a period-separated
# hierarchical value, which would be a module name.

class NoSuchParameter(Exception):
    """
    Someone asked for a Parameter that isn't in the settings file.
    There isn't a NoSuchParameters exception because every time
    you ask for a parameter set it is created.
    """
    def __init__(self, argument_name, message):
        self.argument_name = argument_name
        self.message = message

    def __str__(self):
        if self.argument_name is None:
            format = "{message}"
        else:
            format = "setting name {argument_name}: {message}"
        return format.format(message=self.message,
                             argument_name=self.argument_name)


class PlaceHolder(object):
    """
    A Parameters object is scoped with module.submodule.subsubmodule.name.
    If a Parameters object is created for "name" and the modules
    above don't exist, this PlaceHolder stands in their place.
    """
    def __init__(self, aparameters):
        self.parameters_map = { aparameters : None }

    def append(self, aparameters):
        if aparameters not in self.parameters_map:
            self.parameters_map[aparameters] = None


class Manager(object):
    """
    This is responsible for how Parameters objects fit together.

    It creates and maintains the hierarchy of Parameters objects.
    """
    def __init__(self, rootnode):
        logger.debug("Manager.__init__ enter")
        self.root = rootnode
        self.parameters_dict = dict()

    def get_parameters(self, name, default_dict=None):
        logger.debug("get_parameters {}: {}".format(name,
                                    self.parameters_dict.keys()))
        if not isinstance(name, str):
            raise TypeError("A parameters name must be string or unicode")
        _acquireLock()
        try:
            if name in self.parameters_dict:
                parameters_instance = self.parameters_dict[name]
                if isinstance(parameters_instance, PlaceHolder):
                    place_holder = parameters_instance
                    parameters_instance = Parameters(name)
                    parameters_instance.manager = self
                    self.parameters_dict[name] = parameters_instance
                    self._fixup_children(place_holder, parameters_instance)
                    self._fixup_parents(parameters_instance)
            else:
                parameters_instance = Parameters(name)
                parameters_instance.manager = self
                self.parameters_dict[name] = parameters_instance
                self._fixup_parents(parameters_instance)

            if default_dict is not None:
                parameters_instance.init(default_dict)
            else:
                pass # Nothing to load.
        finally:
            _releaseLock()
        logger.debug("my id {}".format(id(self)))
        logger.debug("get_parameters {}: {}".format(name,
                                            self.parameters_dict.keys()))
        return parameters_instance


    def _fixup_parents(self, aparameters):
        name = aparameters.name
        i = name.rfind(".")
        rv = None
        while (i > 0) and not rv:
            substr = name[:i]
            if substr not in self.parameters_dict:
                self.parameters_dict[substr] = PlaceHolder(aparameters)
            else:
                obj = self.parameters_dict[substr]
                if isinstance(obj, Parameters):
                    rv = obj
                else:
                    assert isinstance(obj, PlaceHolder)
                    obj.append(aparameters)
            i = name.rfind(".", 0, i - 1)
        if not rv:
            rv = self.root
        aparameters.parent = rv


    def _fixup_children(self, ph, aparameters):
        name = aparameters.name
        name_len = len(name)
        for c in ph.parameters_map.keys():
            # The if means ... if not c.parent.name.startswith(nm)
            if c.parent.name[:name_len] != name:
                aparameters.parent = c.parent
                c.parent = aparameters

    def __repr__(self):
        l = list()
        for name, param_obj in self.parameters_dict.items():
            if isinstance(param_obj, PlaceHolder):
                l.append("{}: PlaceHolder".format(name))
            elif param_obj.parent is not None:
                l.append("{}: {}".format(name, param_obj.parent.name))
            else:
                l.append("{}: None".format(name))
        return os.linesep.join(l)



class ChainedParametersIter(object):
    """
    This iterator will
    look in the dictionary of provda.tests.sample,
    then look in the dictionary of provda.tests,
    then provda, each time ignoring entries that
    were in the previous one.
    """
    def __init__(self, parameters):
        self.start = parameters
        self.parameters = parameters
        self.iter = iter(parameters._items)
        self.seen = set()

    def __iter__(self):
        self.parameters = self.start
        self.iter = iter(parameters._items)
        self.seen = set()
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        was_seen = True
        return_value=None
        while was_seen:
            try:
                return_value = next(self.iter)
            except StopIteration:
                self.parameters = self.parameters.parent
                if self.parameters is not None:
                    self.iter = iter(self.parameters._items)
                    return_value = next(self.iter)
                else:
                    raise StopIteration
            was_seen = next in self.seen
        self.seen.add(return_value)
        return return_value



class Parameters(collections.Mapping):
    """
    A Parameters objects is a read-only map from
    parameter names to parameter values.

    It records which parameters are actually used.
    Inherits from the abstract base class for read-only dictionaries, Mapping.
    It can be set at load time using ``load_json`` or
    an ``update()`` method, but it won't let you
    assign a value to a key directly.
    """
    def __init__(self, name):
        self.name = name
        self.parent = None
        self._items = dict()

    def __repr__(self):
        return 'provda.Parameters("{}")'.format(self.name)

    def __str__(self):
        return self.__repr__()

    def init(self, settings_dict):
        self._items.update(settings_dict)

    def update(self, settings_dict):
        logger.debug("parameters.update {}".format(settings_dict))
        for flag, raw_value in settings_dict.items():
            if flag in self._items:
                self._items[flag].set(raw_value)
            else:
                raise KeyError()

    def infile(self, role, *args, **kwargs):
        return self[role].format(*args, **kwargs)

    def outfile(self, role, *args, **kwargs):
        return self[role].format(*args, **kwargs)

    def inoutfile(self, role, *args, **kwargs):
        return self[role].format(*args, **kwargs)

    def __getitem__(self, name):
        """
        Mapping interface
        :param name:
        :return:
        """
        logger.debug("getitem called for {}".format(name))
        if name in self._items:
            retval = self._items[name]
            logger.debug("name {} is type {} and value {}".format(
                name, type(retval), retval
            ))
            if isinstance(retval, Setting):
                rv = retval.get(self)
                if rv is None:
                    raise KeyError(name)
                return copy.copy(rv)
            else:
                return copy.copy(retval)
        elif self.parent is not None:
            return self.parent.__getitem__(name)
        else:
            raise KeyError(name)

    def __iter__(self):
        """
        Mapping interface. Will find values in Parameters
        objects which are above this one in the hierarchy.

        :return: Iterator to dictionary of parameters.
        """
        return ChainedParametersIter(self)


    def __len__(self):
        """
        Mapping interface
        :return:
        """
        return len(self._items)


    def get_child(self, suffix):
        if self.root is not self:
            suffix = ".".join((self.name, suffix))
            return self.manager.get_parameters(suffix)


    # In order to be hashable
    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __eq__(self, other):
        return self.name==other.name

    def __hash__(self):
        return hash(self.name)


class RootParameters(Parameters):
    """
    This special parameters object always exists and is
    named "root".
    """
    def __init__(self):
        Parameters.__init__(self, "root")


root = RootParameters()
Parameters.root = root
Parameters.manager = Manager(Parameters.root)


def get_parameters(name=None, default_dict=None):
    """
    Returns a Parameters object from an implicit hierarchy of them.

    Works like loggers. You ask for provda.tests.sample,
    and it inherits parameters from provda.tests.

    :param name: A unicode or text name with dots to indicate hierarchy.
    :param default_dict: A dictionary of parameters to load.
    :return: A Parameters object, which behaves like a dictionary.
    """
    if name:
        return Parameters.manager.get_parameters(name, default_dict)
    else:
        if default_dict is not None:
            root.update(default_dict)
        return root


## Working with argparse.ArgumentParser

def add_arguments(parser):
    """
    Adds arguments to an argparse.ArgumentParser from settings files.

    Every setting in a settings file that is not a list or dictionary
    is turned into a fully-qualified name as a command-line flag.
    Those which are unique names are also turned into flags without
    any qualification.

    This also adds a --settings flag which can be used to read
    settings files, in order, first to last, all of which are
    applied before the command-line settings, no matter what
    order those appear.

    :param parser: This is an argparse.ArgumentParser.
    :return:
    """
    parser_group=parser.add_argument_group("settings")
    # These map from the name to the default value.
    qualified_parameters = dict()
    unqualified_parameters = dict()
    nonunique = set()

    for qualify, parameters in Parameters.manager.parameters_dict.items():
        if isinstance(parameters, Parameters):
            for name in parameters:
                try:
                    value = parameters[name]
                except KeyError:
                    value = "None"
                qualified_parameters["{}.{}".format(qualify, name)]=value
                if name in unqualified_parameters:
                    nonunique.add(name)
                else:
                    unqualified_parameters[name]=value
        else:
            pass # no parameters in PlaceHolder

    reel_out = collections.OrderedDict()
    reel_out.update({k : qualified_parameters[k]
                     for k in sorted(qualified_parameters)})
    reel_out.update({k : unqualified_parameters[k]
                     for k in sorted(set(unqualified_parameters)-nonunique)})

    for flag, default in reel_out.items():
        if isinstance(default, int):
            parser_group.add_argument("--{}".format(flag), type=int)
        elif isinstance(default, float):
            parser_group.add_argument("--{}".format(flag), type=float)
        elif isinstance(default, str):
            parser_group.add_argument("--{}".format(flag), type=str)
        elif isinstance(default, bool):
            parser_group.add_argument("--{}".format(flag), type=bool)
        elif isinstance(default, collections.Iterable):
            pass
        elif isinstance(default, collections.Mapping):
            pass
        else:
            parser_group.add_argument("--{}".format(flag, type=str))


def namespace_settings(args):
    """
    Sets settings from an argparse specification.

    :param args: A Namespace object from argparse.parse_args.
    :return:
    """
    logger.debug("settings sent to parameters {}".format(args))
    level = logging.INFO
    if "settings" in args.__dict__:
        if isinstance(args.settings, str):
            with open(args.settings, "r") as settings_file:
                read_json(settings_file)
        elif isinstance(args.settings, collections.Iterable):
            for fname in args.settings:
                with open(fname, "r") as settings_file:
                    read_json(settings_file)
        else:
            logger.error("Cannot interpret settings flag {}".format(
                args.settings))

    for flag, value in args.__dict__.items():
        if flag == "settings":
            continue # already handled

        elif value is None:
            continue

        elif "." in flag:
            split = flag.split(".")
            parameters_name=".".join(split[:-1])
            undotted = split[-1]
            logger.debug("Setting {} to {}".format(undotted, value))
            Parameters.manager.get_parameters(parameters_name).update(
                { undotted : value })

        else:
            logger.debug("else flag {} value {}".format(flag, value))
            unset = True
            for q, parameters in Parameters.manager.parameters_dict.items():
                if isinstance(parameters, Parameters):
                    logger.debug("looking for {} in {}".format(flag, q))
                    if flag in parameters._items:
                        logger.debug("Setting {} to {} in {}".format(
                            flag, value, q))
                        parameters.update({flag : value})
                        unset = False
                else:
                    pass # no parameters in PlaceHolder
            if unset:
                pass # Can we check whether this was a user-specified param?



def read(file_or_stream):
    if issubclass(file_or_stream, str):
        filename = file_or_stream
        if filename.endswith(".yml"):
            with open(filename, "r") as yaml_stream:
                read_yaml(yaml_stream)
        else:
            with open(filename, "r") as json_stream:
                read_jsonl(json_stream)
    else:
        read_json(file_or_stream)


## Loading settings
def read_yaml(stream):
    """
    Read a json file which has parameters listed in sections
    and populate the parameters dictionaries from those sections.

    :param stream: A Python stream object, that is, ``f=open(filename, "r").``
    :return: None
    """
    per_module_settings = yaml.load(stream)
    logger.debug(per_module_settings)
    for (namespace, settings) in per_module_settings.items():
        get_parameters(namespace).update(settings)


## Loading settings
def read_json(stream):
    """
    Read a json file which has parameters listed in sections
    and populate the parameters dictionaries from those sections.

    :param stream: A Python stream object, that is, ``f=open(filename, "r").``
    :return: None
    """
    per_module_settings=json.load(stream)
    logger.debug(per_module_settings)
    for (namespace, settings) in per_module_settings.items():
        get_parameters(namespace).update(settings)


## Threading to protect global hierarchy of parameters.

def _acquireLock():
    pass

def _releaseLock():
    pass
