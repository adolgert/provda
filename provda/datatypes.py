"""
These are data types to use when defining parameters.
"""
import __builtin__
import logging

logger = logging.getLogger("provda.datatypes")


class BadParameterType(Exception):
    def __init__(self, target, unmatched):
        self.target = target
        self.unmatched = unmatched


class int(object):
    def __init__(self, value):
        try:
            self.value = __builtin__.int(value)
        except ValueError as e:
            raise BadParameterType("int", value)

class double(object):
    def __init__(self, value):
        try:
            self.value = float(value)
        except ValueError as e:
            raise BadParameterType("float", value)

class string(object):
    def __init__(self, value):
        try:
            self.value = str(value)
        except ValueError as e:
            raise BadParameterType("str", value)

class path_template(object):
    def __init__(self, value, mode):
        try:
            self.value = str(value)
        except ValueError as e:
            raise BadParameterType("path_template", value)
        assert mode in ["r", "w", "rw"]
        self.mode = mode

class cause(object):
    def __init__(self, value):
        try:
            self.value = str(value)
        except ValueError as e:
            raise BadParameterType("cause", value)


class risk(object):
    def __init__(self, value):
        try:
            self.value = str(value)
        except ValueError as e:
            raise BadParameterType("risk", value)

class sex(object):
    def __init__(self, value):
        try:
            self.value = __builtin__.int(value)
            assert self.value in [1, 2, 3]
        except ValueError as e:
            raise BadParameterType("sex", value)
