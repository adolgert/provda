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

Logan Sandar and John Daniel argue that the settings need
to be typed. Their main argument is that typing gives a way
to specify what are inputs and outputs to the script, which
gives one tool with which to specify prospective provenance,
meaning we could figure out what the script will read and write
before it runs. A second argument is that typing parameters
lets us do runtime checks that arguments are correct.
For instance, a "cause" should be a cause of death, chosen
from a given list. A "date" should follow our goofy
non-RFC3339 date format. Types would also make argparse work
better with type checking.

The settings module implements a hierarchical format
similar to logging. It's fun to have the hierarchical definition,
but it means that there is a global definition of settings
which makes it impossible to have two objects in the same
Python process with different settings. Maybe that's a problem.

---------------------------------
Alternative Settings File Formats
---------------------------------
There are lots of options. Let's write out some alternatives
to get a look at them.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Location Inline, Type Python Dict
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Pro* It's right at the top of the file, where globals go.
No need to mess with Python's relative import syntax. There
is some default typing from using Python objects, and this could
be augmented by making stronger typing on those objects.

*Con* It's in the file itself, and people think of settings
as being something you write outside the file. Plus, this
means you have to import all of the imports this file needs
in order to get at the settings.::

    param = parameters.get_parameters("provda.tests.sample", {
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

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Location Inline, Type Dict + types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*Pro* It's right at the top of the file, where globals go.
No need to mess with Python's relative import syntax. There
is some default typing from using Python objects, and this could
be augmented by making stronger typing on those objects.

*Con* It's in the file itself, and people think of settings
as being something you write outside the file. Plus, this
means you have to import all of the imports this file needs
in order to get at the settings.::

    param = parameters.get_parameters("provda.tests.sample", {
      "cod_in": path("workdir/cod{acause}_{date}_{sex_id}.csv", "in"),
      "risks_in": path("workdir/risks{acause}_{date}_{sex_id}.hdf5", "in"),
      "cod_out": path("workdir/results{acause}_{date}_{sex_id}.hdf5", "out"),
      "acause" : cause("heart attack", "in"),
      "risk" : risk("highdiving", "in"),
      "sex_id" : sex(1, "in"),
      "date" : date("2016_03_08", "in"),
      "untracked" : {
        "loglevel": string("DEBUG"),
        "memlimit": int(20)
        }
      })

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Location External, Type JSON
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*Pro* It's a known format, the same one that would be used
by restful services as a default.

*Con* I'm not sure how to convince Python to open the settings
file that is next to the module. Python relative imports
work with ``from . import sample_settings``, but that only
works when the modules are in a package, and we run fbd either
as a package or as a script, so that could be confusing. When running
a script, relative imports fail, so you have to use
``import sample_settings`` instead. I can find where the module
is located after it runs using ``sample.__file__``,
but Python decides which to load
if there is a conflict at runtime, so I don't want to guess before
it's loaded.

The example below also mixes two things, JSON
and JSON-Schema, so it mixes the standard::

    { "provda.tests.sample", {
      "cod_in": { value="workdir/cod{acause}_{date}_{sex_id}.csv",
        "type"="path_template",
        "mode"="in"},
      "risks_in": { value="workdir/risks{acause}_{date}_{sex_id}.hdf5",,
        "type"="path_template",
        "mode"="in"},
      "cod_out": { value="workdir/results{acause}_{date}_{sex_id}.hdf5", "out"),
        "type"="path_template",
        "mode"="in"},
      "acause" : { value = "heart attack",
        type = "cause",
        mode = "in"},
      "risk" : { value = "highdiving",
        type = "risk",
        mode = "in"},
      "sex_id" : { value=1,
        type = "sex",
        mode = "in"},
      "date" : { value = "2016_03_08",
        type = "datestring",
        mode = "in" },
      "untracked" : {
        "loglevel": "DEBUG",
        "memlimit": 20
        }
      }
    }

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Location External, Type JSON with Schema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*Pro* It's a known format, the same one that would be used
by restful services as a default. Maybe we could add to the
default schema so that it would recognize causes.

*Con* Again, finding external files is difficult. This
version would require people to learn JSON schema, which
look a little hairy. Maybe what happens is that we have a simple
type system from which I could build schema, if that becomes
helpful.

First, the schema, which I think I'm doing wrong (look at
`online examples <http://json-schema.org/example2.html>`_), but it's
something like this::

    {
    "title" : "provda.tests.sample",
    "type" : "object",
    "properties" : {
        "cod_in" : {
            "type" : "string"
        },
        "risks_in" : {
            "type" : "string"
        },
        "acause" : {
            "type" : "cause"
        },
        "risk" : {
            "type" : "risk"
        }
    }
    }

and then the JSON itself is the same concise version::

    {
      "cod_in" : "workdir/cod{acause}_{date}_{sex_id}.csv",
      "risks_in": "workdir/risks{acause}_{date}_{sex_id}.hdf5",
      "cod_out": "workdir/results{acause}_{date}_{sex_id}.hdf5",
      "acause" : "heart attack",
      "risk" : "highdiving",
      "sex_id" : value=1,
      "date" : "2016_03_08",
      "untracked" : {
        "loglevel": "DEBUG",
        "memlimit": 20
        }
    }


---------------
Other Questions
---------------
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

*Should we use interpolation?*
This feature would look at the settings, and if one of
them refers to another, then it does the replacement.
I'm not sure interpolation is an excellent idea when settings
can come from any module. Maybe a module-local
interpolation would make sense. Timing of when interpolation
happens would matter, too. Default arguments shouldn't
interpolate before there is a chance to set current values
for this run of the script or module.
