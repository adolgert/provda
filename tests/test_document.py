from argparse import Namespace
import provda.model
import provda.logprov


namespaces = {
    "is": "https://healtdata.org/instances",
    "person": "https://healthdata.org/people",
    "code": "https://healthdata.org/code",
    "doc": "https://healthdata.org/document"
}


def test_create():
    m = provda.model.ProcessDocument(namespaces)


def test_create_file():
    m = provda.model.ProcessDocument(namespaces)
    m.handle(Namespace(prov={
        "path": "/ihme/blah/blah",
        "kind": "create_file"}))


def test_with_logger():
    m = provda.model.ProcessDocument(namespaces)
    l = provda.logprov.ProvLogger("provda.tests")
    l.addHandler(m)
    l.create_file("/ihme/forecasting/all.hdf")
    print(m)
