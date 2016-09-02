=========
Use Cases
=========

Use cases are a way to think through using a piece of
software before you write it. They become test
cases and documentation.


-----------
Development
-----------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
D1. Grunewald writes a script in the FBD repository.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Preconditions* FBD repository exists and is checked
out to the current machine's drive.

#. Grunewald starts a git feature branch.
#. Grunewald downloads a template Python script.
   The top of the script has a parameters section.
#. Grunewald writes code, occasionally needing constants.
#. Grunewald checks a web page describing types of constants
   and how to add them.
#. Grunewald runs the code locally on a synthetic
   dataset using a command-line parameter to set the input
   and output directories.
#. Grunewald submits the script to the cluster with
   qsub on a different dataset.
#. Grunewald checks the code into FBD with default
   values that point to regular computation.

Questions from this use case:

#. Is there a set of known locations, or rules for
   creating and finding known data locations? Assuming
   that's separate, it would be a separate component,
   how do we mix those rules into parameter-setting?
#. Don't we want to record how to test things, too?
   Is there a place to run tests and record the settings
   needed for tests?

