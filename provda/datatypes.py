"""
These are data types to use when defining parameters.
"""
import __builtin__
import logging
import string

logger = logging.getLogger("provda.datatypes")


class BadParameterType(Exception):
    def __init__(self, target, unmatched):
        self.target = target
        self.unmatched = unmatched


class FormatterMissing(string.Formatter):
    def parse(self, format_string):
        ans = super(FormatterMissing, self).parse(format_string)
        return ans

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth):
        """
        This is a copy of the _format method in string.Formatter
        but missing keys are treated as plain text.
        """
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')
        result = []
        for literal_text, field_name, format_spec, conversion in \
                self.parse(format_string):

            # output the literal text
            if literal_text:
                result.append(literal_text)

            # if there's a field, output it
            if field_name is not None:
                # this is some markup, find the object and do
                #   the formatting

                # given the field_name, find the object it references
                #  and the argument it came from
                try:
                    obj, arg_used = self.get_field(field_name, args, kwargs)
                    if obj is None:
                        raise KeyError
                    used_args.add(arg_used)
                    obj = self.convert_field(obj, conversion)
                    format_spec = self._vformat(format_spec, args, kwargs,
                                                used_args, recursion_depth-1)
                    result.append(self.format_field(obj, format_spec))
                except KeyError as ke:
                    result.extend(["{", field_name])
                    if format_spec is not "":
                        result.extend([":", format_spec])
                    if conversion is not None:
                        result.extend(["!", conversion])
                    result.append("}")

        return ''.join(result)

_vformat = FormatterMissing().vformat

class Setting(object): pass

class int(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        self.set(value)

    def set(self, value):
        try:
            if value is not None:
                self.value = __builtin__.int(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("int", value)

    def get(self, mapping):
        return self.value

    def __repr__(self):
        return "provda.int({})".format(self.value)

    def __str__(self):
        return str(self.value)


class double(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        self.set(value)

    def set(self, value):
        try:
            if value is not None:
                self.value = __builtin__.float(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("float", value)

    def get(self, mapping):
        return self.value

    def __repr__(self):
        return "provda.double({})".format(self.value)


    def __str__(self):
        return str(self.value)


class string(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        self.set(value)

    def set(self, value):
        try:
            if value is not None:
                self.value = __builtin__.str(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("str", value)

    def get(self, mapping):
        if self.value is not None:
            return _vformat(self.value, [], mapping)
        else:
            return None

    def __repr__(self):
        return "provda.string({})".format(self.value)


    def __str__(self):
        return str(self.value)


class path_template(Setting):
    def __init__(self, value, mode, tracked=True):
        self.tracked = tracked
        assert mode in ["r", "w", "rw"]
        self.mode = mode
        self.set(value)

    def set(self, value):
        try:
            if value is not None:
                self.value = __builtin__.str(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("path_template", value)

    def get(self, mapping):
        if self.value is not None:
            return _vformat(self.value, [], mapping)
        else:
            return None

    def __repr__(self):
        return "provda.path_template({})".format(self.value)

    def __str__(self):
        return str(self.value)


class cause(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        self.set(value)

    def set(self, value):
        try:
            if value is not None:
                self.value = __builtin__.str(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("cause", value)

    def get(self, mapping):
        if self.value is not None:
            return _vformat(self.value, [], mapping)
        else:
            return None

    def __repr__(self):
        return "provda.cause({})".format(self.value)

    def __str__(self):
        return str(self.value)


class risk(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        self.set(value)

    def set(self, value):
        try:
            if value is not None:
                self.value = __builtin__.str(value)
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("risk", value)

    def get(self, mapping):
        if self.value is not None:
            return _vformat(self.value, [], mapping)
        else:
            return None

    def __repr__(self):
        return "provda.risk({})".format(self.value)


    def __str__(self):
        return str(self.value)


class sex(Setting):
    def __init__(self, value, tracked=True):
        self.tracked = tracked
        self.set(value)

    def set(self, value):
        try:
            if value is not None:
                self.value = __builtin__.int(value)
                assert self.value in [1, 2, 3]
            else:
                self.value = None
        except ValueError as e:
            raise BadParameterType("sex", value)

    def get(self, mapping):
        return self.value

    def __repr__(self):
        return "provda.sex({})".format(self.value)

    def __str__(self):
        return str(self.value)
