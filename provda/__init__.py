"""
This module is responsible for reading settings files and storing provenance.

It copies the pattern (and code) from the logging module so that
each client Python module can have a local settings object.
"""
import collections
import logging
import parameters

__all__ = [ "get_parameters", "namespace_settings", "read_json" ]

__author__ = "Andrew Dolgert <adolgert@uw.edu>"
__status__ = "development"

logger = logging.getLogger("provda")

# These are forwards to the parameters module.
def get_parameters(name=None, default_dict=None):
    parameters.get_parameters(name, default_dict)

def add_arguments(parser):
    parameters.add_arguments(parser)

def namespace_settings(args):
    parameters.namespace_settings(args)

def read_json(stream):
    parameters.read_json(stream)

def read(file_or_stream):
    parameters.read(file_or_stream)



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
    parser.add_argument("--verbose", "-v", action="count")
    parser.add_argument("--quiet", "-q", action="count")

    parameters.add_arguments(parser)



def namespace_settings(args):
    """
    Sets settings from an argparse specification.

    :param args: A Namespace object from argparse.parse_args.
    :return:
    """
    logger.debug("settings sent to provda {}".format(args))
    parameters.namespace_settings(args)
    level = logging.INFO

    for flag, value in args.__dict__.items():
        if flag == "q":
            level = max(0, logging.WARNING + 5 * (args.q - 1))
        elif flag == "v":
            level = max(0, logging.DEBUG - 5 * (args.v + 1))

        elif flag == "settings":
            continue # already handled

        elif value is None:
            continue

        else:
            pass # Can we check whether this was a user-specified param?



def config_logging(args):
    """
    This reads the command line arguments, looks at settings files, and sets
    logging.

    It does a per-module logging settings using the untracked "loglevel"
    parameter. Then it takes the -v  or -q from the command line
    and sets an overall debug level.

    :param args: This is a Namespace object returned by argparse.parse_args().
    """
    param_modules = parameters.Parameters.manager.parameters_dict
    for qualified, params in param_modules.items():
        if not isinstance(params, parameters.PlaceHolder):
            if "loglevel" in params:
                set_level = params["loglevel"]
                if isinstance(set_level, basestring):
                    int_level = getattr(logging, set_level.upper())
                elif isinstance(set_level, int):
                    int_level = set_level
                else:
                    raise Exception("Cannot interpret logging level {}".format(
                        params["loglevel"]))

                logging.getLogger(qualified).setLevel(int_level)
            else:
                pass # OK, so they don't set their log level. Inherited
        else:
            pass # PlaceHolder has nothing for us.

    if hasattr(args, "quiet") and args.quiet is not None:
        level = min(logging.CRITICAL, logging.WARNING + 5 * (args.quiet - 1))
    elif hasattr(args, "verbose") and args.verbose is not None:
        # level 0 is off, so 1 is the maximum.
        level = max(1, logging.DEBUG - 5 * (args.verbose - 1))
        print("level is {} args {}".format(level, args.verbose))
    else:
        level = logging.INFO
    print("No level happened")

    sh = logging.StreamHandler()
    sh.setLevel(level)
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    sh.setFormatter(formatter)
    logging.getLogger().addHandler(sh)



## Loading settings

def add_provenance(filename, additional=None):
    """
    This adds provenance information to a file.
    :param filename:
        This function opens this file and closes it. That's not good
        to do if the file is being modified by another command.
    :param additional: A Mapping object (dict) of key-value pairs.
    :return: None
    """
    pass # RFC 3339 for the dates.
