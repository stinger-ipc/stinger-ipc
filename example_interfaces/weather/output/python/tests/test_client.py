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
        discovered_instance=mock_discovery,
    )
    return client


class TestClientInit:
    """Tests for client initialization."""

    def test_client_initializes(self, client):
        """Test that client initializes successfully."""
        assert client is not None, "Client failed to initialize"
        assert client.service_id == "test_instance", "Client service_id does not match expected value"
