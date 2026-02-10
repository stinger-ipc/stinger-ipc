"""
Tests for Simple server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC

from simpleipc.server import SimpleServer
from simpleipc.property import SimplePropertyAccess, SimpleInitialPropertyValues
from simpleipc.interface_types import *
from stinger_python_utils.return_codes import MethodReturnCode
from pyqttier.mock import MockConnection
from pyqttier.message import Message
import json
from pydantic import BaseModel
from typing import Any, Dict


def to_jsonified_dict(model: BaseModel) -> Dict[str, Any]:
    """Convert a Pydantic model to a JSON-serializable dict."""
    json_str = model.model_dump_json(by_alias=True)
    return json.loads(json_str)


class SimpleServerSetup:

    def __init__(self):
        self.initial_property_values = self.get_initial_property_values()

        self.school = self.initial_property_values.school
        self.reset_modified_flags()

    def get_initial_property_values(self) -> SimpleInitialPropertyValues:
        initial_property_values = SimpleInitialPropertyValues(
            school="apples",
        )
        return initial_property_values

    def get_property_access(self) -> SimplePropertyAccess:
        property_access = SimplePropertyAccess(
            school_getter=self.get_property_school,
            school_setter=self.set_property_school,
        )
        return property_access

    def reset_modified_flags(self):
        self.school_modified_flag = False

    def create_server(self, mock_connection) -> SimpleServer:
        server = SimpleServer(mock_connection, "test_instance", self.get_property_access())
        return server

    def get_property_school(self):
        """Return the value for the 'school' property."""
        return self.school

    def set_property_school(self, value: str):
        """Set the value for the 'school' property."""
        self.school_modified_flag = True
        self.school = value


@pytest.fixture
def server_setup():
    setup = SimpleServerSetup()
    return setup


@pytest.fixture
def initial_property_values(server_setup):
    return server_setup.initial_property_values


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def server(server_setup, mock_connection):
    server = server_setup.create_server(mock_connection)
    yield server
    server.shutdown(timeout=0.01)


class TestSimpleServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"


class TestSimpleServerProperties:

    def test_get_initial_school_property(self, server_setup, server):
        """Test that the server can get the 'school' property."""
        assert server.school == server_setup.school, "Getter for property 'school' returned incorrect value"

    def test_school_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'school' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_school_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x7acc5cf74f50>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'school'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x7acc5cf74f50>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = SchoolProperty(name=initial_property_values.school)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_school_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "name": "example",
        }
        prop_obj = SchoolProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x7acc5cf74f50>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_school.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.school_modified_flag, "Setter for property 'school' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'school'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"


class TestSimpleServerSignals:

    def test_server_emit_person_entered(self, server, mock_connection):
        """Test that the server can emit the 'person_entered' signal."""
        signal_data = {
            "person": Person(name="apples", gender=Gender.MALE),
        }  # type: Dict[str, Any]
        server.emit_person_entered(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("<bound method Signal.topic of <stingeripc.components.Signal object at 0x7acc5ce1a7b0>>".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'person_entered'"

        msg = published_list[0]
        expected_topic = "<bound method Signal.topic of <stingeripc.components.Signal object at 0x7acc5ce1a7b0>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = PersonEnteredSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"


class TestSimpleServerMethods:

    def test_server_handle_trade_numbers_method(self, server, mock_connection):
        """Test that the server can handle the 'trade_numbers' method."""
        handler_callback_data = 42
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(your_number) -> int:
            nonlocal received_args
            received_args = {
                "your_number": your_number,
            }
            return handler_callback_data

        server.handle_trade_numbers(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "your_number": 2020,
        }  # type: Dict[str, Any]
        method_obj = TradeNumbersMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'trade_numbers' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'trade_numbers'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = TradeNumbersMethodResponse(my_number=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"
