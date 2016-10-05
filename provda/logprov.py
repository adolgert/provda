import getpass
import logging
import sys
import uuid


class ProvLogger(logging.Logger):
    """
    This adds calls which explicitly add provenance information to the
    logging stream. This is a separate stream from the messages one
    usually logs, so they circumvent the "level" specification associate
    with debug, info, and error messages.

    Extra information associated with these messages is meant to mirror
    https://www.w3.org/TR/2013/REC-prov-n-20130430/
    """
    process_id = uuid.uuid4()

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        if name == "root":
            user = {"user": getpass.getuser(), "type": "personAgent"}

    def create_file(self, file_path, *args, **kwargs):
        """
        Messages created by create_file have a dictionary of extra
        arguments in their resulting LogRecord, including record.prov=True
        to say that it's a provenance record.

        :param file_path: The path to the file.
        :param args: Any extra args
        :param kwargs: and extra keyword args.
        """
        file_id = uuid.uuid4()
        # Use _log because self.log can exclude msg based on level.
        kw = {"prov": True, "type": "document", "id": file_id,
              "path": file_path, "wasCreatedBy": ProvLogger.process_id}
        kw.update(kwargs)
        self._log(logging.DEBUG, "Create {}".format(file_path), args,
                 extra=kw)

    def read_file(self, file_path, *args, **kwargs):
        kw = {"prov": True, "type": "document",
              "path": file_path, "used": ProvLogger.process_id}
        kw.update(kwargs)
        self._log(logging.DEBUG, "Read {}".format(file_path), args,
                 extra=kw)

    def write_table(self, database, schema, table, *args, **kwargs):
        id = "{}/{}/{}".format(database, schema, table)
        kw = {"prov": True, "type": "table", "id": id,
              "database": database, "schema": schema,
              "table": table, "relation": "wasCreatedBy"}
        kw.update(kwargs)
        self._log(logging.DEBUG, "Create table {}".format(kw), args, extra=kw)


    def read_table(self, database, schema, table, *args, **kwargs):
        id = "{}/{}/{}".format(database, schema, table)
        kw = {"prov": True, "type": "table", "id": id,
              "database": database, "schema": schema,
              "table": table, "relation": "used"}
        kw.update(kwargs)
        self._log(logging.DEBUG, "Read table {}".format(kw), args, extra=kw)


logging.setLoggerClass(ProvLogger)


class ProvFilter:
    """
    This filter will accept only LogRecords with a "prov" keyword.
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
