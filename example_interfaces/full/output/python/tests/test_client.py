"""
Tests for Full client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC
from fullipc.client import FullClient, DiscoveredInstance
from fullipc.property import FullInitialPropertyValues
from fullipc.interface_types import *
from pyqttier.mock import MockConnection


@pytest.fixture
def mock_connection():
    """Fixture providing a mock MQTT connection."""
    conn = MockConnection()
    return conn


@pytest.fixture
def client(mock_connection):
    """Fixture providing a Full client with mocked connection."""
    mock_discovery = DiscoveredInstance(
        instance_id="test_instance",
        initial_property_values=FullInitialPropertyValues(
            favorite_number=42,
            favorite_foods=FullFavoriteFoodsProperty(
                drink="apples",
                slices_of_pizza=42,
                breakfast="apples",
            ),
            lunch_menu=FullLunchMenuProperty(
                monday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
                tuesday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
            ),
            family_name="apples",
            last_breakfast_time=datetime.now(UTC),
            last_birthdays=FullLastBirthdaysProperty(
                mom=datetime.now(UTC),
                dad=datetime.now(UTC),
                sister=datetime.now(UTC),
                brothers_age=42,
            ),
        ),
    )
    client = FullClient(
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
