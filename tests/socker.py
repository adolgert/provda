"""
This script is a most direct test of how to send logging entries
to logstash and ElasticSearch.
"""
import json
import logging
import socket
import sys


logger = logging.getLogger("socker")


def send_tcp(records, host, port, timeout=10):
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

    :param record: A list of logger records.
    :param host: Hostname of logstash.
    :param port: Port is it on.
    :param timeout: A timeout in seconds.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((host, port))
    for record in records:
        record_str = json.dumps(record)
        logger.debug("Sending {}".format(record_str))
        s.sendall(str.encode(record_str, encoding="utf-8") + b'\n')
    s.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    records = [
        {
            "name": "John Doe",
            "iter": sys.argv[1],
            "env": [
                {"name": "user",
                 "value": "adolgert"},
                {"name": "SGE_TASK_ID",
                 "value": "32276"}
            ],
        },
        {
            "name": "Rick",
            "iter": sys.argv[1],
            "further": {"deeper": {"farther": {"notyet": {"there": 42}}}}
        },
        {
            "name": "Morty",
            "iter": sys.argv[1],
            "more": {"stuff": 36}
        }
    ]
    send_tcp(records, "localhost", 6000)
