from io import StringIO
import logging
import numpy as np
import provda.logprov
import provda.patch


def test_basic_patch():
    logging.basicConfig(level=logging.DEBUG)
    s = StringIO()
    handler = logging.StreamHandler(s)
    logging.root.addHandler(handler)
    before = s.tell()
    np.save("z.np", np.array([1,2,3]))
    assert s.tell() - before > 0


def test_open():
    logging.basicConfig(level=logging.DEBUG)
    s = StringIO()
    handler = logging.StreamHandler(s)
    logging.root.addHandler(handler)
    before = s.tell()
    try:
        provda.patch.open("z.np")
    except FileNotFoundError:
        pass
    assert s.tell() - before > 0
    try:
        provda.patch.open("z.np", mode="w")
    except FileNotFoundError:
        pass
