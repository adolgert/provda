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
    print("sex_id is {}".format(param["sex_id"]))
    print("type of param {}".format(type(param)))
    print("cod_in is {}".format(param["cod_in"]))
    print(param["cod_in"])
    print(param["risks_in"])
    print(param["cod_out"])
    print("memory limit {} is untracked".format(param["memlimit"]))
    print(param["list_of_stuff"])
    assert len(param["list_of_stuff"]) == 3



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    # plog = logging.getLogger("provda")
    # plog.addHandler(handler)
    # plog.setLevel(logging.DEBUG)

    print("param is {}".format(param))
    parser = argparse.ArgumentParser(description="Testing provenance")
    print("-------------------1")
    provda.add_arguments(parser)
    print("-------------------2")
    args = parser.parse_args()
    logger.debug("About to parse namespace")
    provda.namespace_settings(args)
    logger.debug("Parsed namespace")

    logger.debug("logger debug")
    logger.info("logger info")
    logger.warn("logger warn")
    logger.error("logger error")
    list_of_stuff = param["list_of_stuff"]
    list_of_stuff.remove("one")
    print(list_of_stuff)

    transform_files((param["acause"], param["date"],
                     param["sex_id"]))
