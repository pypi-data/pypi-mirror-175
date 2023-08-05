"""Test get_data"""
HOST = "test_host"
PORT = "test_port"
TOPIC = "test_topic"


def test_get_data():
    """Test get_data."""
    from sdm_modbus_zmq.client import Client

    client = Client(HOST, PORT, TOPIC)
    print(client.get_data())


test_get_data()
