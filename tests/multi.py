"""
This tests whether the parameters work with multiprocessing.
Unsure how to include this in unit tests b/c it's multiprocessing.
"""

import logging
from multiprocessing import Pool
import os
import sys
import provda


__modname__ = "multi"


logger = logging.getLogger(__modname__)
params = provda.get_parameters(__modname__, {
    "draws": provda.int(1000),
    "acause": provda.string("becauseisaidso")
})


G = 2


def run(args):
    logger.debug("Running args {} with draws {}".format(args, params["draws"]))
    logger.debug("Arg {} G {}".format(args, G))
    logger.debug("pid {} gpid {}".format(os.getpid(),
                                         os.getpgid(os.getpid())))
    logger.debug("argv {}".format(sys.argv))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("pid {} gpid {}".format(os.getpid(),
                                         os.getpgid(os.getpid())))
    p = Pool(2)
    G = 3
    p.map(run, [3, 7, "incongruent"])
