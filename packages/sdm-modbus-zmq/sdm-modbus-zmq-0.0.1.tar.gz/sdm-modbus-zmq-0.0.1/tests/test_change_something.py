"""Test change_something"""
HOST = "test_host"
PORT = "test_port"
TOPIC = "test_topic"


def test_change_something_true():
    """Test hange_something_true."""
    from sdm_modbus_zmq.client import Client

    client = Client(HOST, PORT, TOPIC)
    # print(client.something)
    # client.change_something(False)
    # print(client.something)


def test_change_something_false():
    """Test change_something_false."""
    from sdm_modbus_zmq.client import Client

    client = Client(HOST, PORT, TOPIC)
    # print(client.something)
    # client.change_something(False)
    # print(client.something)


test_change_something_true()
test_change_something_false()
