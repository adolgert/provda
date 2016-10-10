import logging
import numpy as np
import org_specific


logger = logging.getLogger("module")
params = org_specific.get_parameters("module", {"draws": 1000})


if __name__ == "__main__":
    logger.create_file("/ihme/forecasting/data/file.hdf")
    logger.create_file("/ihme/forecasting/data/another.csv")
