"""
This represents an organization-specific use of provda.
Import this, and defaults are set.
"""
import atexit
import logging
import logstash
import provda.logprov
import provda.model
import provda.patch
import provda.handler


namespaces = {
    "is": "https://healtdata.org/instances",
    "person": "https://healthdata.org/people",
    "code": "https://healthdata.org/code",
    "doc": "https://healthdata.org/document"
}


def report(model):
    print("reporting the model")
    provda.handler.send_tcp(model.json(), "localhost", 5000)


def setup():
    model = provda.model.ProcessDocument(namespaces)
    logging.root.addHandler(model)
    atexit.register(report, model)


def get_parameters(name, value=None):
    return provda.parameters.get_parameters(name, value)


setup()
