=================
Why This Library?
=================


There are several academic provenance systems, but none of them are in common
use. I conclude that we don't know how to do this yet in general, even though
we know many of the tools and techniques. This library compiles tools
according to a practical, yet principled, set of techniques, so that IHME
can enact the kind of provenance recording we need.

The practical, yet principled, approach comes from `Margo Seltzer's talk
at TAPP 2012 <https://www.usenix.org/conference/tapp12/workshop-program/presentation/macko>`_
about the
`Core Provenance Library <https://github.com/End-to-end-provenance/core-provenance-library>`_.
It means that we know that there are three kinds of objects in the world
and five kinds of relationships among them according to either the
`Open Provenance Model <http://openprovenance.org/>`_ or the
`W3C Provenance Model <https://www.w3.org/TR/prov-overview/>`_, so we'll
use that structure for provenance assertions, but that we'll give up on
detailed schema for attributes of those objects and relationships.
The rules are these:

1. We use the language of `W3C PROV-N <https://www.w3.org/TR/2013/REC-prov-n-20130430/>`_
   because it is human-readable, so there are entities, activities, and agents.
   There is a library, called `prov <https://github.com/trungdong/prov>`_,
   that implements the W3C PROV model. That's what we use under the hood.
   The `prov <https://github.com/trungdong/prov>`_ library defines provenance
   in general. This library uses that to make a process-level set
   of assumptions.

2. Every entity, activity, or agent has a unique identifier (id) constructed
   from two pieces, a domain and a name. The domain may be an application
   or an organization.

3. An entity, activity, or agent may have versions. The tuple
   (domain, name, version) must be unique.

4. Each entity, activity, or agent also has a type which comes from the W3C
   PROV model, if possible. For instance, an entity may have type=document.

5. Beyond that, there are key-value pairs assigned to entities or relationships.

PROV-N provides this cute little language that looks like::

    entity(e1)
    activity(ex:a1, [ex:type="process"])
    wasGeneratedBy(e1, a1, 2016-10-10T16:00:00)

The prov library will serialize and deserialize to both
PROV-N and JSON formats. We can either send those to a provenance
store or embed them in HDF or PDF files.

.. image:: ProvdaComponents.*
   :width: 300px
   :alt: All the parts of this provenance library.

Where to go for more provenance
-------------------------------

* `Open Provenance Model <http://openprovenance.org/>`_
* `W3C Provenance Model <https://www.w3.org/TR/prov-overview/>`_
* `End-to-end provenance <https://github.com/End-to-end-provenance>`_ on Github.
  Look at a
  `sample of using that library <https://github.com/End-to-end-provenance/core-provenance-library/blob/master/test/standalone-test/test-simple.cpp>`_ for a sense of what we want to
  do here.
* `YesWorkflow paper <https://arxiv.org/abs/1502.02403>`_ and
  `YesWorkflow repository <https://github.com/yesworkflow-org>`_
* `Recipy <https://github.com/recipy/recipy>`_, which patches common
  scientific calls in order to observe provenance.
* `Vistrails <https://www.vistrails.org>`_
* `Sumatra <https://pythonhosted.org/Sumatra/>`_
* `Margo Seltzer's Research <http://www.eecs.harvard.edu/margo/research.html>`_
* The `Springer <https://www.springer.com>`_ proceedings on
  Provenance and Annotation of Data and Processes.
