"""
This sample defines templates and leaves it possible
that any way to fill in the templates will be used.
"""
import logging
import argparse
import provda


logger = logging.getLogger("provda.tests.sample")
parameters = provda.get_parameters("provda.tests.sample", {
  "cod_in": "workdir/cod{acause}_{date}_{sex_id}.csv",
  "risks_in": "workdir/risks{acause}_{date}_{sex_id}.hdf5",
  "cod_out": "workdir/results{acause}_{date}_{sex_id}.hdf5",
  "acause" : "heart attack",
  "risk" : "highdiving",
  "sex_id" : 1,
  "date" : "2016_03_08",
  "untracked" : {
    "loglevel": "DEBUG",
    "memlimit": 20
    }
  })


def transform_files(cds):
    value = parameters["cod_in"]
    print(parameters.infile("cod_in", **parameters))
    print(parameters.infile("risks_in", **parameters))
    print(parameters.outfile("cod_out", **parameters))
    print("memory limit {} is untracked".format(parameters["memlimit"]))



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

    transform_files((parameters["acause"], parameters["risk"],
                     parameters["sex_id"]))
