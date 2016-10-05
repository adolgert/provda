=================
Provenance Logger
=================

This module makes a subclass ``logging.Logger`` which has a couple of
extra methods that record provenance information. With this extra information,
those messages can be sent to
`Logstash <https://www.elastic.co/guide/en/logstash/current/input-plugins.html>`_,
or a file, or printed into
regular logging messages.

Provenance is the record of what caused something to happen.
There are two standards, the
`Open Provenance Model <http://openprovenance.org/>`_ and the
`W3C Provenance Model <https://www.w3.org/TR/prov-overview/>`_.
This will use
the `W3C PROV-N <https://www.w3.org/TR/2013/REC-prov-n-20130430/>`_
representation of provenance.

An example::

    import provda.logprov
    import logging
    logger = logging.getLogger("module.name")
    logger.create_file("/path/to/file.hdf")
    f = open("/path/to/file.hdf", "w")

That's enough to record the file opening. This logging method doesn't
make recording automatic. There is another module that can automate
the process by patching common libraries.

The second part of the process is deciding where to send the messages.
Here is a program which uses logstash to record information.::

    import logging
    import logstash
    import provda

    handler = logstash.TCPLogstashHandler("localhost", 5959)
    # Ensure only provenance messages are sent.
    handler.addFilter(provda.logprov.ProvFilter())
    logging.root.addHandler(handler)

Logging is usually used to produce human-readable messages. These
messages do have a human-readable format statement, but they are
of a different sort. They don't have an explicit debug, info,
or warning level. They are always turned on. Here's how that
works.

The way Python logging works is that the logging level is entirely
separate from its filtering mechanism. They are two separate things (surprisingly).
The level of the debugger determines whether the debugger will
return immediately from the initial call to ``debug()``, ``info()``, ``error()``,
or ``log()``. In the case of the provenance calls, these always
store the provenance information for calls to methods such
as ``logger.create_file()``. Then, the way logging works, is that
the logger, before it sends a message to a handler, such as
``StreamHandler``, will check the level of that handler and not send
it if the level is too low. In this case, all provenance records
have a level set to ``logging.DEBUG`` by default.

