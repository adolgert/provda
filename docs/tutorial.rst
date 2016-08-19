========
Tutorial
========

Provda can make it easier to get settings. Use it the way
you would use logging.::

   import logging
   import provda

   logger = logging.getLogger("provda.tests.sample")
   parameters = provda.get_parameters("provda.tests.sample")

   def transform_files(causes):
      algorithm = parameters["algorithm"]
      logger.debug("Using algorithm {}".format(algorithm))
      # do things

   if __name__ == "__main__":
       provda.read_json(open("sample.settings"))
       parser = argparse.ArgumentParser()
       provda.add_arguments(parser)
       args = parser.parse_args()
       provda.namespace_settings(args)
       transform_files(settings["causes"])

Note that, in main, provda will add arguments to the command
line and read them. It turns each entry in the settings file
into a possible command-line argument.

The settings themselves sit in JSON-formatted files (for now), and
are, themselves, hierarchical.::

    { "provda.tests.sample" : {
      "cod_in": "workdir/cod{acause}_{date}_{sex_id}.csv",
      "risks_in": "workdir/risks{acause}_{date}_{sex_id}.hdf5",
      "cod_out": "workdir/results{acause}_{date}_{sex_id}.hdf5",
      "acause" : "heart attack",
      "risk" : "smoking",
      "sex_id" : 2,
      "date" : "2016_03_07",
      "untracked" : {
        "loglevel": "DEBUG",
        "memlimit": 20
        }
      },

      "provda.tests.submodule" : {
        "algorithm" : "steepest descent"
      },

      "provda.tests" : {
        "runlimit" : 10
      }
    }

In the example above, the ``runlimit`` variable
under ``provda.tests`` would be available to all modules
below. For instance,::

    parameters = provda.get_parameters("provda.tests.sample")

    def transform_files(causes):
        while count < parameters["runlimit"]:
            # do things

A parameter can be marked as ``untracked`` when it isn't relevant
to what gets calculated. This might include settings for logging,
or whether a machine is on development or production
clusters.

