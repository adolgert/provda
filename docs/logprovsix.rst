==========================
Logging Process Provenance
==========================
Drew Dolgert, 25 January 2017

---------------------------
Scope and Problem Statement
---------------------------

The scope of this document is automating how IHME tracks the movement
of data through its statistical computations. Knowing what made and what
uses files is a small piece of automating workflow, of
knowing what files can be deleted, of knowing how much was read
or written by a process.

.. image:: mindmap.*
   :width: 300px
   :alt: Provenance relates to workflow, measurements and file management.

This document proposes delivering a search tool based on
tracking what files and database tables each Unix process reads
and writes. It describes how this fits into the larger context of
tracking provenance of our papers for research purposes.

#. We meet GATHER requirements by asking researchers which external
   datasets were used to produce which outputs. There is no check on that.

#. There are cases where different versions of a dataset are used at
   different stages of computation.

#. We don't know what files can be deleted or are archival.

#. We don't know which files are used by other groups, which leads
   other groups to create personal caches of input files copied from
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
   :width: 500px
   :alt: Architecture for logging provenance

That flow chart doesn't necessarily map clearly to
underlying Unix processes. We might consider the same
Unix process as part of two different flows.

.. image:: provda_stages.*
   :width: 300px
   :alt: Architecture for logging provenance

Meanwhile, IHME already uses something called an NID to track
which of our products is derived from which measurements in
external papers.

---------------
Other Solutions
---------------

The in-house approaches use

1. Assiduous error-checking, famously last-minute by PBFs.

2. Track inputs in per-computation databases.

3. Associate database entries with stages of computation.

This last solution is effective where it's used. It requires
setting up a database table that makes sense. Our goal is to
provide a provenance solution that works without that kind of setup.

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

------------------------
Process-level Provenance
------------------------

We choose to record what files and databases a Unix or
Windows process reads and writes and then, from this
and information provided later, to reconstruct what
were the inputs and outputs to stages of computation.

There is a standard
`W3C Provenance Model <https://www.w3.org/TR/prov-overview/>`_
which we follow in order to have a promise that the causal
chain is complete, that future standards-based tools might work,
and that implementations in Python, R, and anything else can communicate
with each other. That model defines three entities with six
relationships. The three entities are Agent, Entity, and Activity.

.. image:: provont.*
   :width: 400px
   :alt: Process-level provenance using W3C-Prov diagram

Each entity can have subclasses, such as a collection of Activities
used below to represent a collection of jobs on the cluster,
all of which are started by the same stage of computation.
This diagram below shows our *central example of using
provenance to derive relationships.*

.. image:: ProcessProvenance.*
   :width: 500px
   :alt: Process-level provenance for a cluster job.

We make this happen by inserting commands into our Python, R,
or other code (Python is implemented now)::

    import provda.logprov
    import logging
    logger = logging.getLogger("module.name")
    logger.create_file("/path/to/file.hdf")
    f = open("/path/to/file.hdf", "w")

Behind the scenes, the library collects information on git
repository, who ran the code, where the code is on disk,
what machine it's on, what time it is, and who the current
monorail driver is out front.

.. autoclass:: provda.logprov.ProvLogger
   :members:
   :noindex:


That information gets sent to a server IHME has running
ElasticSearch. It uses the logging mechanisms we already have
in place for cluster metrics.

.. image:: Logarch.*
   :width: 300px
   :alt: Architecture for logging provenance

In terms of code, that means we develop two pieces, the provda
library and a search function. We also design the format of the
data as a logging record and as it sits in ElasticSearch.

.. image:: provda_architecture.*
   :width: 300px
   :alt: The script uses the provda library which sends to logstash which sends to ElasticSearch which is read by the search function.



--------------
User Interface
--------------

The user interface is in the
`Fungi repository <https://github.com/ihmeuw/fungi>`_ on Github.
The user interface assumes that there are records in ElasticSearch.
Those records contain unique IDs for processes, but the web of
relationships among them isn't constructed.
In addition, the moment the user makes a query, they can add information
that shapes how data is interpreted. For instance, all files in a folder
are likely related, so the fungi interface can elide the actual filenames
in favor of showing just folders.

We have not addressed how to understand stages of computation or
their relationship with NIDs or MEIDs.

.. image:: NIDERD.*
   :width: 300px
   :alt: entity-relationship diagram for NIDs, files, processes and stages


------------
Further Work
------------

The Provda repository has several sub-projects.

.. image:: ProvdaComponents.*
   :width: 500px
   :alt: All the parts of this provenance library.

#. Insert data into HDF or PDF files. These insert generic data
   and would need work to store serializations of provenance
   data in a repeatable way.

#. Read program parameters from a central database. Provenance
   implementations are supposed to abstract parameter storage
   so it sits outside of the executables. This defines Python
   data structures for parameter storage.

#. Automatically hook all open and close calls in order to guess
   what files are read or written. This is last-ditch.

There are also several other large related questions.

#. *Data checking.* Look at data before and after processing.
   Relate the two with an invariant.

#. *Timing of processes.* Knowing what ran helps interpret how long
   it ran.

#. *File retention.* This tells us what is reading data and whether
   it has ever been read by another process that is recorded.


Missing is prospective provenance.

What happens when machines are down?
What should we add to the call for creating a file?
Yes, we also add things to the file itself as a record.

