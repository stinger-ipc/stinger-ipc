"""
Tests for SignalOnly server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from signal_onlyipc.server import SignalOnlyServer
from signal_onlyipc.interface_types import *
from pyqttier.mock import MockConnection
from pyqttier.message import Message
import json


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def server(mock_connection):
    server = SignalOnlyServer(mock_connection, "test_instance")
    yield server
    server.shutdown(timeout=0.1)


class TestServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"


# No (stinger-owned) properties to test


class TestServerSignals:

    def test_server_emit_another_signal(self, server, mock_connection):
        """Test that the server can emit the 'another_signal' signal."""
        signal_data = {
            "one": 3.14,
            "two": True,
            "three": "apples",
        }
        server.emit_another_signal(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/anotherSignal".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'another_signal'"

        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/anotherSignal".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload

        payload_dict = json.loads(msg.payload.decode("utf-8"))
        payload_obj = AnotherSignalSignalPayload.model_validate_json(msg.payload.decode("utf-8"))
        assert payload_dict.get("one") == signal_data["one"], f"Payload 'one' does not match expected value of '{ signal_data["one"]}'"
        assert payload_dict.get("two") == signal_data["two"], f"Payload 'two' does not match expected value of '{ signal_data["two"]}'"
        assert payload_dict.get("three") == signal_data["three"], f"Payload 'three' does not match expected value of '{ signal_data["three"]}'"

    def test_server_emit_bark(self, server, mock_connection):
        """Test that the server can emit the 'bark' signal."""
        signal_data = {
            "word": "apples",
        }
        server.emit_bark(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/bark".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'bark'"

        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/bark".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload

        payload_dict = json.loads(msg.payload.decode("utf-8"))
        payload_obj = BarkSignalPayload.model_validate_json(msg.payload.decode("utf-8"))
        assert payload_dict.get("word") == signal_data["word"], f"Payload 'word' does not match expected value of '{ signal_data["word"]}'"

    def test_server_emit_maybe_number(self, server, mock_connection):
        """Test that the server can emit the 'maybe_number' signal."""
        signal_data = {
            "number": 42,
        }
        server.emit_maybe_number(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/maybeNumber".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'maybe_number'"

        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/maybeNumber".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload

        payload_dict = json.loads(msg.payload.decode("utf-8"))
        payload_obj = MaybeNumberSignalPayload.model_validate_json(msg.payload.decode("utf-8"))
        assert payload_dict.get("number") == signal_data["number"], f"Payload 'number' does not match expected value of '{ signal_data["number"]}'"

    def test_server_emit_maybe_name(self, server, mock_connection):
        """Test that the server can emit the 'maybe_name' signal."""
        signal_data = {
            "name": "apples",
        }
        server.emit_maybe_name(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/maybeName".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'maybe_name'"

        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/maybeName".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload

        payload_dict = json.loads(msg.payload.decode("utf-8"))
        payload_obj = MaybeNameSignalPayload.model_validate_json(msg.payload.decode("utf-8"))
        assert payload_dict.get("name") == signal_data["name"], f"Payload 'name' does not match expected value of '{ signal_data["name"]}'"

    def test_server_emit_now(self, server, mock_connection):
        """Test that the server can emit the 'now' signal."""
        signal_data = {
            "timestamp": datetime.now(UTC),
        }
        server.emit_now(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/now".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'now'"

        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/now".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload

        payload_dict = json.loads(msg.payload.decode("utf-8"))
        payload_obj = NowSignalPayload.model_validate_json(msg.payload.decode("utf-8"))
        assert payload_dict.get("timestamp") == signal_data["timestamp"], f"Payload 'timestamp' does not match expected value of '{ signal_data["timestamp"]}'"
