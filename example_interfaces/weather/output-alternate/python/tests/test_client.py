"""
Tests for weather client.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

from weatheripc.client import WeatherClient, DiscoveredInstance
from weatheripc.property import WeatherInitialPropertyValues
from weatheripc.interface_types import *
from pyqttier.mock import MockConnection
import json
from typing import Dict, Any


def to_jsonified_dict(model: BaseModel) -> Dict[str, Any]:
    """Convert a Pydantic model to a JSON-serializable dict."""
    json_str = model.model_dump_json(by_alias=True)
    return json.loads(json_str)


@pytest.fixture
def initial_property_values():
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


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def client(mock_connection, initial_property_values):
    """Fixture providing a weather client with mocked connection."""
    mock_discovery = DiscoveredInstance(
        instance_id="test_instance",
        initial_property_values=initial_property_values,
    )
    client = WeatherClient(
        connection=mock_connection,
        instance_info=mock_discovery,
    )
    return client


class TestClient:
    """Tests for client initialization."""

    def test_client_initializes(self, client):
        """Test that client initializes successfully."""
        assert client is not None, "Client failed to initialize"
        assert client.service_id == "test_instance", "Client service_id does not match expected value"


class TestClientProperties:

    def test_client_properties_initialization(self, client, initial_property_values):
        """Test that client properties are initialized correctly."""

        assert hasattr(client, "location"), "Client missing property 'location'"
        assert client.location is not None, "Property 'location' not initialized properly"
        assert client.location == initial_property_values.location, "Property 'location' value does not match expected value"

        assert hasattr(client, "current_temperature"), "Client missing property 'current_temperature'"
        assert client.current_temperature is not None, "Property 'current_temperature' not initialized properly"
        assert client.current_temperature == initial_property_values.current_temperature, "Property 'current_temperature' value does not match expected value"

        assert hasattr(client, "current_condition"), "Client missing property 'current_condition'"
        assert client.current_condition is not None, "Property 'current_condition' not initialized properly"
        assert client.current_condition == initial_property_values.current_condition, "Property 'current_condition' value does not match expected value"

        assert hasattr(client, "daily_forecast"), "Client missing property 'daily_forecast'"
        assert client.daily_forecast is not None, "Property 'daily_forecast' not initialized properly"
        assert client.daily_forecast == initial_property_values.daily_forecast, "Property 'daily_forecast' value does not match expected value"

        assert hasattr(client, "hourly_forecast"), "Client missing property 'hourly_forecast'"
        assert client.hourly_forecast is not None, "Property 'hourly_forecast' not initialized properly"
        assert client.hourly_forecast == initial_property_values.hourly_forecast, "Property 'hourly_forecast' value does not match expected value"

        assert hasattr(client, "current_condition_refresh_interval"), "Client missing property 'current_condition_refresh_interval'"
        assert client.current_condition_refresh_interval is not None, "Property 'current_condition_refresh_interval' not initialized properly"
        assert (
            client.current_condition_refresh_interval == initial_property_values.current_condition_refresh_interval
        ), "Property 'current_condition_refresh_interval' value does not match expected value"

        assert hasattr(client, "hourly_forecast_refresh_interval"), "Client missing property 'hourly_forecast_refresh_interval'"
        assert client.hourly_forecast_refresh_interval is not None, "Property 'hourly_forecast_refresh_interval' not initialized properly"
        assert client.hourly_forecast_refresh_interval == initial_property_values.hourly_forecast_refresh_interval, "Property 'hourly_forecast_refresh_interval' value does not match expected value"

        assert hasattr(client, "daily_forecast_refresh_interval"), "Client missing property 'daily_forecast_refresh_interval'"
        assert client.daily_forecast_refresh_interval is not None, "Property 'daily_forecast_refresh_interval' not initialized properly"
        assert client.daily_forecast_refresh_interval == initial_property_values.daily_forecast_refresh_interval, "Property 'daily_forecast_refresh_interval' value does not match expected value"


class TestClientMethods:

    def test_refresh_daily_forecast_method_call_sends_request(self, mock_connection, client):
        kwargs = {}  # type: Dict[str, Any]
        client.refresh_daily_forecast(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'refresh_daily_forecast' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/refreshDailyForecast"), f"Incorrect topic for 'refresh_daily_forecast' method call: {message.topic}"

    def test_refresh_hourly_forecast_method_call_sends_request(self, mock_connection, client):
        kwargs = {}  # type: Dict[str, Any]
        client.refresh_hourly_forecast(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'refresh_hourly_forecast' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/refreshHourlyForecast"), f"Incorrect topic for 'refresh_hourly_forecast' method call: {message.topic}"

    def test_refresh_current_conditions_method_call_sends_request(self, mock_connection, client):
        kwargs = {}  # type: Dict[str, Any]
        client.refresh_current_conditions(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'refresh_current_conditions' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/refreshCurrentConditions"), f"Incorrect topic for 'refresh_current_conditions' method call: {message.topic}"
