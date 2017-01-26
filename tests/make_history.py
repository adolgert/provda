"""
This creates provenance history. It first claims that it will run
a bunch of subprocesses, and then it uses os.Popen to actually run them.
The subprocesses are this process, again, but with an argument that
says, "Hey, you're the child. You should log some file opens and closes."
"""
import argparse
import atexit
import copy
import logging
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
import os
import subprocess
import provda.logprov
import provda.model
import provda.handler


logger = logging.getLogger("make_history")


namespaces = {
    "is": "https://healthdata.org/instances",
    "people": "https://healthdata.org/people",
    "code": "https://healthdata.org/code",
    "doc": "https://healthdata.org/document"
}


def provda_report(model):
    print("reporting the model")
    provda.handler.send_tcp(model.json(), "localhost", 5000)


def one_process_logger(name):
    prov_logger = provda.logprov.ProvLogger(name, level=logging.DEBUG)
    model = provda.model.ProcessDocument(namespaces)
    atexit.register(provda_report, model)
    prov_logger.addHandler(model)
    return prov_logger


def log_many(tag, start):
    parent = one_process_logger("run_scalars")

    def strrange(begin, count):
        return [str(x) for x in range(begin, begin+count)]

    children = [["calculate_pafs", strrange(start, 4)],
                ["calculate_scalars", strrange(start+10, 4)],
                ["combine_scalars", strrange(start+20, 2)]]
    for executable, job_ids in children:
        parent.start_tasks(executable, job_ids)

    environment = copy.copy(os.environ)
    for run_name, with_ids in children:
        for job_id in with_ids:
            environment["SGE_JOB_ID"] = job_id
            sp = subprocess.Popen(
                  ["python", "make_history.py",
                   "--child", run_name,
                   "--tag", tag],
                  env=environment)
            if sp.wait() is not 0:
                raise Exception("One of the children failed.")


def log_one(name, tag):
    child = one_process_logger(name)
    if "paf" in name:
        child.read_file(Path("gbd") / tag / "cvd_ihd.hdf", "cause_scalar")
        child.read_table("gbd-read", "schema", "table", "risks")
        child.write_file(Path("paf") / tag / "cvd_ihd.hdf", "pafs")
    elif "calculate_scalars" in name:
        child.read_file(Path("paf") / tag / "cvd_ihd.hdf", "pafs")
        child.read_table("gbd-read", "schema", "table", "risks")
        child.write_file(Path("scalar") / tag / "cvd_ihd.hdf", "scalars")
    elif "combine" in name:
        child.read_file(Path("scalar") / tag / "cvd_ihd.hdf", "scalars")
        child.read_table("gbd-read", "schema", "table", "risks")
        child.write_table("fbd-write", "fbd",
                          "model_entity", "combined_scalars")
        child.write_file(Path("combined") / tag / "cvd_ihd.hdf",
                         "combined_scalars")
    else:
        raise Exception("Unidentified process name")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="""
Makes fake data. Start logstash. Then call this as

python make_history.py --start 243 --tag one_time
""")
    parser.add_argument("--tag", action="store", metavar="tag",
                        help="Some tag, because we tag runs.")
    parser.add_argument("--child", action="store", metavar="child")
    parser.add_argument("--start", action="store", metavar="start",
                        help="The first job_id", type=int)
    args = parser.parse_args()

    if args.child:
        assert args.tag is not None
        logger.debug("starting child {}".format(args.child))
        log_one(args.child, args.tag)
    else:
        args_start = args.start or 137
        for job_set_idx in range(10):
            log_many(args.tag+str(job_set_idx), args_start+job_set_idx*50)
