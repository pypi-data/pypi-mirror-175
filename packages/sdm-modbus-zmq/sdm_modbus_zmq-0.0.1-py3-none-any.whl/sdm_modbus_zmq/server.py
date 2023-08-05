import json
import logging

import zmq

logger = logging.getLogger()


class Server:
    def __init__(self, port):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)
        logger.info(f"Zmq listening on port:{port}")

    def push(self, topic, data):
        messagedata = json.dumps(data, indent=None, separators=(",", ":"))
        logger.debug(f"{topic} {messagedata}")
        self.socket.send_string(f"{topic} {messagedata}")
