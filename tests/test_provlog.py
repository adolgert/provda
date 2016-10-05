import logging
from io import StringIO
import sys
import provda
import provda.logprov

def test_create_file():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("provda.test.test_provlog")
    logger.create_file("/ihme/forecasting/file.hdf")
    # logger.read_file("/ihme/forecasting/file2.hdf")
    # logger.read_table("sql:///server", "schema", "table")
    # logger.initiate_run()?


def test_turn_off_printing_provenance():
    logging.basicConfig(level=logging.INFO)
    # You have to tell the handlers not to print.
    for h in logging.root.handlers:
        print("setting handler {}".format(h))
        h.setLevel(level=logging.INFO)
    logger = logging.getLogger("provda.test.test_provlog")
    logger.create_file("/ihme/forecasting/file.hdf")


def test_show_provenance_stream():
    s = StringIO()
    handler = logging.StreamHandler(s)
    handler.addFilter(provda.logprov.ProvFilter())
    logging.root.addHandler(handler)
    logger = logging.getLogger("provda.test.test_provlog")
    logger.create_file("/ihme/forecasting/file.hdf")
    before = s.tell()
    assert before > 0
    logger.debug("But don't show this.")
    assert s.tell()-before == 0
