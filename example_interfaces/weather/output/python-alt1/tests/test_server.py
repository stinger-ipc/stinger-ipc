"""
Tests for weather server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC

from weatheripc.server import WeatherServer
from weatheripc.property import WeatherPropertyAccess, WeatherInitialPropertyValues
from weatheripc.interface_types import *
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


class WeatherServerSetup:

    def __init__(self):
        self.initial_property_values = self.get_initial_property_values()

        self.location = self.initial_property_values.location
        self.current_temperature = self.initial_property_values.current_temperature
        self.current_condition = self.initial_property_values.current_condition
        self.daily_forecast = self.initial_property_values.daily_forecast
        self.hourly_forecast = self.initial_property_values.hourly_forecast
        self.current_condition_refresh_interval = self.initial_property_values.current_condition_refresh_interval
        self.hourly_forecast_refresh_interval = self.initial_property_values.hourly_forecast_refresh_interval
        self.daily_forecast_refresh_interval = self.initial_property_values.daily_forecast_refresh_interval
        self.reset_modified_flags()

    def get_initial_property_values(self) -> WeatherInitialPropertyValues:
        initial_property_values = WeatherInitialPropertyValues(
            location=LocationProperty(
                latitude=3.14,
                longitude=3.14,
            ),
            current_temperature=3.14,
            current_condition=CurrentConditionProperty(
                condition=WeatherCondition.SNOWY,
                description="apples",
            ),
            daily_forecast=DailyForecastProperty(
                monday=ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
                tuesday=ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
                wednesday=ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
            ),
            hourly_forecast=HourlyForecastProperty(
                hour_0=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
                hour_1=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
                hour_2=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
                hour_3=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
            ),
            current_condition_refresh_interval=42,
            hourly_forecast_refresh_interval=42,
            daily_forecast_refresh_interval=42,
        )
        return initial_property_values

    def get_property_access(self) -> WeatherPropertyAccess:
        property_access = WeatherPropertyAccess(
            location_getter=self.get_property_location,
            location_setter=self.set_property_location,
            current_temperature_getter=self.get_property_current_temperature,
            current_condition_getter=self.get_property_current_condition,
            daily_forecast_getter=self.get_property_daily_forecast,
            hourly_forecast_getter=self.get_property_hourly_forecast,
            current_condition_refresh_interval_getter=self.get_property_current_condition_refresh_interval,
            current_condition_refresh_interval_setter=self.set_property_current_condition_refresh_interval,
            hourly_forecast_refresh_interval_getter=self.get_property_hourly_forecast_refresh_interval,
            hourly_forecast_refresh_interval_setter=self.set_property_hourly_forecast_refresh_interval,
            daily_forecast_refresh_interval_getter=self.get_property_daily_forecast_refresh_interval,
            daily_forecast_refresh_interval_setter=self.set_property_daily_forecast_refresh_interval,
        )
        return property_access

    def reset_modified_flags(self):
        self.location_modified_flag = False
        self.current_temperature_modified_flag = False
        self.current_condition_modified_flag = False
        self.daily_forecast_modified_flag = False
        self.hourly_forecast_modified_flag = False
        self.current_condition_refresh_interval_modified_flag = False
        self.hourly_forecast_refresh_interval_modified_flag = False
        self.daily_forecast_refresh_interval_modified_flag = False

    def create_server(self, mock_connection) -> WeatherServer:
        server = WeatherServer(mock_connection, "test_instance", self.get_property_access())
        return server

    def get_property_location(self):
        """Return the value for the 'location' property."""
        return self.location

    def set_property_location(self, value: LocationProperty):
        """Set the value for the 'location' property."""
        self.location_modified_flag = True
        self.location = value

    def get_property_current_temperature(self):
        """Return the value for the 'current_temperature' property."""
        return self.current_temperature

    def get_property_current_condition(self):
        """Return the value for the 'current_condition' property."""
        return self.current_condition

    def get_property_daily_forecast(self):
        """Return the value for the 'daily_forecast' property."""
        return self.daily_forecast

    def get_property_hourly_forecast(self):
        """Return the value for the 'hourly_forecast' property."""
        return self.hourly_forecast

    def get_property_current_condition_refresh_interval(self):
        """Return the value for the 'current_condition_refresh_interval' property."""
        return self.current_condition_refresh_interval

    def set_property_current_condition_refresh_interval(self, value: int):
        """Set the value for the 'current_condition_refresh_interval' property."""
        self.current_condition_refresh_interval_modified_flag = True
        self.current_condition_refresh_interval = value

    def get_property_hourly_forecast_refresh_interval(self):
        """Return the value for the 'hourly_forecast_refresh_interval' property."""
        return self.hourly_forecast_refresh_interval

    def set_property_hourly_forecast_refresh_interval(self, value: int):
        """Set the value for the 'hourly_forecast_refresh_interval' property."""
        self.hourly_forecast_refresh_interval_modified_flag = True
        self.hourly_forecast_refresh_interval = value

    def get_property_daily_forecast_refresh_interval(self):
        """Return the value for the 'daily_forecast_refresh_interval' property."""
        return self.daily_forecast_refresh_interval

    def set_property_daily_forecast_refresh_interval(self, value: int):
        """Set the value for the 'daily_forecast_refresh_interval' property."""
        self.daily_forecast_refresh_interval_modified_flag = True
        self.daily_forecast_refresh_interval = value


@pytest.fixture
def server_setup():
    setup = WeatherServerSetup()
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


class TestWeatherServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"


class TestWeatherServerProperties:

    def test_get_initial_location_property(self, server_setup, server):
        """Test that the server can get the 'location' property."""
        assert server.location == server_setup.location, "Getter for property 'location' returned incorrect value"

    def test_location_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'location' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_location_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830532a80>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'location'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830532a80>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.location
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_location_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "latitude": 1.0,
            "longitude": 3.14,
        }
        prop_obj = LocationProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x70c830532a80>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_location.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.location_modified_flag, "Setter for property 'location' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'location'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_current_temperature_property(self, server_setup, server):
        """Test that the server can get the 'current_temperature' property."""
        assert server.current_temperature == server_setup.current_temperature, "Getter for property 'current_temperature' returned incorrect value"

    def test_current_temperature_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'current_temperature' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_current_temperature_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830532b70>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'current_temperature'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830532b70>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = CurrentTemperatureProperty(temperature_f=initial_property_values.current_temperature)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_current_temperature_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "temperature_f": 1.0,
        }
        prop_obj = CurrentTemperatureProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x70c830532b70>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_current_temperature.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.current_temperature_modified_flag is not True, "Setter for property 'current_temperature' was called on read-only property"

    def test_get_initial_current_condition_property(self, server_setup, server):
        """Test that the server can get the 'current_condition' property."""
        assert server.current_condition == server_setup.current_condition, "Getter for property 'current_condition' returned incorrect value"

    def test_current_condition_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'current_condition' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_current_condition_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c8305336e0>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'current_condition'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c8305336e0>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.current_condition
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_current_condition_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "condition": WeatherCondition.SUNNY,
            "description": "apples",
        }
        prop_obj = CurrentConditionProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x70c8305336e0>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_current_condition.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.current_condition_modified_flag is not True, "Setter for property 'current_condition' was called on read-only property"

    def test_get_initial_daily_forecast_property(self, server_setup, server):
        """Test that the server can get the 'daily_forecast' property."""
        assert server.daily_forecast == server_setup.daily_forecast, "Getter for property 'daily_forecast' returned incorrect value"

    def test_daily_forecast_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'daily_forecast' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_daily_forecast_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830533890>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'daily_forecast'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830533890>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.daily_forecast
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_daily_forecast_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "monday": ForecastForDay(high_temperature=1.0, low_temperature=1.0, condition=WeatherCondition.SUNNY, start_time="example", end_time="example"),
            "tuesday": ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
            "wednesday": ForecastForDay(high_temperature=1.0, low_temperature=1.0, condition=WeatherCondition.SUNNY, start_time="foo", end_time="foo"),
        }
        prop_obj = DailyForecastProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x70c830533890>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_daily_forecast.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.daily_forecast_modified_flag is not True, "Setter for property 'daily_forecast' was called on read-only property"

    def test_get_initial_hourly_forecast_property(self, server_setup, server):
        """Test that the server can get the 'hourly_forecast' property."""
        assert server.hourly_forecast == server_setup.hourly_forecast, "Getter for property 'hourly_forecast' returned incorrect value"

    def test_hourly_forecast_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'hourly_forecast' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_hourly_forecast_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830533920>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'hourly_forecast'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830533920>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.hourly_forecast
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_hourly_forecast_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "hour_0": ForecastForHour(temperature=1.0, starttime=datetime.now(UTC), condition=WeatherCondition.SUNNY),
            "hour_1": ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
            "hour_2": ForecastForHour(temperature=1.0, starttime=datetime.now(UTC), condition=WeatherCondition.SUNNY),
            "hour_3": ForecastForHour(temperature=1.0, starttime=datetime.now(UTC), condition=WeatherCondition.SUNNY),
        }
        prop_obj = HourlyForecastProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x70c830533920>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_hourly_forecast.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.hourly_forecast_modified_flag is not True, "Setter for property 'hourly_forecast' was called on read-only property"

    def test_get_initial_current_condition_refresh_interval_property(self, server_setup, server):
        """Test that the server can get the 'current_condition_refresh_interval' property."""
        assert server.current_condition_refresh_interval == server_setup.current_condition_refresh_interval, "Getter for property 'current_condition_refresh_interval' returned incorrect value"

    def test_current_condition_refresh_interval_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'current_condition_refresh_interval' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_current_condition_refresh_interval_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830532a20>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'current_condition_refresh_interval'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830532a20>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = CurrentConditionRefreshIntervalProperty(seconds=initial_property_values.current_condition_refresh_interval)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_current_condition_refresh_interval_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "seconds": 2020,
        }
        prop_obj = CurrentConditionRefreshIntervalProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x70c830532a20>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_current_condition_refresh_interval.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.current_condition_refresh_interval_modified_flag, "Setter for property 'current_condition_refresh_interval' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'current_condition_refresh_interval'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_hourly_forecast_refresh_interval_property(self, server_setup, server):
        """Test that the server can get the 'hourly_forecast_refresh_interval' property."""
        assert server.hourly_forecast_refresh_interval == server_setup.hourly_forecast_refresh_interval, "Getter for property 'hourly_forecast_refresh_interval' returned incorrect value"

    def test_hourly_forecast_refresh_interval_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'hourly_forecast_refresh_interval' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_hourly_forecast_refresh_interval_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830533dd0>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'hourly_forecast_refresh_interval'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830533dd0>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = HourlyForecastRefreshIntervalProperty(seconds=initial_property_values.hourly_forecast_refresh_interval)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_hourly_forecast_refresh_interval_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "seconds": 2020,
        }
        prop_obj = HourlyForecastRefreshIntervalProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x70c830533dd0>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_hourly_forecast_refresh_interval.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.hourly_forecast_refresh_interval_modified_flag, "Setter for property 'hourly_forecast_refresh_interval' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'hourly_forecast_refresh_interval'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_get_initial_daily_forecast_refresh_interval_property(self, server_setup, server):
        """Test that the server can get the 'daily_forecast_refresh_interval' property."""
        assert server.daily_forecast_refresh_interval == server_setup.daily_forecast_refresh_interval, "Getter for property 'daily_forecast_refresh_interval' returned incorrect value"

    def test_daily_forecast_refresh_interval_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'daily_forecast_refresh_interval' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_daily_forecast_refresh_interval_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830533bc0>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'daily_forecast_refresh_interval'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x70c830533bc0>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = DailyForecastRefreshIntervalProperty(seconds=initial_property_values.daily_forecast_refresh_interval)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_daily_forecast_refresh_interval_receive(self, server, server_setup, mock_connection):
        mock_connection.clear_published_messages()

        # Create and simulate receiving a property update message
        prop_data = {
            "seconds": 2020,
        }
        prop_obj = DailyForecastRefreshIntervalProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"3.1415926535"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x70c830533bc0>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_daily_forecast_refresh_interval.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Verify that server property was updated

        assert server_setup.daily_forecast_refresh_interval_modified_flag, "Setter for property 'daily_forecast_refresh_interval' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'daily_forecast_refresh_interval'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"


class TestWeatherServerSignals:

    def test_server_emit_current_time(self, server, mock_connection):
        """Test that the server can emit the 'current_time' signal."""
        signal_data = {
            "current_time": "apples",
        }  # type: Dict[str, Any]
        server.emit_current_time(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("<bound method Signal.topic of <stingeripc.components.Signal object at 0x70c8305327e0>>".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'current_time'"

        msg = published_list[0]
        expected_topic = "<bound method Signal.topic of <stingeripc.components.Signal object at 0x70c8305327e0>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = CurrentTimeSignalPayload(**signal_data)  # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"


class TestWeatherServerMethods:

    def test_server_handle_refresh_daily_forecast_method(self, server, mock_connection):
        """Test that the server can handle the 'refresh_daily_forecast' method."""
        handler_callback_data = None
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler() -> None:
            nonlocal received_args
            received_args = {}
            return handler_callback_data

        server.handle_refresh_daily_forecast(handler)

        # Create and simulate receiving a method call message
        method_data = {}  # type: Dict[str, Any]
        method_obj = RefreshDailyForecastMethodRequest(**method_data)
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
        assert received_args is not None, "Handler for method 'refresh_daily_forecast' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'refresh_daily_forecast'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = {}  # type: Dict[str, Any]
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_refresh_hourly_forecast_method(self, server, mock_connection):
        """Test that the server can handle the 'refresh_hourly_forecast' method."""
        handler_callback_data = None
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler() -> None:
            nonlocal received_args
            received_args = {}
            return handler_callback_data

        server.handle_refresh_hourly_forecast(handler)

        # Create and simulate receiving a method call message
        method_data = {}  # type: Dict[str, Any]
        method_obj = RefreshHourlyForecastMethodRequest(**method_data)
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
        assert received_args is not None, "Handler for method 'refresh_hourly_forecast' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'refresh_hourly_forecast'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = {}  # type: Dict[str, Any]
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"

    def test_server_handle_refresh_current_conditions_method(self, server, mock_connection):
        """Test that the server can handle the 'refresh_current_conditions' method."""
        handler_callback_data = None
        received_args = None  # type: Optional[Dict[str, Any]]

        def handler() -> None:
            nonlocal received_args
            received_args = {}
            return handler_callback_data

        server.handle_refresh_current_conditions(handler)

        # Create and simulate receiving a method call message
        method_data = {}  # type: Dict[str, Any]
        method_obj = RefreshCurrentConditionsMethodRequest(**method_data)
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
        assert received_args is not None, "Handler for method 'refresh_current_conditions' was not called"
        assert method_data == received_args, f"Handler arguments {received_args} do not match expected {method_data}"

        # Verify that a response message was published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for method 'refresh_current_conditions'."

        resp_msg = published_list[0]
        assert resp_msg.correlation_data == correlation_data, "Correlation data in response does not match expected value"
        assert resp_msg.topic == response_topic, "Response topic does not match expected value"

        # Verify response payload
        resp_payload = json.loads(resp_msg.payload.decode("utf-8"))

        expected_resp_dict = {}  # type: Dict[str, Any]
        assert resp_payload == expected_resp_dict, f"Response payload '{resp_payload}' does not match expected '{expected_resp_dict}'"
