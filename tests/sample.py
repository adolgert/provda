"""
This sample defines templates and leaves it possible
that any way to fill in the templates will be used.
"""
import logging
import argparse
import provda


parameters = provda.get_parameters("provda.tests.sample")


def transform_files(cds):
    value = parameters["cod_in"]
    print(parameters.infile("cod_in", **parameters))
    print(parameters.infile("risks_in", **parameters))
    print(parameters.outfile("cod_out", **parameters))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    provda.read_json(open("sample.settings"))

    parser = argparse.ArgumentParser(description="Testing provenance")
    provda.add_arguments(parser.add_argument_group("settings"))
    args = parser.parse_args()
    provda.namespace_settings(args)

    transform_files((parameters["acause"], parameters["risk"],
                     parameters["sex_id"]))
