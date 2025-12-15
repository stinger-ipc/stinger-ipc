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
from pyqttier.mock import MockConnection
import json


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
def server(mock_connection, initial_property_values):
    server = WeatherServer(mock_connection, "test_instance", initial_property_values)
    yield server
    server.shutdown(timeout=0.1)


class TestServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"


class TestServerProperties:

    def test_server_location_property_initialization(self, server, initial_property_values):
        """Test that the location server property is initialized correctly."""
        assert hasattr(server, "location"), "Server missing property 'location'"
        assert server.location is not None, "Property 'location' not initialized properly"
        assert server.location == initial_property_values.location, "Property 'location' value does not match expected value"

    def test_server_current_temperature_property_initialization(self, server, initial_property_values):
        """Test that the current_temperature server property is initialized correctly."""
        assert hasattr(server, "current_temperature"), "Server missing property 'current_temperature'"
        assert server.current_temperature is not None, "Property 'current_temperature' not initialized properly"
        assert server.current_temperature == initial_property_values.current_temperature, "Property 'current_temperature' value does not match expected value"

    def test_server_current_condition_property_initialization(self, server, initial_property_values):
        """Test that the current_condition server property is initialized correctly."""
        assert hasattr(server, "current_condition"), "Server missing property 'current_condition'"
        assert server.current_condition is not None, "Property 'current_condition' not initialized properly"
        assert server.current_condition == initial_property_values.current_condition, "Property 'current_condition' value does not match expected value"

    def test_server_daily_forecast_property_initialization(self, server, initial_property_values):
        """Test that the daily_forecast server property is initialized correctly."""
        assert hasattr(server, "daily_forecast"), "Server missing property 'daily_forecast'"
        assert server.daily_forecast is not None, "Property 'daily_forecast' not initialized properly"
        assert server.daily_forecast == initial_property_values.daily_forecast, "Property 'daily_forecast' value does not match expected value"

    def test_server_hourly_forecast_property_initialization(self, server, initial_property_values):
        """Test that the hourly_forecast server property is initialized correctly."""
        assert hasattr(server, "hourly_forecast"), "Server missing property 'hourly_forecast'"
        assert server.hourly_forecast is not None, "Property 'hourly_forecast' not initialized properly"
        assert server.hourly_forecast == initial_property_values.hourly_forecast, "Property 'hourly_forecast' value does not match expected value"

    def test_server_current_condition_refresh_interval_property_initialization(self, server, initial_property_values):
        """Test that the current_condition_refresh_interval server property is initialized correctly."""
        assert hasattr(server, "current_condition_refresh_interval"), "Server missing property 'current_condition_refresh_interval'"
        assert server.current_condition_refresh_interval is not None, "Property 'current_condition_refresh_interval' not initialized properly"
        assert (
            server.current_condition_refresh_interval == initial_property_values.current_condition_refresh_interval
        ), "Property 'current_condition_refresh_interval' value does not match expected value"

    def test_server_hourly_forecast_refresh_interval_property_initialization(self, server, initial_property_values):
        """Test that the hourly_forecast_refresh_interval server property is initialized correctly."""
        assert hasattr(server, "hourly_forecast_refresh_interval"), "Server missing property 'hourly_forecast_refresh_interval'"
        assert server.hourly_forecast_refresh_interval is not None, "Property 'hourly_forecast_refresh_interval' not initialized properly"
        assert server.hourly_forecast_refresh_interval == initial_property_values.hourly_forecast_refresh_interval, "Property 'hourly_forecast_refresh_interval' value does not match expected value"

    def test_server_daily_forecast_refresh_interval_property_initialization(self, server, initial_property_values):
        """Test that the daily_forecast_refresh_interval server property is initialized correctly."""
        assert hasattr(server, "daily_forecast_refresh_interval"), "Server missing property 'daily_forecast_refresh_interval'"
        assert server.daily_forecast_refresh_interval is not None, "Property 'daily_forecast_refresh_interval' not initialized properly"
        assert server.daily_forecast_refresh_interval == initial_property_values.daily_forecast_refresh_interval, "Property 'daily_forecast_refresh_interval' value does not match expected value"
