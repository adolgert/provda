============
Introduction
============
The responsibility of this class is to read the settings
file and deliver it to the class while versioning the settings
and recording what files and database
tables were read and written.

------------------------------------
What problem are we trying to solve?
------------------------------------
1. Settings files let other programs (workflows) see and modify
   the behavior of a script.

   There are lots of constants in scripts. They represent
   easily-forgotten algorithmic choices, so we would like
   to make them visible. They change frequently, too, so
   they can give the impression the script changed when
   it did not.

   We want to run scripts and applications under a workflow.
   Running under a workflow means we are not running interactively,
   and the command-line argument parsing is designed for
   interactive use. We'll effectively be using settings lists
   any way you look at it, so let's do it in a regular manner.

2. Explicit provenance information about files and tables
   can be collected over the network and stored with data.

   There are lots of kinds of provenance, from tracking
   individual function calls that happened to predicting
   future database calls that will happen. We want to collect
   data at the right level.


--------------------------
What are the requirements?
--------------------------

* Have to be able to change what settings the program reads
  from outside the program.
* Have to be able to have some settings which are marked as
  unimportant for the algorithm.
* Have to know the exact filename or table name.
* Have to be able to pull settings from some service.
* Have to be able to run without thought on local computer.
* A script that starts scripts should be able to create their settings.
* Would like to record settings used, git version, each time it runs.
* Would like to embed settings into HDF and PDF files that are written.

For someone writing code, this means something that looks
roughly like Python's ConfigParser module::

   config = ConfigParser("fbd.path.filename")
   retries = config.getint("retries")

-------------------------
How does it get settings?
-------------------------
How do we start a program under a workflow and give
it its settings? We could write all settings for a run
to a directory.::

    cat > /tmp/xyz.settings <<EOF
    { "a" : 3 }
    EOF
    python script.py --settings "/tmp/xyz.settings,script.settings"

They could alternatively be piped to the class::

    cat "{ "a" : 3 }" | python script.py --settings "script.settings"

We could tell the class to retrieve them.::

    python script.py --settings "123@127.0.0.1:5007,script.settings"

Here, the address is "task_id@dotted_ip:port", where task_id
is an identifier to send to the settings server to get
the settings for this instance of the script.

We could require that all settings be versioned, so that they
are retrieved from a versioned repository by hashed object id,::

    python script.py --settings "a374h12,script.settings"

or by an explicit version number::

    python script.py --settings "2.1.497,script.settings"

----------------------------
What's in the settings file?
----------------------------

The settings file could have a .ini style,::

    mu = 3.7
    algorithm = gradient descent

It could follow the convention from high energy physics,
of having tracked and untracked parameters, so that some
parameters can be considered run properties which don't
affect the algorithm,::

    [tracked]
    mu = 3.7
    algorithm = gradient descent
    [untracked]
    cores = 4
    maxmem = 8GB

The tracked/untracked for the physics folks doesn't exactly
translate here if we want to have a separate script for
each tuple of (cause, risk, sex, year). Those would be tracked.
Maybe what we want is something that's templated.::

    [tracked]
    mu = 3.7
    algorithm = gradient descent
    cod_in = gbd_out{acause}_{risk}.hdf
    [templated]
    acause = heart attack
    risk = excitement
    [untracked]
    cores = 4
    maxmem = 8GB



*Are the scripts themselves hierarchical?*
For instance, you might have one script that does a series
of steps, each in a separate module (Python .py file).
In this case, each one could have its own part of the settings
file, delineated according to its dotted name (fbd.risk_factors.do_stuff).


*Should the file be in INI, Yaml, or JSON?*
We need to support UTF-8 very well.
INI is fine for key-value with sections, and it's super easy.
Yaml is designed to be human-readable and easy for a computer
to write prettily, and it handles more complex data structures
such as hierarchical objects of lists and dictionaries.
JSON has the advantage of being the wire format of
Restful interfaces.

Using a Python module or R script would work to set variables,
too. It might be more intelligible to programmers already
working in those languages.

XML is a possibility. It's designed for a computer to read
and write, and designed to be read correctly. It isn't
great for people, though.


*Should it store types for the variables?*
Should it have a level of complexity similar to that
of Argparse, which allows default arguments, functions
to verify arguments before the script sees them,
and other odd rules?

JSON has a separate way to check its form, sort of like
XML schema. Wait a minute, what about XML Schema?
Staying away from that because we want human-readable.
