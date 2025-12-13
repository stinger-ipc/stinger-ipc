"""
Tests for weather client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from weatheripc.client import WeatherClient, DiscoveredInstance
from weatheripc.property import WeatherInitialPropertyValues
from weatheripc.interface_types import *
from pyqttier.mock import MockConnection
import json


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def client(mock_connection):
    """Fixture providing a weather client with mocked connection."""
    mock_discovery = DiscoveredInstance(
        instance_id="test_instance",
        initial_property_values=WeatherInitialPropertyValues(
            location=WeatherLocationProperty(
                latitude=3.14,
                longitude=3.14,
            ),
            current_temperature=3.14,
            current_condition=WeatherCurrentConditionProperty(
                condition=WeatherCondition.SNOWY,
                description="apples",
            ),
            daily_forecast=WeatherDailyForecastProperty(
                monday=ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
                tuesday=ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
                wednesday=ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=WeatherCondition.SNOWY, start_time="apples", end_time="apples"),
            ),
            hourly_forecast=WeatherHourlyForecastProperty(
                hour_0=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
                hour_1=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
                hour_2=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
                hour_3=ForecastForHour(temperature=3.14, starttime=datetime.now(UTC), condition=WeatherCondition.SNOWY),
            ),
            current_condition_refresh_interval=42,
            hourly_forecast_refresh_interval=42,
            daily_forecast_refresh_interval=42,
        ),
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

    def test_client_properties_initialization(self, client):
        """Test that client properties are initialized correctly."""

        assert hasattr(client, "location"), "Client missing property 'location'"

        assert client.location is not None, "Property 'location' not initialized properly"

        assert hasattr(client, "current_temperature"), "Client missing property 'current_temperature'"

        assert client.current_temperature is not None, "Property 'current_temperature' not initialized properly"

        assert hasattr(client, "current_condition"), "Client missing property 'current_condition'"

        assert client.current_condition is not None, "Property 'current_condition' not initialized properly"

        assert hasattr(client, "daily_forecast"), "Client missing property 'daily_forecast'"

        assert client.daily_forecast is not None, "Property 'daily_forecast' not initialized properly"

        assert hasattr(client, "hourly_forecast"), "Client missing property 'hourly_forecast'"

        assert client.hourly_forecast is not None, "Property 'hourly_forecast' not initialized properly"

        assert hasattr(client, "current_condition_refresh_interval"), "Client missing property 'current_condition_refresh_interval'"

        assert client.current_condition_refresh_interval is not None, "Property 'current_condition_refresh_interval' not initialized properly"

        assert hasattr(client, "hourly_forecast_refresh_interval"), "Client missing property 'hourly_forecast_refresh_interval'"

        assert client.hourly_forecast_refresh_interval is not None, "Property 'hourly_forecast_refresh_interval' not initialized properly"

        assert hasattr(client, "daily_forecast_refresh_interval"), "Client missing property 'daily_forecast_refresh_interval'"

        assert client.daily_forecast_refresh_interval is not None, "Property 'daily_forecast_refresh_interval' not initialized properly"

    def test_refresh_daily_forecast_method_call_sends_request(self, mock_connection, client):
        kwargs = {}
        client.refresh_daily_forecast(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'refresh_daily_forecast' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/refreshDailyForecast"), "Incorrect topic for 'refresh_daily_forecast' method call: {message.topic}"
        payload = json.loads(message.payload.decode())

    def test_refresh_hourly_forecast_method_call_sends_request(self, mock_connection, client):
        kwargs = {}
        client.refresh_hourly_forecast(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'refresh_hourly_forecast' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/refreshHourlyForecast"), "Incorrect topic for 'refresh_hourly_forecast' method call: {message.topic}"
        payload = json.loads(message.payload.decode())

    def test_refresh_current_conditions_method_call_sends_request(self, mock_connection, client):
        kwargs = {}
        client.refresh_current_conditions(**kwargs)
        assert len(mock_connection.published_messages) == 1, "No message was published for 'refresh_current_conditions' method call"
        message = mock_connection.published_messages[0]
        assert message.topic.endswith("/method/refreshCurrentConditions"), "Incorrect topic for 'refresh_current_conditions' method call: {message.topic}"
        payload = json.loads(message.payload.decode())
