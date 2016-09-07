"""
This sample defines templates and leaves it possible
that any way to fill in the templates will be used.
"""
import logging
import argparse
import provda
from sample_cfg import param


logger = logging.getLogger("provda.tests.sample")
#param = provda.get_parameters("provda.tests.sample")


def transform_files(cds):
    print("type of param {}".format(type(param)))
    print("cod_in is {}".format(param["cod_in"]))
    print(provda.input_file(param["cod_in"], **param))
    print(provda.input_file(param["risks_in"], **param))
    print(provda.output_file(param["cod_out"], **param))
    print("memory limit {} is untracked".format(param["memlimit"]))



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    # plog = logging.getLogger("provda")
    # plog.addHandler(handler)
    # plog.setLevel(logging.DEBUG)

    print("param is {}".format(param))

    parser = argparse.ArgumentParser(description="Testing provenance")
    provda.add_arguments(parser)
    args = parser.parse_args()
    provda.namespace_settings(args)

    logger.debug("logger debug")
    logger.info("logger info")
    logger.warn("logger warn")
    logger.error("logger error")

    transform_files((param["acause"], param["date"],
                     param["sex_id"]))
