import sys
from argparse import ArgumentParser
from importlib.metadata import version

from sdm_modbus_zmq.client import Client


def entry_point():
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-h", "--host")
    parser.add_argument("-p", "--port")
    parser.add_argument("-t", "--topic")

    args = parser.parse_args()

    if args.version:
        print(version("sdm-modbus-zmq"))
        sys.exit()
    elif args.host and args.port and args.topic:
        client = Client(args.host, args.port, args.topic)
        client.get_data()
    else:
        print("Bad input.")
