========
Tutorial
========

--------------
Settings Files
--------------


Provda can make it easier to get settings. Use it the way
you would use logging.::

   import logging
   import provda

   logger = logging.getLogger("provda.tests.sample",
          "sample.settings")
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

    parameters = provda.get_parameters("provda.tests.sample",
            "sample.settings")

    def transform_files(causes):
        while count < parameters["runlimit"]:
            # do things

A parameter can be marked as ``untracked`` when it isn't relevant
to what gets calculated. This might include settings for logging,
or whether a machine is on development or production
clusters.

---------------
File Provenance
---------------

This module offers two ways to record provenance.
It will record what database table or file a script
has read or written. It will also add provenance information
to HDF5 and PDF files.

In order to record what files were read or written, use
the ``provda.infile()`` and ``provda.outfile()`` functions::

    def transform(causes):
      for acause in causes:
        risks = pandas.open(provda.infile("risks_in", acause,
                today, 2), "r")
        # do stuff
        result = pandas.open(provda.outfile("cod_out", acause,
                today, 2), "w")

The ``infile()``, ``outfile()``, and ``inoutfile()`` commands act like
Python format commands, except that they will look in the settings
file for the format string.

When you write certain kinds of files, provda will add provenance data
to those files::

    def transform(causes):
      for acause in causes:
        # do stuff
        hdf5_file = pandas.open(provda.outfile("cod_out", acause,
                today, 2), "w")
        provda.add_provenance(hdf5_file)
        pdf = matplotlib.write("cod_out.pdf")
        provda.add_provenance(pdf)

