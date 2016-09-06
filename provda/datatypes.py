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

class Setting(object): pass

class int(Setting):
    def __init__(self, value):
        try:
            self.value = __builtin__.int(value)
        except ValueError as e:
            raise BadParameterType("int", value)
    def __repr__(self):
        return "provda.int({})".format(self.value)
    def __str__(self):
        return str(self.value)

class double(Setting):
    def __init__(self, value):
        try:
            self.value = float(value)
        except ValueError as e:
            raise BadParameterType("float", value)

    def __repr__(self):
        return "provda.int({})".format(self.value)


    def __str__(self):
        return str(self.value)


class string(Setting):
    def __init__(self, value):
        try:
            self.value = str(value)
        except ValueError as e:
            raise BadParameterType("str", value)


    def __repr__(self):
        return "provda.int({})".format(self.value)


    def __str__(self):
        return str(self.value)


class path_template(Setting):
    def __init__(self, value, mode):
        try:
            self.value = str(value)
        except ValueError as e:
            raise BadParameterType("path_template", value)
        assert mode in ["r", "w", "rw"]
        self.mode = mode


    def __repr__(self):
        return "provda.int({})".format(self.value)


    def __str__(self):
        return str(self.value)


class cause(Setting):
    def __init__(self, value):
        try:
            self.value = str(value)
        except ValueError as e:
            raise BadParameterType("cause", value)


    def __repr__(self):
        return "provda.int({})".format(self.value)


    def __str__(self):
        return str(self.value)


class risk(Setting):
    def __init__(self, value):
        try:
            self.value = str(value)
        except ValueError as e:
            raise BadParameterType("risk", value)


    def __repr__(self):
        return "provda.int({})".format(self.value)


    def __str__(self):
        return str(self.value)


class sex(Setting):
    def __init__(self, value):
        try:
            self.value = __builtin__.int(value)
            assert self.value in [1, 2, 3]
        except ValueError as e:
            raise BadParameterType("sex", value)


    def __repr__(self):
        return "provda.int({})".format(self.value)


    def __str__(self):
        return str(self.value)
