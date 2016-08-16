"""
This module is responsible for reading settings files and storing provenance.

It copies the pattern (and code) from the logging module so that
each client Python module can have a local settings object.
"""
import collections
import json
import logging

__all__ = [ "get_parameters", "namespace_settings", "read_json" ]

__author__ = "Andrew Dolgert <adolgert@uw.edu>"
__status__ = "development"

logger = logging.getLogger("provda")

# Parameters behave like loggers in that there is a root
# and sub-parameter sets, delineated by a period-separated
# hierarchical value, which would be a module name.

class NoSuchParameter(Exception):
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
    def __init__(self, aparameters):
        self.parameters_map = { aparameters : None }

    def append(self, aparameters):
        if aparameters not in self.parameters_map:
            self.parameters_map[aparameters] = None


class Manager(object):
    def __init__(self, rootnode):
        self.root = rootnode
        self.parameters_dict = dict()

    def get_parameters(self, name):
        parameters_instance = None
        if not isinstance(name, basestring):
            raise TypeError("A parameters name must be string or unicode")
        if isinstance(name, unicode):
            name = name.encode("utf-8")
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
        finally:
            _releaseLock()
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



class Parameters(collections.Mapping):
    """
    Records which parameters are actually used.

    Inherits from the abstract base class for read-only dictionaries, Mapping.
    """
    def __init__(self, name):
        self.name = name
        self.parent = None
        self._items = dict()

    def update(self, settings_dict):
        self._items.update(settings_dict)

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
        if name in self._items:
            return self._items[name]
        elif self.parent is not None:
            return self.parent[name]
        else:
            raise KeyError(name)

    def __iter__(self):
        """
        Mapping interface
        :return:
        """
        return iter(self._items)


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
    def __init__(self):
        Parameters.__init__(self, "root")


root = RootParameters()
Parameters.root = root
Parameters.manager = Manager(Parameters.root)


def get_parameters(name=None):
    if name:
        return Parameters.manager.get_parameters(name)
    else:
        return root

def input_file(template_string, **kw_replacements):
    return template_string.format(**kw_replacements)


def input_database_table(template_string, **kw_replacements):
    # You open a schema, not a set of tables. How to do this?
    # retrieve passwords
    return template_string.format(**kw_replacements)


def output_file(template_string, **kw_replacements):
    return template_string.format(**kw_replacements)


def output_database_table(template_string, **kw_replacements):
    # retrieve passwords
    return template_string.format(**kw_replacements)


## Working with argparse.ArgumentParser

def add_arguments(parser):
    parser.add_argument("--verbose", "-v", action="count")
    parser.add_argument("--quiet", "-q", action="count")
    parser.add_argument("--settings", action="append")

    parser_group=parser.add_argument_group("settings")
    # These map from the name to the default value.
    qualified_parameters = dict()
    unqualified_parameters = dict()
    nonunique = set()

    for qualify, parameters in Parameters.manager.parameters_dict.items():
        if isinstance(parameters, Parameters):
            for name, value in parameters.items():
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
        elif isinstance(default, basestring):
            parser_group.add_argument("--{}".format(flag), type=str)
        elif isinstance(default, bool):
            parser_group.add_argument("--{}".format(flag), type=bool)
        elif isinstance(default, collections.Iterable):
            pass
        elif isinstance(default, collections.Mapping):
            pass
        else:
            logger.warn("Not sure what type {} is.".format(default))


def namespace_settings(args):
    logger.debug("settings sent to provda {}".format(args))
    level = logging.INFO
    if "settings" in args.__dict__:
        if isinstance(args.settings, basestring):
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
        if flag == "q":
            level = max(0, logging.WARNING + 5 * (args.q - 1))
        elif flag == "v":
            level = max(0, logging.DEBUG - 5 * (args.v + 1))

        elif flag == "settings":
            continue # already handled

        elif value is None:
            continue

        elif "." in flag:
            split = flag.split(".")
            parameters_name=".".join(split[:-1])
            Parameters.manager.get_parameters(parameters_name)[split[-1]]=value

        else:
            unset = True
            for q, parameters in Parameters.manager.parameters_dict.items():
                if isinstance(parameters, Parameters):
                    if flag in parameters:
                        parameters.update({flag : value})
                        unset = False
                else:
                    pass # no parameters in PlaceHolder
            if unset:
                pass # Can we check whether this was a user-specified param?

    logging.basicConfig(level=level)


## Loading settings
def read_json(stream):
    per_module_settings=json.load(stream)
    logger.debug(per_module_settings)
    for (namespace, settings) in per_module_settings.items():
        get_parameters(namespace).update(settings)


## Threading to protect global hierarchy of parameters.

def _acquireLock():
    pass

def _releaseLock():
    pass