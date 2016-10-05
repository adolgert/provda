# Provda

Python library to record what ran, what it read, and what it wrote.

We don't tell you how to store this information. We don't tell you
what you have to log. We don't tell you when to record it.
We give you tools to gather provenance data such that it will
easily map onto either the Open Provenance Model or the
W3C provenance model, approximately.

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
