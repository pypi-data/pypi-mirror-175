import json
import logging

import zmq

logger = logging.getLogger()


class Client:
    def __init__(self, host, port, topic):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.topic = topic
        self.connection_string = f"tcp://{host}:{port}"
        logger.debug(f"Connecting to {self.connection_string}/{self.topic}")
        self.socket.connect(self.connection_string)

    def get_data(self):
        self.socket.setsockopt_string(zmq.SUBSCRIBE, str(self.topic))
        logger.debug(f"Fetching from {self.connection_string}/{self.topic}")
        recv_string = self.socket.recv()
        topic, message_data = recv_string.split()
        parsed_message_data = json.loads(message_data)
        return parsed_message_data
