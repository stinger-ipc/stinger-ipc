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
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def server(mock_connection):

    initial_property_values = WeatherInitialPropertyValues(
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
    )

    server = WeatherServer(mock_connection, "test_instance", initial_property_values)
    return server


class TestServer:
    """Tests for server initialization."""

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"

    def test_server_properties_initialization(self, server):
        """Test that server properties are initialized correctly."""

        assert hasattr(server, "location"), "Server missing property 'location'"

        assert server.location is not None, "Property 'location' not initialized properly"

        assert hasattr(server, "current_temperature"), "Server missing property 'current_temperature'"

        assert server.current_temperature is not None, "Property 'current_temperature' not initialized properly"

        assert hasattr(server, "current_condition"), "Server missing property 'current_condition'"

        assert server.current_condition is not None, "Property 'current_condition' not initialized properly"

        assert hasattr(server, "daily_forecast"), "Server missing property 'daily_forecast'"

        assert server.daily_forecast is not None, "Property 'daily_forecast' not initialized properly"

        assert hasattr(server, "hourly_forecast"), "Server missing property 'hourly_forecast'"

        assert server.hourly_forecast is not None, "Property 'hourly_forecast' not initialized properly"

        assert hasattr(server, "current_condition_refresh_interval"), "Server missing property 'current_condition_refresh_interval'"

        assert server.current_condition_refresh_interval is not None, "Property 'current_condition_refresh_interval' not initialized properly"

        assert hasattr(server, "hourly_forecast_refresh_interval"), "Server missing property 'hourly_forecast_refresh_interval'"

        assert server.hourly_forecast_refresh_interval is not None, "Property 'hourly_forecast_refresh_interval' not initialized properly"

        assert hasattr(server, "daily_forecast_refresh_interval"), "Server missing property 'daily_forecast_refresh_interval'"

        assert server.daily_forecast_refresh_interval is not None, "Property 'daily_forecast_refresh_interval' not initialized properly"
