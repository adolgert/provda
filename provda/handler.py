import datetime
import json
import logging
import logging.handlers
import socket


logger = logging.getLogger("provda.handler")


class TCPJSONHandler(logging.handlers.SocketHandler):
    def __init__(self, host, port):
        super().__init__(host, port)

    def makePickle(self, record):
        record = {
            "host": "withme",
            "tags": "fake",
            "message": "hi there"
        }
        logger.debug("record is {}".format(record))
        return record


def send_tcp(record, host, port, timeout=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    logger.debug("Sending to {}:{} record {}".format(host, port, record))
    s.connect((host, port))

    pfields = json.loads(record)
    logger.debug(json.dumps(
        pfields, sort_keys=True, indent=4, separators=(',', ': ')))
    transmittable = ["agent", "entity", "activity", "used",
                     "wasAssociatedWith", "wasGeneratedBy"]
    simple_fields = [str, float, int, bool]
    logger.debug("Not transmitting {}".format(
        set(pfields.keys())-set(transmittable)))
    total = 0
    for kind in transmittable:
        if kind in pfields:
            for instance in pfields[kind].keys():
                ifields = pfields[kind][instance]
                logger.debug("ifields {}".format(ifields))
                stamp = datetime.datetime.now().isoformat()
                fields = dict()
                for name, val in ifields.items():
                    if any(isinstance(val, s) for s in simple_fields):
                        fields[name] = val
                    else:
                        fields[name] = json.dumps(val)

                fields = {k: json.dumps(v) for (k, v) in ifields.items()}
                record = json.dumps(
                    {'@message': 'create_file3',
                     '@source_host': "withme",
                     '@version': 1,
                     'prov': kind,
                     '@timestamp': stamp,
                     "@fields": fields})
                s.sendall(str.encode(record, encoding="utf-8") + b'\n')
                total = total + 1
    s.close()
    logger.debug("sent {} objects".format(total))
