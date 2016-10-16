"""
Wraps modules in order to call logging methods for provenance.
Must be loaded after the modules it wraps. Chose this order because
numpy will always be loaded before a random package like provda.
Could add a loader, as in recipy, to hook things that are loaded after.
"""
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import logging
import sys
import wrapt
from . import logprov  # This hooks logging, so it only looks unused.


logger = logging.getLogger("provda.patch")


@wrapt.decorator
def report_write(wrapped, instance, args, kwargs):
    logger.write_file(args[0], "unknown")
    return wrapped(*args, **kwargs)


@wrapt.decorator
def report_read(wrapped, instance, args, kwargs):
    logger.read_file(args[0], "unknown")
    return wrapped(*args, **kwargs)


WRAPS0 = {
    "pandas": {
        "in": [
            "read_csv", "read_table", "read_excel", "read_hdf",
            "read_pickle", "read_stata", "read_msgpack"
        ],
        "out": [
            'DataFrame.to_csv', 'DataFrame.to_excel', 'DataFrame.to_hdf',
            'DataFrame.to_msgpack', 'DataFrame.to_stata',
            'DataFrame.to_pickle', 'Panel.to_excel', 'Panel.to_hdf',
            'Panel.to_msgpack', 'Panel.to_pickle',
            'Series.to_csv', 'Series.to_hdf',
            'Series.to_msgpack', 'Series.to_pickle'
        ]
    },
    "matplotlib.pyplot": {
        "in": [],
        "out": [
            "savefig"
        ]
    },
    "numpy": {
        "in": [
            'genfromtxt', 'loadtxt', 'fromfile'
        ],
        "out": [
            'save', 'savez', 'savez_compressed', 'savetxt'
        ]
    }
}


def wrap_modules():
    for module_name, in_out in WRAPS0.items():
        if module_name in sys.modules:
            module = sys.modules[module_name]
            if not hasattr(module, "_provda_patch"):
                for in_f in in_out["in"]:
                    setattr(module, in_f, report_read(getattr(module, in_f)))
                for o_f in in_out["out"]:
                    setattr(module, o_f, report_write(getattr(module, o_f)))
                module._provda_patch = True


wrap_modules()


def open(*args, **kwargs):
    """All good ideas from https://github.com/recipy:
    Use this as provda.patch.open(file, mode="blah").
    We don't want to hook open because lots of other modules use it.
    """
    if "mode" in kwargs:
        mode = kwargs["mode"]
    elif len(args) > 1:
        mode = args[1]
    else:
        mode = "r"

    if "r" in mode:
        logger.read_file(args[0], "unknown")
    if {"w", "x", "a", "+"} & set(mode):
        logger.write_file(args[0], "unknown")

    return builtins.open(*args, **kwargs)
