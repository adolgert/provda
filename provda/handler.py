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
    """
    This is sending messages to a
    `logstash tcp socket
    <https://github.com/logstash-plugins/logstash-input-tcp>_`.
    The key to understanding the format to send is that, whether
    you send over TCP or UDP, the input channel will decode
    the incoming string using a codec, and we are assuming the
    chosen one is either
    `json <https://github.com/logstash-plugins/logstash-codec-json>_` or
    `json lines
    <https://github.com/logstash-plugins/logstash-codec-json_lines>_`.
    This one works with `json_lines`. It won't work with the `json` filter.

    :param record: A logger record.
    :param host: Hostname of logstash.
    :param port: Port is it on.
    :param timeout: A timeout in seconds.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    logger.debug("Sending to {}:{} record {}".format(host, port, record))
    s.connect((host, port))

    pfields = json.loads(record)
    logger.debug(json.dumps(
        pfields, sort_keys=True, indent=4, separators=(',', ': ')))
    transmittable = ["agent", "entity", "activity", "used",
                     "wasAssociatedWith", "wasGeneratedBy"]
    document_id = list(pfields["activity"].keys())[0]
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
                    fields[name] = val

                record = json.dumps(
                    {'@message': 'create_file3',
                     '@source_host': "withme",
                     '@version': 1,
                     'prov': kind,
                     'document': document_id,
                     'instance': instance,
                     '@timestamp': stamp,
                     "@fields": fields})
                print("final json {}".format(record))
                s.sendall(str.encode(record, encoding="utf-8") + b'\n')
                total = total + 1
    s.close()
    logger.debug("sent {} objects".format(total))
