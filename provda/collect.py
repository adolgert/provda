"""
This module is responsible for collecting provenance information.
"""
import getpass
import os.path
import platform
import socket
import sys
import time
import uuid
import git
from rfc3339 import rfc3339


THIS_PROCESS_PROV_ID = uuid.uuid4()


def who_ran_this_process():
    user = {"id": getpass.getuser(),
            "type": "personAgent"}
    return user


def this_process():
    """
    Reading recipy/recipy, among other things.
    """
    if sys.argv[0] in ["-c", "-m"]:
        script_path = os.path.realpath(sys.argv[1])
        cmd_args = sys.argv[2:]
    else:
        script_path = os.path.realpath(sys.argv[0])
        cmd_args = sys.argv[1:]

    try:
        r = git.Repo(".", search_parent_directories=True)
        repo = {
            "version_branch": r.active_branch.name,
            "version_branch_hash": r.active_branch.object.hexsha
        }
        if r.remotes:
            repo["version_remote"] = list(r.remotes[0].urls)[0]
        else:
            repo["version_remote"] = "local"
    except git.InvalidGitRepositoryError:
        repo = {}

    me = {
        "id": str(THIS_PROCESS_PROV_ID),
        "script": script_path,
        "args": " ".join(cmd_args),
        "command": sys.executable,
        "hostname": socket.gethostname(),
        "process_id": os.getpid,
        "environment": [platform.platform(),
                        "python " + sys.version.split('\n')[0]],
        "date": rfc3339(time.time()),
        "type": "software"
    }
    me.update(repo)
    return me


def create_file(path):
    return {"type": "artifact", "path": path, "id": uuid.uuid4()}


def flatten(process_descr, file_descr):
    """
    We have to put provenance information into files as a flat
    list of attributes, so this encodes a relation, wasGeneratedBy,
    between two entities and then stores them by name.
    :param process: A dictionary describing the process artifact.
    :param file: A dictionary describint the file artifact.
    :return: A dictionary that's flat with everything.
    """
    msg = {"process": process_descr["id"], "artifact": file_descr["id"],
           "relation": "wasGeneratedBy"}
    for entity in [process_descr, file_descr]:
        for k, v in entity:
            msg["{}_{}".format(entity["id"], k)]=str(v)
    return msg


def inflate(kv):
    """
    This takes the key-value pairs and extracts them into two
    objects and a relation between them.
    :param kv: A dictionary of key-value pairs
    :return: A hierarchical dictionary with the relation and items related.
    """
    entities = [k for k in kv if not k.contains("_")]
    res = {x: {} for x in entities}
    res["relation"]=kv["relation"]

    for k, v in kv.items():
        under = k.find("_")
        if under > 0:
            which = k[:under]
            val = k[under+1:]
            res[which][val] = v
    return res
