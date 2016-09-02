"""
This sample defines templates and leaves it possible
that any way to fill in the templates will be used.
"""
import logging
import argparse
import provda
from sample_cfg import param


logger = logging.getLogger("provda.tests.sample")


def transform_files(cds):
    value = param["cod_in"]
    print(provda.input_file("cod_in", **param))
    print(provda.input_file("risks_in", **param))
    print(provda.output_file("cod_out", **param))
    print("memory limit {} is untracked".format(param["memlimit"]))



if __name__ == "__main__":
    provda.read_json(open("sample.settings"))

    parser = argparse.ArgumentParser(description="Testing provenance")
    provda.add_arguments(parser)
    args = parser.parse_args()
    provda.namespace_settings(args)
    provda.config_logging(args)

    logger.debug("logger debug")
    logger.info("logger info")
    logger.warn("logger warn")
    logger.error("logger error")

    transform_files((param["acause"], param["risk"],
                     param["sex_id"]))
