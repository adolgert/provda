import logging
import numpy as np
import org_specific


logger = logging.getLogger("module")
params = org_specific.get_parameters("module", { "draws": 1000})


def test_params():
    assert params["draws"] == 1000


def test_patch():
    try:
        np.save("blah")
    except:
        pass


def test_logging():
    logger.create_file("made")
