"""
Tests for Full server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC

from fullipc.server import FullServer
from fullipc.property import FullPropertyAccess, FullInitialPropertyValues
from fullipc.interface_types import *
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


class FullServerSetup:

    def __init__(self):
        self.initial_property_values = self.get_initial_property_values()

        self.favorite_number = self.initial_property_values.favorite_number
        self.favorite_foods = self.initial_property_values.favorite_foods
        self.lunch_menu = self.initial_property_values.lunch_menu
        self.family_name = self.initial_property_values.family_name
        self.last_breakfast_time = self.initial_property_values.last_breakfast_time
        self.last_birthdays = self.initial_property_values.last_birthdays
        self.reset_modified_flags()

    def get_initial_property_values(self) -> FullInitialPropertyValues:
        initial_property_values = FullInitialPropertyValues(
            favorite_number=42,
            favorite_foods=FavoriteFoodsProperty(
                drink="apples",
                slices_of_pizza=42,
                breakfast="apples",
            ),
            lunch_menu=LunchMenuProperty(
                monday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
                tuesday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
            ),
            family_name="apples",
            last_breakfast_time=datetime.now(UTC),
            last_birthdays=LastBirthdaysProperty(
                mom=datetime.now(UTC),
                dad=datetime.now(UTC),
                sister=None,
                brothers_age=42,
            ),
        )
        return initial_property_values

    def get_property_access(self) -> FullPropertyAccess:
        property_access = FullPropertyAccess(
            favorite_number_getter=self.get_property_favorite_number,
            favorite_number_setter=self.set_property_favorite_number,
            favorite_foods_getter=self.get_property_favorite_foods,
            favorite_foods_setter=self.set_property_favorite_foods,
            lunch_menu_getter=self.get_property_lunch_menu,
            family_name_getter=self.get_property_family_name,
            family_name_setter=self.set_property_family_name,
            last_breakfast_time_getter=self.get_property_last_breakfast_time,
            last_breakfast_time_setter=self.set_property_last_breakfast_time,
            last_birthdays_getter=self.get_property_last_birthdays,
            last_birthdays_setter=self.set_property_last_birthdays,
        )
        return property_access

    def reset_modified_flags(self):
        self.favorite_number_modified_flag = False
        self.favorite_foods_modified_flag = False
        self.lunch_menu_modified_flag = False
        self.family_name_modified_flag = False
        self.last_breakfast_time_modified_flag = False
        self.last_birthdays_modified_flag = False

    def create_server(self, mock_connection) -> FullServer:
        server = FullServer(mock_connection, "test_instance", self.get_property_access())
        return server

    def get_property_favorite_number(self):
        """Return the value for the 'favorite_number' property."""
        return self.favorite_number

    def set_property_favorite_number(self, value: int):
        """Set the value for the 'favorite_number' property."""
        self.favorite_number_modified_flag = True
        self.favorite_number = value

    def get_property_favorite_foods(self):
        """Return the value for the 'favorite_foods' property."""
        return self.favorite_foods

    def set_property_favorite_foods(self, value: FavoriteFoodsProperty):
        """Set the value for the 'favorite_foods' property."""
        self.favorite_foods_modified_flag = True
        self.favorite_foods = value

    def get_property_lunch_menu(self):
        """Return the value for the 'lunch_menu' property."""
        return self.lunch_menu

    def get_property_family_name(self):
        """Return the value for the 'family_name' property."""
        return self.family_name

    def set_property_family_name(self, value: str):
        """Set the value for the 'family_name' property."""
        self.family_name_modified_flag = True
        self.family_name = value

    def get_property_last_breakfast_time(self):
        """Return the value for the 'last_breakfast_time' property."""
        return self.last_breakfast_time

    def set_property_last_breakfast_time(self, value: datetime):
        """Set the value for the 'last_breakfast_time' property."""
        self.last_breakfast_time_modified_flag = True
        self.last_breakfast_time = value

    def get_property_last_birthdays(self):
        """Return the value for the 'last_birthdays' property."""
        return self.last_birthdays

    def set_property_last_birthdays(self, value: LastBirthdaysProperty):
        """Set the value for the 'last_birthdays' property."""
        self.last_birthdays_modified_flag = True
        self.last_birthdays = value


@pytest.fixture
def server_setup():
    setup = FullServerSetup()
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


class TestFullServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"


class TestFullServerProperties:

    def test_get_initial_favorite_number_property(self, server_setup, server):
        """Test that the server can get the 'favorite_number' property."""
        assert server.favorite_number == server_setup.favorite_number, "Getter for property 'favorite_number' returned incorrect value"

    def test_favorite_number_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'favorite_number' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_favorite_number_value()

        published_list = mock_connection.find_published("full/{}/property/favoriteNumber/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'favorite_number'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "full/{}/property/favoriteNumber/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = FavoriteNumberProperty(number=initial_property_values.favorite_number)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_favorite_number_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "number": 2020,
        }
        prop_obj = FavoriteNumberProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="full/{}/property/favoriteNumber/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_favorite_number.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.favorite_number_modified_flag, "Setter for property 'favorite_number' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'favorite_number'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_favorite_foods_property(self, server_setup, server):
        """Test that the server can get the 'favorite_foods' property."""
        assert server.favorite_foods == server_setup.favorite_foods, "Getter for property 'favorite_foods' returned incorrect value"

    def test_favorite_foods_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'favorite_foods' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_favorite_foods_value()

        published_list = mock_connection.find_published("full/{}/property/favoriteFoods/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'favorite_foods'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "full/{}/property/favoriteFoods/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.favorite_foods
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_favorite_foods_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "drink": "example",
            "slices_of_pizza": 42,
            "breakfast": "foo",
        }
        prop_obj = FavoriteFoodsProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="full/{}/property/favoriteFoods/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_favorite_foods.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.favorite_foods_modified_flag, "Setter for property 'favorite_foods' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'favorite_foods'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_lunch_menu_property(self, server_setup, server):
        """Test that the server can get the 'lunch_menu' property."""
        assert server.lunch_menu == server_setup.lunch_menu, "Getter for property 'lunch_menu' returned incorrect value"

    def test_lunch_menu_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'lunch_menu' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_lunch_menu_value()

        published_list = mock_connection.find_published("full/{}/property/lunchMenu/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'lunch_menu'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "full/{}/property/lunchMenu/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.lunch_menu
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_lunch_menu_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "monday": Lunch(drink=True, sandwich="example", crackers=1.0, day=DayOfTheWeek.MONDAY, order_number=2020, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=551)),
            "tuesday": Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
        }
        prop_obj = LunchMenuProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="full/{}/property/lunchMenu/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_lunch_menu.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.lunch_menu_modified_flag is not True, "Setter for property 'lunch_menu' was called on read-only property"

    def test_get_initial_family_name_property(self, server_setup, server):
        """Test that the server can get the 'family_name' property."""
        assert server.family_name == server_setup.family_name, "Getter for property 'family_name' returned incorrect value"

    def test_family_name_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'family_name' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_family_name_value()

        published_list = mock_connection.find_published("full/{}/property/familyName/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'family_name'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "full/{}/property/familyName/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = FamilyNameProperty(family_name=initial_property_values.family_name)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_family_name_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "family_name": "example",
        }
        prop_obj = FamilyNameProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="full/{}/property/familyName/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_family_name.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.family_name_modified_flag, "Setter for property 'family_name' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'family_name'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_last_breakfast_time_property(self, server_setup, server):
        """Test that the server can get the 'last_breakfast_time' property."""
        assert server.last_breakfast_time == server_setup.last_breakfast_time, "Getter for property 'last_breakfast_time' returned incorrect value"

    def test_last_breakfast_time_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'last_breakfast_time' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_last_breakfast_time_value()

        published_list = mock_connection.find_published("full/{}/property/lastBreakfastTime/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'last_breakfast_time'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "full/{}/property/lastBreakfastTime/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = LastBreakfastTimeProperty(timestamp=initial_property_values.last_breakfast_time)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_last_breakfast_time_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "timestamp": datetime.now(UTC),
        }
        prop_obj = LastBreakfastTimeProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="full/{}/property/lastBreakfastTime/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_last_breakfast_time.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.last_breakfast_time_modified_flag, "Setter for property 'last_breakfast_time' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'last_breakfast_time'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_last_birthdays_property(self, server_setup, server):
        """Test that the server can get the 'last_birthdays' property."""
        assert server.last_birthdays == server_setup.last_birthdays, "Getter for property 'last_birthdays' returned incorrect value"

    def test_last_birthdays_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'last_birthdays' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_last_birthdays_value()

        published_list = mock_connection.find_published("full/{}/property/lastBirthdays/value".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'last_birthdays'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "full/{}/property/lastBirthdays/value".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.last_birthdays
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_last_birthdays_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "mom": datetime.now(UTC),
            "dad": datetime.now(UTC),
            "sister": datetime.now(UTC),
            "brothers_age": 2022,
        }
        prop_obj = LastBirthdaysProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="full/{}/property/lastBirthdays/setValue".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_last_birthdays.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.last_birthdays_modified_flag, "Setter for property 'last_birthdays' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'last_birthdays'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"


class TestFullServerSignals:

    def test_server_emit_today_is(self, server, mock_connection):
        """Test that the server can emit the 'today_is' signal."""
        signal_data = {
            "day_of_month": 42,
            "day_of_week": DayOfTheWeek.SATURDAY,
        }  # type: Dict[str, Any]
        server.emit_today_is(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("full/{}/signal/todayIs".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'today_is'"

        msg = published_list[0]
        expected_topic = "full/{}/signal/todayIs".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = TodayIsSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_server_emit_random_word(self, server, mock_connection):
        """Test that the server can emit the 'random_word' signal."""
        signal_data = {
            "word": "apples",
            "time": datetime.now(UTC),
        }  # type: Dict[str, Any]
        server.emit_random_word(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("full/{}/signal/randomWord".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'random_word'"

        msg = published_list[0]
        expected_topic = "full/{}/signal/randomWord".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = RandomWordSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"


class TestFullServerMethods:

    def test_server_handle_add_numbers_method(self, server, mock_connection):
        """Test that the server can handle the 'add_numbers' method."""
        handler_callback_data = 42
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(first, second, third) -> int:
            nonlocal received_args
            received_args = {
                "first": first,
                "second": second,
                "third": third,
            }
            return handler_callback_data

        server.handle_add_numbers(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "first": 2020,
            "second": 42,
            "third": 2022,
        }  # type: Dict[str, Any]
        method_obj = AddNumbersMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="full/{}/method/addNumbers".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'add_numbers' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'add_numbers'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = AddNumbersMethodResponse(sum=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_do_something_method(self, server, mock_connection):
        """Test that the server can handle the 'do_something' method."""
        handler_callback_data = DoSomethingMethodResponse(label="apples", identifier=42)
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(task_to_do) -> DoSomethingMethodResponse:
            nonlocal received_args
            received_args = {
                "task_to_do": task_to_do,
            }
            return handler_callback_data

        server.handle_do_something(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "task_to_do": "example",
        }  # type: Dict[str, Any]
        method_obj = DoSomethingMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="full/{}/method/doSomething".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'do_something' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'do_something'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = to_jsonified_dict(handler_callback_data)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_what_time_is_it_method(self, server, mock_connection):
        """Test that the server can handle the 'what_time_is_it' method."""
        handler_callback_data = datetime.now(UTC)
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler() -> datetime:
            nonlocal received_args
            received_args = {}
            return handler_callback_data

        server.handle_what_time_is_it(handler)

        # Create and simulate receiving a method call message
        method_data = {}  # type: Dict[str, Any]
        method_obj = WhatTimeIsItMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="full/{}/method/whatTimeIsIt".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'what_time_is_it' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'what_time_is_it'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = WhatTimeIsItMethodResponse(timestamp=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_hold_temperature_method(self, server, mock_connection):
        """Test that the server can handle the 'hold_temperature' method."""
        handler_callback_data = True
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler(temperature_celsius) -> bool:
            nonlocal received_args
            received_args = {
                "temperature_celsius": temperature_celsius,
            }
            return handler_callback_data

        server.handle_hold_temperature(handler)

        # Create and simulate receiving a method call message
        method_data = {
            "temperature_celsius": 1.0,
        }  # type: Dict[str, Any]
        method_obj = HoldTemperatureMethodRequest(**method_data)
        print(method_obj)
        response_topic = "client/test/response"
        correlation_data = b"method-1234"
        incoming_msg = Message(
            topic="full/{}/method/holdTemperature".format(server.instance_id),
            payload=method_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that handler was called with correct arguments
        assert received_args is not None, "Handler for method 'hold_temperature' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'hold_temperature'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_return_obj = HoldTemperatureMethodResponse(success=handler_callback_data)
        expected_resp_dict = to_jsonified_dict(expected_return_obj)
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"
