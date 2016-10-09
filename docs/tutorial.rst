========
Tutorial
========

--------------------------------------
Create an Organization-specific Import
--------------------------------------

This library is a set of tools. You can create a module
that defines for your group or software how it will use
provenance. For instance, this one defines namespaces,
ensures the logging hooks are in place, and monkey-patches
any of the covered libraries.::

    import logging
    import logstash
    import provda.logprov
    import provda.model
    import provda.patch


    namespaces = {
        "is": "https://healtdata.org/instances",
        "person": "https://healthdata.org/people",
        "code": "https://healthdata.org/code",
        "doc": "https://healthdata.org/document"
    }


    @provda.datatypes.add
    class cause:
      """Makes a typed datatype available to settings."""
      def __init__(self, value, tracked=True):
        self.tracked = tracked
        self.value = str(value)


    @provda.datatypes.add
    class risk:
      """Makes a typed datatype available to settings."""
      def __init__(self, value, tracked=True):
        self.tracked = tracked
        self.value = str(value)


    def setup():
        prov_doc = provda.model.ProcessDocument(namespaces)
        logging.root.addHandler(prov_doc)
        prov_doc.addHandler(logstash.TCPLogstashHandler("localhost", 5959))


    def get_parameters(name, value=None):
        return provda.parameters.get_parameters(name, value)

    setup()

The logstash handler will send messages from the provenance collection
as JSON to logstash.


------------------
Automatic Patching
------------------

We know pandas.read_hdf() will open a file, so the patching mechanism
of provda.patch will track when this routine is called and then
record that a file was read. If you import provda.patch, it
patches whatever is already loaded and recognized.


-------------------------
Explicit Provenance Calls
-------------------------

The provenance store is attached to the logging mechanism, so it's
available through any logger you create.::

    import logging
    import reader

    logger = logging.getLogger("my.module")
    def transform(causes):
      for acause in causes:
        logger.read_file("/in/filename")
        risks = reader.read("/in/filename", "r")
        # do stuff
        logger.create_file("/in/filename.out")
        result = reader.write("/in/filename.out, "w")

-----------------------------
Insert Provenance Into a File
-----------------------------

It's possible to insert strings into some documents such
as HDF5 and PDF. That takes the following form.::

   f = h5py.write("file.hdf")
   f.close()
   provda.annotate.hdf("file.hdf")

This will always write into the file the provenance
of the current process and that it wrote this file.

--------------
Settings Files
--------------

Provda can make it easier to get settings. Use it the way
you would use logging.::

   import logging
   import provda

    GLOBALS = {
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
      }

   logger = logging.getLogger("provda.tests.sample")
   parameters = provda.get_parameters("provda.tests.sample", GLOBALS)

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
