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
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        try:
            if value is not None:
                self.value = __builtin__.int(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("int", value)
    def __repr__(self):
        return "provda.int({})".format(self.value)
    def __str__(self):
        return str(self.value)


class double(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        try:
            if value is not None:
                self.value = __builtin__.float(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("float", value)

    def __repr__(self):
        return "provda.double({})".format(self.value)


    def __str__(self):
        return str(self.value)


class string(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        try:
            if value is not None:
                self.value = __builtin__.str(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("str", value)


    def __repr__(self):
        return "provda.string({})".format(self.value)


    def __str__(self):
        return str(self.value)


class path_template(Setting):
    def __init__(self, value, mode, tracked=True):
        self.tracked = tracked
        try:
            if value is not None:
                self.value = __builtin__.str(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("path_template", value)
        assert mode in ["r", "w", "rw"]
        self.mode = mode


    def __repr__(self):
        return "provda.path_template({})".format(self.value)


    def __str__(self):
        return str(self.value)


class cause(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        try:
            if value is not None:
                self.value = __builtin__.str(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("cause", value)


    def __repr__(self):
        return "provda.cause({})".format(self.value)


    def __str__(self):
        return str(self.value)


class risk(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        try:
            if value is not None:
                self.value = __builtin__.str(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("risk", value)


    def __repr__(self):
        return "provda.risk({})".format(self.value)


    def __str__(self):
        return str(self.value)


class sex(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        try:
            if value is not None:
                self.value = __builtin__.int(value)
                assert self.value in [1, 2, 3]
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("sex", value)


    def __repr__(self):
        return "provda.sex({})".format(self.value)


    def __str__(self):
        return str(self.value)
