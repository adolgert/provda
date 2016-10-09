"""
This represents an organization-specific use of provda.
Import this, and defaults are set.
"""
import logging
import provda.logprov
import provda.model
import provda.patch


namespaces = {
    "is": "https://healtdata.org/instances",
    "person": "https://healthdata.org/people",
    "code": "https://healthdata.org/code",
    "doc": "https://healthdata.org/document"
}


def setup():
    prov_doc = provda.model.ProcessDocument(namespaces)
    logging.root.addHandler(prov_doc)


def get_parameters(name, value=None):
    return provda.parameters.get_parameters(name, value)


setup()
