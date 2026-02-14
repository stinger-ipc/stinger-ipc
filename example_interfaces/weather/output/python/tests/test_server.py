"""
Tests for weather server.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC

from weatheripc.server import WeatherServer
from weatheripc.property import WeatherInitialPropertyValues
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

    def create_server(self, mock_connection) -> WeatherServer:
        server = WeatherServer(mock_connection, "test_instance", self.initial_property_values)
        return server


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

    def test_server_location_property_initialization(self, server, initial_property_values):
        """Test that the location server property is initialized correctly."""
        assert hasattr(server, "location"), "Server missing property 'location'"
        assert server.location is not None, "Property 'location' not initialized properly"
        assert server.location == initial_property_values.location, "Property 'location' value does not match expected value"

    def test_location_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'location' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_location_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd4166960>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'location'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd4166960>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.location
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_location_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'location' updates the server property and calls callbacks."""
        received_data = None

        def callback(latitude, longitude):
            nonlocal received_data
            received_data = {
                "latitude": latitude,
                "longitude": longitude,
            }

        server.on_location_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "latitude": 1.0,
            "longitude": 3.14,
        }
        prop_obj = LocationProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"123-41"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4166960>>".format(server.instance_id),
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
        assert received_data is not None, "Callback for property 'location' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'location'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_location_property_receive_out_of_sync(self, server, mock_connection):
        """Test that receiving a property update for 'location' updates the server property and calls callbacks."""
        received_data = None

        def callback(latitude, longitude):
            nonlocal received_data
            received_data = {
                "latitude": latitude,
                "longitude": longitude,
            }

        server.on_location_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "latitude": 1.0,
            "longitude": 3.14,
        }
        prop_obj = LocationProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4166960>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": "67"},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'location' was called despite out-of-sync version"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for out-of-sync property 'location'."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.OUT_OF_SYNC.value), f"Expected OUT_OF_SYNC return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_location_property_receive_nonsense_payload(self, server, mock_connection):
        """Test that receiving a property update for 'location' updates the server property and calls callbacks."""
        received_data = None

        def callback(latitude, longitude):
            nonlocal received_data
            received_data = {
                "latitude": latitude,
                "longitude": longitude,
            }

        server.on_location_updated(callback)

        # Create and simulate receiving a property update message that has nonsensical payload
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4166960>>".format(server.instance_id),
            payload=b"adsfaf{this is not json}12|false",
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": str(server._property_location.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'location' was called despite bad payload"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for bad payload request."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(
            MethodReturnCode.SERVER_DESERIALIZATION_ERROR.value
        ), f"Expected SERVER_DESERIALIZATION_ERROR return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_location_property_receive_wrong_payload(self, server, mock_connection):
        """Test that receiving a property update for 'location' updates the server property and calls callbacks."""
        received_data = None

        def callback(latitude, longitude):
            nonlocal received_data
            received_data = {
                "latitude": latitude,
                "longitude": longitude,
            }

        server.on_location_updated(callback)

        # Create and simulate receiving a property update message that has nonsensical payload
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4166960>>".format(server.instance_id),
            payload=b'{"wrong_field": 123, "another_wrong": false}',
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": str(server._property_location.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'location' was called despite wrong payload"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for wrong payload request."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(
            MethodReturnCode.SERVER_DESERIALIZATION_ERROR.value
        ), f"Expected SERVER_DESERIALIZATION_ERROR return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_server_current_temperature_property_initialization(self, server, initial_property_values):
        """Test that the current_temperature server property is initialized correctly."""
        assert hasattr(server, "current_temperature"), "Server missing property 'current_temperature'"
        assert server.current_temperature is not None, "Property 'current_temperature' not initialized properly"
        assert server.current_temperature == initial_property_values.current_temperature, "Property 'current_temperature' value does not match expected value"

    def test_current_temperature_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'current_temperature' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_current_temperature_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd43a6fc0>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'current_temperature'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd43a6fc0>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = CurrentTemperatureProperty(temperature_f=initial_property_values.current_temperature)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_current_temperature_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'current_temperature' updates the server property and calls callbacks."""
        received_data = None

        def callback(temperature_f):
            nonlocal received_data
            received_data = {
                "temperature_f": temperature_f,
            }

        server.on_current_temperature_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "temperature_f": 1.0,
        }
        prop_obj = CurrentTemperatureProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"123-41"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd43a6fc0>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_current_temperature.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Read-only property should not update server state
        assert received_data is None, "Read-only property 'current_temperature' should not be updated"

    def test_server_current_condition_property_initialization(self, server, initial_property_values):
        """Test that the current_condition server property is initialized correctly."""
        assert hasattr(server, "current_condition"), "Server missing property 'current_condition'"
        assert server.current_condition is not None, "Property 'current_condition' not initialized properly"
        assert server.current_condition == initial_property_values.current_condition, "Property 'current_condition' value does not match expected value"

    def test_current_condition_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'current_condition' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_current_condition_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd43f8590>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'current_condition'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd43f8590>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.current_condition
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_current_condition_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'current_condition' updates the server property and calls callbacks."""
        received_data = None

        def callback(condition, description):
            nonlocal received_data
            received_data = {
                "condition": condition,
                "description": description,
            }

        server.on_current_condition_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "condition": WeatherCondition.SUNNY,
            "description": "apples",
        }
        prop_obj = CurrentConditionProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"123-41"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd43f8590>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_current_condition.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Read-only property should not update server state
        assert received_data is None, "Read-only property 'current_condition' should not be updated"

    def test_server_daily_forecast_property_initialization(self, server, initial_property_values):
        """Test that the daily_forecast server property is initialized correctly."""
        assert hasattr(server, "daily_forecast"), "Server missing property 'daily_forecast'"
        assert server.daily_forecast is not None, "Property 'daily_forecast' not initialized properly"
        assert server.daily_forecast == initial_property_values.daily_forecast, "Property 'daily_forecast' value does not match expected value"

    def test_daily_forecast_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'daily_forecast' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_daily_forecast_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd4167c20>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'daily_forecast'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd4167c20>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.daily_forecast
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_daily_forecast_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'daily_forecast' updates the server property and calls callbacks."""
        received_data = None

        def callback(monday, tuesday, wednesday):
            nonlocal received_data
            received_data = {
                "monday": monday,
                "tuesday": tuesday,
                "wednesday": wednesday,
            }

        server.on_daily_forecast_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "monday": ForecastForDay(high_temperature=1.0, low_temperature=1.0, condition=WeatherCondition.SUNNY, start_time="example", end_time="example"),
            "tuesday": ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
            "wednesday": ForecastForDay(high_temperature=1.0, low_temperature=1.0, condition=WeatherCondition.SUNNY, start_time="foo", end_time="foo"),
        }
        prop_obj = DailyForecastProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"123-41"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4167c20>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_daily_forecast.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Read-only property should not update server state
        assert received_data is None, "Read-only property 'daily_forecast' should not be updated"

    def test_server_hourly_forecast_property_initialization(self, server, initial_property_values):
        """Test that the hourly_forecast server property is initialized correctly."""
        assert hasattr(server, "hourly_forecast"), "Server missing property 'hourly_forecast'"
        assert server.hourly_forecast is not None, "Property 'hourly_forecast' not initialized properly"
        assert server.hourly_forecast == initial_property_values.hourly_forecast, "Property 'hourly_forecast' value does not match expected value"

    def test_hourly_forecast_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'hourly_forecast' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_hourly_forecast_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd4167e00>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'hourly_forecast'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd4167e00>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = initial_property_values.hourly_forecast
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_hourly_forecast_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'hourly_forecast' updates the server property and calls callbacks."""
        received_data = None

        def callback(hour_0, hour_1, hour_2, hour_3):
            nonlocal received_data
            received_data = {
                "hour_0": hour_0,
                "hour_1": hour_1,
                "hour_2": hour_2,
                "hour_3": hour_3,
            }

        server.on_hourly_forecast_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "hour_0": ForecastForHour(temperature=1.0, starttime=datetime.now(UTC), condition=WeatherCondition.SUNNY),
            "hour_1": ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
            "hour_2": ForecastForHour(temperature=1.0, starttime=datetime.now(UTC), condition=WeatherCondition.SUNNY),
            "hour_3": ForecastForHour(temperature=1.0, starttime=datetime.now(UTC), condition=WeatherCondition.SUNNY),
        }
        prop_obj = HourlyForecastProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"123-41"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4167e00>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            response_topic=response_topic,
            correlation_data=correlation_data,
            content_type="application/json",
            user_properties={"PropertyVersion": str(server._property_hourly_forecast.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        # Read-only property should not update server state
        assert received_data is None, "Read-only property 'hourly_forecast' should not be updated"

    def test_server_current_condition_refresh_interval_property_initialization(self, server, initial_property_values):
        """Test that the current_condition_refresh_interval server property is initialized correctly."""
        assert hasattr(server, "current_condition_refresh_interval"), "Server missing property 'current_condition_refresh_interval'"
        assert server.current_condition_refresh_interval is not None, "Property 'current_condition_refresh_interval' not initialized properly"
        assert (
            server.current_condition_refresh_interval == initial_property_values.current_condition_refresh_interval
        ), "Property 'current_condition_refresh_interval' value does not match expected value"

    def test_current_condition_refresh_interval_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'current_condition_refresh_interval' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_current_condition_refresh_interval_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd41677a0>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'current_condition_refresh_interval'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd41677a0>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = CurrentConditionRefreshIntervalProperty(seconds=initial_property_values.current_condition_refresh_interval)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_current_condition_refresh_interval_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'current_condition_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_current_condition_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "seconds": 2020,
        }
        prop_obj = CurrentConditionRefreshIntervalProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"123-41"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd41677a0>>".format(server.instance_id),
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
        assert received_data is not None, "Callback for property 'current_condition_refresh_interval' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'current_condition_refresh_interval'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_current_condition_refresh_interval_property_receive_out_of_sync(self, server, mock_connection):
        """Test that receiving a property update for 'current_condition_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_current_condition_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "seconds": 2020,
        }
        prop_obj = CurrentConditionRefreshIntervalProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd41677a0>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": "67"},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'current_condition_refresh_interval' was called despite out-of-sync version"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for out-of-sync property 'current_condition_refresh_interval'."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.OUT_OF_SYNC.value), f"Expected OUT_OF_SYNC return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_current_condition_refresh_interval_property_receive_nonsense_payload(self, server, mock_connection):
        """Test that receiving a property update for 'current_condition_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_current_condition_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message that has nonsensical payload
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd41677a0>>".format(server.instance_id),
            payload=b"adsfaf{this is not json}12|false",
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": str(server._property_current_condition_refresh_interval.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'current_condition_refresh_interval' was called despite bad payload"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for bad payload request."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(
            MethodReturnCode.SERVER_DESERIALIZATION_ERROR.value
        ), f"Expected SERVER_DESERIALIZATION_ERROR return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_current_condition_refresh_interval_property_receive_wrong_payload(self, server, mock_connection):
        """Test that receiving a property update for 'current_condition_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_current_condition_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message that has nonsensical payload
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd41677a0>>".format(server.instance_id),
            payload=b'{"wrong_field": 123, "another_wrong": false}',
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": str(server._property_current_condition_refresh_interval.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'current_condition_refresh_interval' was called despite wrong payload"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for wrong payload request."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(
            MethodReturnCode.SERVER_DESERIALIZATION_ERROR.value
        ), f"Expected SERVER_DESERIALIZATION_ERROR return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_server_hourly_forecast_refresh_interval_property_initialization(self, server, initial_property_values):
        """Test that the hourly_forecast_refresh_interval server property is initialized correctly."""
        assert hasattr(server, "hourly_forecast_refresh_interval"), "Server missing property 'hourly_forecast_refresh_interval'"
        assert server.hourly_forecast_refresh_interval is not None, "Property 'hourly_forecast_refresh_interval' not initialized properly"
        assert server.hourly_forecast_refresh_interval == initial_property_values.hourly_forecast_refresh_interval, "Property 'hourly_forecast_refresh_interval' value does not match expected value"

    def test_hourly_forecast_refresh_interval_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'hourly_forecast_refresh_interval' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_hourly_forecast_refresh_interval_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd4167d40>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'hourly_forecast_refresh_interval'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd4167d40>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = HourlyForecastRefreshIntervalProperty(seconds=initial_property_values.hourly_forecast_refresh_interval)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_hourly_forecast_refresh_interval_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'hourly_forecast_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_hourly_forecast_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "seconds": 2020,
        }
        prop_obj = HourlyForecastRefreshIntervalProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"123-41"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4167d40>>".format(server.instance_id),
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
        assert received_data is not None, "Callback for property 'hourly_forecast_refresh_interval' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'hourly_forecast_refresh_interval'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_hourly_forecast_refresh_interval_property_receive_out_of_sync(self, server, mock_connection):
        """Test that receiving a property update for 'hourly_forecast_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_hourly_forecast_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "seconds": 2020,
        }
        prop_obj = HourlyForecastRefreshIntervalProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4167d40>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": "67"},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'hourly_forecast_refresh_interval' was called despite out-of-sync version"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for out-of-sync property 'hourly_forecast_refresh_interval'."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.OUT_OF_SYNC.value), f"Expected OUT_OF_SYNC return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_hourly_forecast_refresh_interval_property_receive_nonsense_payload(self, server, mock_connection):
        """Test that receiving a property update for 'hourly_forecast_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_hourly_forecast_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message that has nonsensical payload
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4167d40>>".format(server.instance_id),
            payload=b"adsfaf{this is not json}12|false",
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": str(server._property_hourly_forecast_refresh_interval.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'hourly_forecast_refresh_interval' was called despite bad payload"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for bad payload request."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(
            MethodReturnCode.SERVER_DESERIALIZATION_ERROR.value
        ), f"Expected SERVER_DESERIALIZATION_ERROR return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_hourly_forecast_refresh_interval_property_receive_wrong_payload(self, server, mock_connection):
        """Test that receiving a property update for 'hourly_forecast_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_hourly_forecast_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message that has nonsensical payload
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd4167d40>>".format(server.instance_id),
            payload=b'{"wrong_field": 123, "another_wrong": false}',
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": str(server._property_hourly_forecast_refresh_interval.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'hourly_forecast_refresh_interval' was called despite wrong payload"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for wrong payload request."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(
            MethodReturnCode.SERVER_DESERIALIZATION_ERROR.value
        ), f"Expected SERVER_DESERIALIZATION_ERROR return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_server_daily_forecast_refresh_interval_property_initialization(self, server, initial_property_values):
        """Test that the daily_forecast_refresh_interval server property is initialized correctly."""
        assert hasattr(server, "daily_forecast_refresh_interval"), "Server missing property 'daily_forecast_refresh_interval'"
        assert server.daily_forecast_refresh_interval is not None, "Property 'daily_forecast_refresh_interval' not initialized properly"
        assert server.daily_forecast_refresh_interval == initial_property_values.daily_forecast_refresh_interval, "Property 'daily_forecast_refresh_interval' value does not match expected value"

    def test_daily_forecast_refresh_interval_property_publish(self, server, mock_connection, initial_property_values):
        """Test that setting the 'daily_forecast_refresh_interval' property publishes the correct message."""
        mock_connection.clear_published_messages()
        server.publish_daily_forecast_refresh_interval_value()

        published_list = mock_connection.find_published("<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd41b0380>>".format("+"))
        assert len(published_list) == 1, f"No message was published for property 'daily_forecast_refresh_interval'.  Messages: {mock_connection.published_messages}"

        msg = published_list[0]
        expected_topic = "<bound method Property.value_topic of <stingeripc.components.Property object at 0x71dcd41b0380>>".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"

        # Verify payload
        expected_obj = DailyForecastRefreshIntervalProperty(seconds=initial_property_values.daily_forecast_refresh_interval)
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode("utf-8"))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"

    def test_daily_forecast_refresh_interval_property_receive(self, server, mock_connection):
        """Test that receiving a property update for 'daily_forecast_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_daily_forecast_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "seconds": 2020,
        }
        prop_obj = DailyForecastRefreshIntervalProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"123-41"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd41b0380>>".format(server.instance_id),
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
        assert received_data is not None, "Callback for property 'daily_forecast_refresh_interval' was not called"

        # Expect a reply sent back acknowledging the update
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response message was published for property 'daily_forecast_refresh_interval'."
        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.SUCCESS.value), f"Expected SUCCESS return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_daily_forecast_refresh_interval_property_receive_out_of_sync(self, server, mock_connection):
        """Test that receiving a property update for 'daily_forecast_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_daily_forecast_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message
        prop_data = {
            "seconds": 2020,
        }
        prop_obj = DailyForecastRefreshIntervalProperty(**prop_data)  # type: ignore[arg-type]
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd41b0380>>".format(server.instance_id),
            payload=prop_obj.model_dump_json(by_alias=True).encode("utf-8"),
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": "67"},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'daily_forecast_refresh_interval' was called despite out-of-sync version"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for out-of-sync property 'daily_forecast_refresh_interval'."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(MethodReturnCode.OUT_OF_SYNC.value), f"Expected OUT_OF_SYNC return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_daily_forecast_refresh_interval_property_receive_nonsense_payload(self, server, mock_connection):
        """Test that receiving a property update for 'daily_forecast_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_daily_forecast_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message that has nonsensical payload
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd41b0380>>".format(server.instance_id),
            payload=b"adsfaf{this is not json}12|false",
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": str(server._property_daily_forecast_refresh_interval.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'daily_forecast_refresh_interval' was called despite bad payload"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for bad payload request."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(
            MethodReturnCode.SERVER_DESERIALIZATION_ERROR.value
        ), f"Expected SERVER_DESERIALIZATION_ERROR return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"

    def test_daily_forecast_refresh_interval_property_receive_wrong_payload(self, server, mock_connection):
        """Test that receiving a property update for 'daily_forecast_refresh_interval' updates the server property and calls callbacks."""
        received_data = None

        def callback(seconds):
            nonlocal received_data
            received_data = {
                "seconds": seconds,
            }

        server.on_daily_forecast_refresh_interval_updated(callback)

        # Create and simulate receiving a property update message that has nonsensical payload
        response_topic = "client/test/response"
        correlation_data = b"12345-67"
        incoming_msg = Message(
            topic="<bound method Property.update_topic of <stingeripc.components.Property object at 0x71dcd41b0380>>".format(server.instance_id),
            payload=b'{"wrong_field": 123, "another_wrong": false}',
            qos=1,
            retain=False,
            content_type="application/json",
            response_topic=response_topic,
            correlation_data=correlation_data,
            user_properties={"PropertyVersion": str(server._property_daily_forecast_refresh_interval.version)},
        )
        mock_connection.simulate_message(incoming_msg)

        assert received_data is None, "Callback for property 'daily_forecast_refresh_interval' was called despite wrong payload"

        # Check for error message published
        published_list = mock_connection.find_published(response_topic)
        assert len(published_list) == 1, f"No response/error message was published for wrong payload request."

        resp = published_list[0]
        assert resp.user_properties.get("ReturnCode") == str(
            MethodReturnCode.SERVER_DESERIALIZATION_ERROR.value
        ), f"Expected SERVER_DESERIALIZATION_ERROR return code, got '{resp.user_properties.get('ReturnCode')}'"
        assert resp.correlation_data == correlation_data, "Correlation data in response does not match expected value"


class TestWeatherServerSignals:

    def test_server_emit_current_time(self, server, mock_connection):
        """Test that the server can emit the 'current_time' signal."""
        signal_data = {
            "current_time": "apples",
        }  # type: Dict[str, Any]
        server.emit_current_time(**signal_data)

        # Verify that a message was published
        published_list = mock_connection.find_published("<bound method Signal.topic of <stingeripc.components.Signal object at 0x71dcd41673b0>>".format("+"))
        assert len(published_list) == 1, "No message was published for signal 'current_time'"

        msg = published_list[0]
        expected_topic = "<bound method Signal.topic of <stingeripc.components.Signal object at 0x71dcd41673b0>>".format(server.instance_id)
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
