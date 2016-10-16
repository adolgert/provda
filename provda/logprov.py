import logging
import sys


class ProvLogger(logging.Logger):
    """
    This adds calls which explicitly add provenance information to the
    logging stream. This is a separate stream from the messages one
    usually logs, so they circumvent the "level" specification associate
    with debug, info, and error messages.

    Extra information associated with these messages is meant to mirror
    https://www.w3.org/TR/2013/REC-prov-n-20130430/
    """
    def __init__(self, name, level=logging.NOTSET):
        super(ProvLogger, self).__init__(name, level)

    def write_file(self, file_path, role, *args, **kwargs):
        """
        Messages created by create_file have a dictionary of extra
        arguments in their resulting LogRecord, including record.prov=True
        to say that it's a provenance record.

        :param file_path: The path to the file.
        :param args: Any extra args
        :param kwargs: and extra keyword args.
        """
        # Use _log because self.log can exclude msg based on level.
        kw = {"path": file_path, "kind": "create_file", "role": role}
        kw.update(kwargs)
        self._log(logging.DEBUG, "ProvWrite".format(file_path), args,
                  extra={"prov": kw})

    def read_file(self, file_path, role, *args, **kwargs):
        """
        Report that we are reading the file with the given path.

        :param file_path str: The filesystem path to the file.
        :param role: What role the file plays. Its model entity.
        :param args:  Any additional arguments.
        :param kwargs:  Or keyword arguments.
        """
        kw = {"path": file_path, "kind": "read_file", "role": role}
        kw.update(kwargs)
        self._log(logging.DEBUG, "ProvRead".format(file_path), args,
                  extra={"prov": kw})

    def write_table(self, database, schema, table, role, *args, **kwargs):
        """
        Report we are writing to a particular table.

        :param database str: The database hostname.
        :param schema: Which schema contains the table.
        :param table: The table itself.
        :param role: The model entity in the table.
        :param args:  Any additional arguments.
        :param kwargs:  Or keyword arguments.
        """
        kw = {"database": database, "schema": schema, "table": table,
              "kind": "write_table", "role": role}
        kw.update(kwargs)
        self._log(logging.DEBUG, "ProvWrite {}".format(kw), args,
                  extra={"prov": kw})

    def read_table(self, database, schema, table, role, *args, **kwargs):
        """
        Report we are reading from a particular table.

        :param database str: The database hostname.
        :param schema: Which schema contains the table.
        :param table: The table itself.
        :param role: The model entity in the table.
        :param args:  Any additional arguments.
        :param kwargs:  Or keyword arguments.
        """
        kw = {"database": database, "schema": schema, "table": table,
              "kind": "read_table", "role": role}
        kw.update(kwargs)
        self._log(logging.DEBUG, "ProvRead {}".format(kw), args,
                  extra={"prov": kw})

    def start_tasks(self, executable, task_ids, *args, **kwargs):
        """
        This process is starting processes to complete tasks with these
        task ids. This is a way to say this process is starting batch
        jobs or multiple processes on a node.

        :param executable: The name of the executable we are starting.
        :param task_ids: The job ids of the started jobs.
        """
        self._log(logging.DEBUG, "ProvTasks {}".format(task_ids), args,
                  extra={"prov": {"executable": executable,
                                  "ids": task_ids, "kind": "start_tasks"}})


logging.setLoggerClass(ProvLogger)


class ProvFilter:
    """
    This filter will accept only LogRecords with a "prov" keyword.
    It looks like it should just be a single function, and it should,
    and this is fixed in Python 3, but the class works
    for backward-compatibility.
    """
    def filter(self, record):
        return hasattr(record, "prov")


def add_handler(logger):
    """
    Add a handler to a logging.Logger which will print a message in such
    a way that you can pick out the provenance messages using grep.
    :param logger: A logging.logger, such as logging.root.
    """
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.addFilter(ProvFilter())
    formatter = logging.Formatter(fmt="logprov: %(message)")
    sh.setFormatter(formatter)
    logger.addHandler(sh)
