.. Provda documentation master file, created by
   sphinx-quickstart on Tue Aug 16 07:26:07 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Provda's documentation!
==================================

Python library to record what ran, what it read, and what it wrote.

1. An extension to Python's logging module to be able to explicitly
   log provenance events.

2. A way to separate parameters from the code so they can be
   versioned and modified separately. Yes, it's like config files,
   but with types.

3. A set of data collection methods to retrieve the typical
   records of what code is running and who is running it.

4. A set of routines to add provenance information to different
   file types such as PDF and HDF5. Your graphs can know what made
   them.

5. A module to spy on every time your code reads and writes from
   common scientific file formats.

Contents:

.. toctree::
   :maxdepth: 2

   why
   reporting
   annotation
   intro
   usecases
   tutorial


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

