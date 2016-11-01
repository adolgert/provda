"""
This class is the document that stores provenance.
"""
import collections
import logging
import uuid
import prov.model
from . import collect


logger = logging.getLogger("prov.model")


class ProvFilter:
    """
    This filter will accept only LogRecords with a "prov" keyword.
    """
    def filter(self, record):
        return hasattr(record, "prov")


class ProcessDocument:
    """
    This represents process-level provenance. There will be one per process.
    It can act as a logging.Handler for logging.
    """
    def __init__(self, namespaces):
        """
        If namespaces includes ("is", "https://healthdata.org/instances"),
        then the qualified_process_name could be "is:scalars-step-3".
        This document assumes the following namespaces:
        "is" for an instance of a program, "person" for a person,
        "code" for software code, and "doc" is a file or table.

        :param namespaces: An iterable of (short, long) namespaces.
        """
        self._document = prov.model.ProvDocument()
        self._targets = list()

        if isinstance(namespaces, collections.Mapping):
            namespaces = namespaces.items()
        for short, long in namespaces:
            self._document.add_namespace(short, long)
        default_namespaces = {
            "unk": "http://example.com/unknown",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "prov": "http://www.w3.org/ns/prov#",
            "dct": "http://purl.org/dc/terms/"
        }
        for short, long in default_namespaces.items():
            self._document.add_namespace(short, long)

        script_id, script_traits = collect.this_script()
        script_entity = self._document.entity(
            script_id, other_attributes=script_traits)
        who_id, who_traits = collect.who_ran_this_process()
        runner_agent = self._document.agent(
            who_id, other_attributes=who_traits)
        process_traits = collect.this_process()
        self.process = self._document.activity(
            "is:"+str(uuid.uuid4()), other_attributes=process_traits)
        self.process.used(script_entity)
        self.process.wasAssociatedWith(runner_agent)
        self.level = logging.DEBUG

    def setLevel(self, level):
        pass

    # Logging handler interface.
    def filter(self, record):
        return hasattr(record, "prov")

    def handle(self, record):
        if not hasattr(record, "prov"):
            print("Where is the prov? {}".format(record))
            raise Exception("Every record at this point should be filtered.")
        p = record.prov
        if p["kind"] == "create_file":
            file_id = self._document.entity("doc:"+str(p["path"]))
            file_id.wasGeneratedBy(self.process)
        elif p["kind"] == "read_file":
            file_id = self._document.entity("doc:"+str(p["path"]))
            self.process.used(file_id)
        elif p["kind"] == "write_table":
            id = "{}/{}/{}".format(p["database"], p["schema"], p["table"])
            table_id = self._document.entity("doc:"+id)
            table_id.wasGeneratedBy(self.process)
        elif p["kind"] == "read_table":
            id = "{}/{}/{}".format(p["database"], p["schema"], p["table"])
            table_id = self._document.entity("doc:" + id)
            self.process.used(table_id)
        elif p["kind"] == "start_tasks":
            id = "unk:processcollection"
            subprocesses = self._document.collection(id)
            for task in p["ids"]:
                sub_proc = self._document.entity("doc:"+str(task),
                                                 {"unk:task_id": task})
                self._document.membership(subprocesses, sub_proc)
            self._document.influence(subprocesses, self.process)
        else:
            raise RuntimeError("Unknown type of provenance record {}".format(
                p["kind"]))

    def json(self):
        return self._document.serialize(format="json")

    def __str__(self):
        return self._document.get_provn()
