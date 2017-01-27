==========================
Logging Process Provenance
==========================
This section is a handout for a meeting to review project direction
on 26 January 2017.

---------------------------
Scope and Problem Statement
---------------------------

The scope of this document is automating how IHME tracks the movement
of data through its statistical computations. Knowing what made and what
uses files is a small piece of automating workflow, of
knowing what files can be deleted, of knowing how much was read
or written by a process.

.. image:: mindmap.*
   :width: 3in
   :align: center
   :alt: Provenance relates to workflow, measurements and file management.

This document proposes delivering a search tool to tell us
what files and database tables each Unix process reads
and writes. The document describes how this fits into the larger context of
tracking provenance of our papers for research purposes.
Current work sits in the
`Provda repository <https://stash.ihme.washington.edu/projects/CP/repos/provda/browse>`_
and `Fungi repository <https://github.com/ihmeuw/fungi>`_.

*Problems*

#. We currently meet GATHER requirements by asking researchers which external
   datasets were used to produce which outputs.

#. Sometimes different versions of a dataset are used at
   different stages of computation.

#. We don't know what files can be deleted or are archival.

#. We don't know which files are used by other groups, so
   other groups create personal caches of input files copied from
   other teams.

=============  ==================================================================
Term           Definition
=============  ==================================================================
NID            Unique identifier of a set of data in the GDBx data repository
MEID           Modelable entity is an internal data product defined in a database
Unix process   Single instance of a running program.
Stage          Part of a production pipeline known by name.
Logstash       Service to gather log messages from a computer.
ElasticSearch  Service to search a set of unstructured documents.
Provenance     Record of causal events.
=============  ==================================================================

We think about computation in terms of a flow chart.

.. image:: Fbd2015.*
   :width: 6in
   :align: center
   :alt: Architecture for logging provenance

That flow chart doesn't necessarily map clearly to
underlying Unix processes. We might consider the same
Unix process as part of two different flows.

.. image:: provda_stages.*
   :width: 2.5in
   :align: center
   :alt: Architecture for logging provenance

Meanwhile, IHME already tracks computation with NIDs, MEIDs,
log files, and lots of database entries. We have to work alongside
those.

---------------
Other Solutions
---------------

The in-house approaches use

1. Assiduous error-checking, famously last-minute
   observations by post-bachelor fellows.

2. Track inputs in databases for a portion of the work
   we do.

This last solution is effective where it's used. It requires
setting up a database table that makes sense. Our goal is to
provide a provenance solution that works with explicit annotation
in code but without database schema creation.

General approaches to automating provenance have historically
been too focused on acquiring a complete causal record, so they
tend to get jettisoned by research teams.

#. Several commercial products track complete provenance of
   computations done in Jupyter Notebooks. Sense.io is among them,
   but there are two more.

#. `Margo Seltzer's Research <http://www.eecs.harvard.edu/margo/research.html>`_
   creates a provenance-capturing service with a simple interface.
   It isn't suitable for parallel access to the service without work.

#. `YesWorkflow paper <https://arxiv.org/abs/1502.02403>`_ and
   `YesWorkflow repository <https://github.com/yesworkflow-org>`_
   insert annotations into code to show when it reads or writes
   data.

#. An approach in high-energy physics requires that every on-road calculation
   be submitted as a configuration script that specifies what
   files it needs and will produce.

This work will use Seltzer's approach on what to store
but not use the software that group created. We'll favor, instead,
systems designed for fault-tolerance and scalability.


------------------------
Process-level Provenance
------------------------

The approach chosen here is to record what files and databases a Unix or
Windows process reads and writes and then, from this
and information provided at search time, to reconstruct what
were the inputs and outputs to stages of computation.

There is a standard
`W3C Provenance Model <https://www.w3.org/TR/prov-overview/>`_
which we follow in order to have a promise that the causal
chain is complete, that future standards-based tools might work,
and that implementations in Python, R, and anything else can communicate
with each other. That model defines three entities with six
relationships. The three entities are Agent, Entity, and Activity.

.. image:: provont.*
   :width: 4in
   :align: center
   :alt: Process-level provenance using W3C-Prov diagram

Each entity can have subclasses, such as a collection of Activities
used below to represent a collection of jobs on the cluster,
all of which are started by the same stage of computation.
This diagram below shows our *central example of using
provenance to derive relationships.*

.. image:: ProcessProvenance.*
   :width: 4in
   :align: center
   :alt: Process-level provenance for a cluster job.

Every IHME researcher is expected to insert commands into our Python, R,
or other code (Python is implemented now)::

    import provda.logprov
    import logging
    logger = logging.getLogger("module.name")
    logger.create_file("/path/to/file.hdf")
    f = open("/path/to/file.hdf", "w")

Behind the scenes, the library collects information on the git
repository, who ran the code, where the code is on disk,
what machine it's on, what time it is, and who last drove
the monorail past our building. Below are all the calls
a programmer would use.

.. autoclass:: provda.logprov.ProvLogger
   :members:
   :noindex:


That information gets sent to a server IHME has running
ElasticSearch. It uses the logging mechanisms we already have
in place for cluster metrics. (We're not running Kafka but could.)

.. image:: Logarch.*
   :width: 3in
   :align: center
   :alt: Architecture for logging provenance

In terms of code, that means we develop two pieces, the provda
library and a search function. We also design the format of the
data as a logging record and as it sits in ElasticSearch.

.. image:: provda_architecture.*
   :width: 3in
   :align: center
   :alt: The script uses the provda library which sends to logstash which sends to ElasticSearch which is read by the search function.

The prov library is an external effort to codify W3C-PROV in Python.

--------------
User Interface
--------------

The user interface is in the
`Fungi repository <https://github.com/ihmeuw/fungi>`_ on Github.
The user interface assumes that there are records in ElasticSearch.
Those records contain unique IDs for processes, but the web of
relationships among them isn't represented in ElasticSearch,
so the user interface reads records and relates them.
The moment the user makes a query, they can add information
that shapes how data is interpreted. For instance, all files in a folder
are likely related, so the fungi interface can elide the actual filenames
in favor of showing just folders.

There is a working query interface, but it just gets records.
Here is a *made-up interface* based on what we could do with
the metadata already stored::

   (py36) > ./esprov list_stages --hours 10
   run_rates.py, tag=casper, user=adolgert, 2017-01-27 1:40
   scalars.py, tag=regen_rates, user=adolgert, 2017-01-27 2:32
   run_rates.py, tag=run_fast, user=adolgert, 2017-01-27 4:17

   (py36) > ./esprov info casper --hours 1
   tag=casper, user=adolgert, 2017-01-27 4:17, 196-way
   executable=run_rates.py --tag casper --conf with_parallel
   input directories:
     /ihme/forecasting/data/pop/latest
     /ihme/forecasting/data/runs/conf
   output directories:
     /ihme/forecasting/data/pop_rt/20170127_casper

There is a lot of work to do for the client because, while the work
to define provenance assures us the puzzle pieces fit, we have
to later piece them together and relate them in ways that matter.

.. image:: NIDERD.*
   :width: 3in
   :align: center
   :alt: entity-relationship diagram for NIDs, files, processes and stages

*Questions*

#. Applications can qsub hierarchically. What do you condense
   for display and what not?

#. Model entities (MEIDs) and other database entries also track
   computations. How would file-based provenance relate to those?

#. We have not addressed how to understand stages of computation or
   their relationship with NIDs. Process-level provenance
   mixes which incoming data is associated with which outgoing data.

#. We think of stages as several steps of Unix processes. Those
   would have to be defined on top of this interface.



------------
Further Work
------------

The Provda repository has several sub-projects.

.. image:: ProvdaComponents.*
   :width: 5in
   :align: center
   :alt: All the parts of this provenance library.

#. Insert data into HDF or PDF files. These insert generic data
   and would need work to store serializations of provenance
   data in a repeatable way.

#. Read program parameters from a central database. Provenance
   implementations are supposed to abstract parameter storage
   so it sits outside of the executables. This defines Python
   data structures for parameter storage.

#. Automatically hook all open and close calls in order to guess
   what files are read or written. It does work.

There are also several other large related questions.

#. *Data checking.* Look at data before and after processing.
   Relate the two with an invariant.

#. *Timing of processes.* Knowing what ran helps interpret how long
   it ran.

#. *File retention.* This tells us what is reading data and whether
   it has ever been read by another process that is recorded.

#. *Reliability.* What happens when you compute off the cluster,
   off-campus? What if machines are down?

#. *Completeness.* Is this enough? Should we track NIDs?
