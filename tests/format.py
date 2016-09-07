import logging
import string

logger = logging.getLogger("provda.tests.format")

class FormatterMissing(string.Formatter):
    # def __init__(self):
    #     super(FormatterMissing, self).__init__(self)

    def parse(self, format_string):
        logger.debug("parse enter '{}'".format(format_string))
        ans = super(FormatterMissing, self).parse(format_string)
        logger.debug("parse leave")
        return ans

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth):
        """
        This is a copy of the _format method in string.Formatter
        but it changes how it handles missing keys.
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
                    used_args.add(arg_used)
                    obj = self.convert_field(obj, conversion)
                    format_spec = self._vformat(format_spec, args, kwargs,
                                                used_args, recursion_depth-1)
                    result.append(self.format_field(obj, format_spec))
                except KeyError as ke:
                    result.extend(["{", field_name])
                    if format_spec is not "":
                        logger.debug(
                            "format spec is type {}".format(type(format_spec)))
                        result.extend([":", format_spec])
                    if conversion is not None:
                        result.extend(["!", conversion])
                    result.append("}")

        return ''.join(result)

    def get_field(self, field_name, args, kwargs):
        logger.debug("get_field enter {}".format(field_name))
        ans=super(FormatterMissing, self).get_field(field_name, args, kwargs)
        print("get_field {}".format(ans))
        logger.debug("get_field leave")
        return ans
        # if isinstance(key, int):
        #     return args[key]
        # elif key in kwargs:
        #     return kwargs[key]
        # else:
        #     return "{key}"

    def get_value(self, key, args, kwargs):
        logger.debug("get_value enter {}".format(key))
        ans=super(FormatterMissing, self).get_value(key, args, kwargs)
        print("get_value {}".format(ans))
        logger.debug("get_value leave")
        return ans

    def format_field(self, value, format_spec):
        logger.debug("format_field enter {} {}".format(value, format_spec))
        ans = super(FormatterMissing, self).format_field(value, format_spec)
        logger.debug("format_field leave {}".format(ans))
        return ans

    def convert_field(self, value, conversion):
        logger.debug("convert_field enter {} {}".format(value, conversion))
        ans = super(FormatterMissing, self).convert_field(value, conversion)
        logger.debug("convert_field leave {}".format(ans))
        return ans


def run():
    args = ["Bill", "what"]
    kwargs = { "hi" : "Susan", "there" : None}
    hiless = { "there" : "Bob"}
    s="good{hi:3}morning{there!s}joe{0}"
    f=FormatterMissing()
    print("and the result is: {}".format(f.vformat(s, args, kwargs)))
    print("")
    print("and the result is: {}".format(f.vformat(s, args, hiless)))
    print("and the result is: {}".format(f.vformat(s, ["needed"], {})))

    print("----------------------")
    for literal_text, field_name, format_spec, conversion in f.parse(s):
        print("literal text {}".format(literal_text))
        print("field_name {}".format(field_name))
        print("format spec {}".format(format_spec))
        print("conversion {}".format(conversion))

        if field_name is not None:
            field = f.get_field(field_name, args, kwargs)
            print("field is {}".format(field))
        print("")



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
