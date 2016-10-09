import datetime
import json
import logging.handlers
import socket
import logstash_formatter


class TCPJSONHandler(logging.handlers.SocketHandler):
    def __init__(self, host, port):
        super().__init__(host, port)

    def makePickle(self, record):
        record = {
            "host": "withme",
            "tags": "fake",
            "message": "hi there"
        }
        print("record is {}".format(record))
        return record


def send_tcp(record, host, port, timeout=10):
    stamp = datetime.datetime.now().isoformat()
    fields = json.loads(record)
    fields = {"table": "anytable", "account": "adolgert"}
    record = json.dumps(
        {'@message': 'create_file3',
         '@source_host': "withme",
         '@version': 1,
         '@timestamp': stamp,
         "@fields": fields})
    # formatter = logstash_formatter.LogstashFormatter()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    print("Sending to {}:{} record {}".format(host, port, record))
    s.connect((host, port))
    s.sendall(str.encode(record, encoding="utf-8") + b'\n')
    s.close()
