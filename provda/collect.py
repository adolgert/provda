"""
This module is responsible for collecting provenance information.
These use a lot of default namespaces:

            "unk": "http://example.com/unknown",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "prov": "http://www.w3.org/ns/prov#",
            "dct": "http://purl.org/dc/terms/"

Take a look here: https://www.w3.org/TR/prov-dc/,
http://xmlns.com/foaf/spec/.
"""
import getpass
import os
import platform
import pwd
import socket
import sys
import time
import uuid
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # Python 2.7
import git
from .rfc3339 import rfc3339


def who_ran_this_process():
    p = pwd.getpwuid(os.getuid())
    user = {"unk:fullname": p.pw_gecos,
            "unk:homedir": p.pw_dir}
    return "person:"+getpass.getuser(), user


def this_script():
    if sys.argv[0] in ["-c", "-m"]:
        script_path = os.path.realpath(sys.argv[1])
    else:
        script_path = os.path.realpath(sys.argv[0])

    try:
        r = git.Repo(".", search_parent_directories=True)
        repo = {
            "unk:version_branch": r.active_branch.name,
            "unk:version_branch_hash": r.active_branch.object.hexsha
        }
        if r.remotes:
            repo["unk:version_remote"] = list(r.remotes[0].urls)[0]
        else:
            repo["unk:version_remote"] = "local"
        try:
            id = str(Path(script_path).relative_to(r.working_dir))
        except ValueError:
            id = script_path
    except git.InvalidGitRepositoryError:
        repo = {}
        id = script_path

    me = {
        "unk:script": script_path,
    }
    me.update(repo)
    return "code:"+id, me


def this_process():
    """
    Reading recipy/recipy, among other things.
    """
    if sys.argv[0] in ["-c", "-m"]:
        cmd_args = sys.argv[2:]
    else:
        cmd_args = sys.argv[1:]

    me = {
        "unk:process_id": os.getpid(),
        "unk:group_id": os.getpgid(os.getpid()),
        "unk:args": " ".join(cmd_args),
        "unk:command": sys.executable,
        "unk:hostname": socket.gethostname(),
        "unk:platform": platform.platform(),
        "unk:interpreter": sys.version.split('\n')[0],
        "unk:date": rfc3339(time.time()),
    }
    if "SGE_JOB_ID" in os.environ:
        me["unk:sge_job_id"] = os.environ["SGE_JOB_ID"]
    return me


def create_file(path):
    return {"unk:path": path, "unk:id": uuid.uuid4()}
