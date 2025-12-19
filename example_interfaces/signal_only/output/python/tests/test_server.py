"""
Tests for SignalOnly server.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime, timedelta, UTC

from signal_onlyipc.server import SignalOnlyServer
from signal_onlyipc.interface_types import *
from stinger_python_utils.return_codes import *
from pyqttier.mock import MockConnection
from pyqttier.message import Message
import json
from pydantic import BaseModel
from typing import Any, Dict

def to_jsonified_dict(model: BaseModel) -> Dict[str, Any]:
    """Convert a Pydantic model to a JSON-serializable dict."""
    json_str = model.model_dump_json(by_alias=True)
    return json.loads(json_str)

class SignalOnlyServerSetup:

    def __init__(self):
        self.initial_property_values = self.get_initial_property_values()
         

    def create_server(self, mock_connection) -> SignalOnlyServer:
        server = SignalOnlyServer(
            mock_connection, 
            "test_instance", 
            
        )
        return server 

@pytest.fixture
def server_setup():
    setup = SignalOnlyServerSetup()
    return setup



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

class TestSignalOnlyServer:

    def test_server_initializes(self, server):
        """Test that client initializes successfully."""
        assert server is not None, "server failed to initialize"
        assert server.instance_id == "test_instance", "Server instance_id does not match expected value"

 


class TestSignalOnlyServerSignals:
    
    def test_server_emit_another_signal(self, server, mock_connection):
        """Test that the server can emit the 'another_signal' signal."""
        signal_data = {
            "one": 3.14,
            
            "two": True,
            
            "three": "apples",
            
        } # type: Dict[str, Any]
        server.emit_another_signal(**signal_data)
        
        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/anotherSignal".format('+'))
        assert len(published_list) == 1, "No message was published for signal 'another_signal'"
        
        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/anotherSignal".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"
        
        # Verify payload
        expected_obj = AnotherSignalSignalPayload(**signal_data) # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode('utf-8'))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"
    
    def test_server_emit_bark(self, server, mock_connection):
        """Test that the server can emit the 'bark' signal."""
        signal_data = {
            "word": "apples",
            
        } # type: Dict[str, Any]
        server.emit_bark(**signal_data)
        
        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/bark".format('+'))
        assert len(published_list) == 1, "No message was published for signal 'bark'"
        
        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/bark".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"
        
        # Verify payload
        expected_obj = BarkSignalPayload(**signal_data) # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode('utf-8'))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"
    
    def test_server_emit_maybe_number(self, server, mock_connection):
        """Test that the server can emit the 'maybe_number' signal."""
        signal_data = {
            "number": 42,
            
        } # type: Dict[str, Any]
        server.emit_maybe_number(**signal_data)
        
        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/maybeNumber".format('+'))
        assert len(published_list) == 1, "No message was published for signal 'maybe_number'"
        
        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/maybeNumber".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"
        
        # Verify payload
        expected_obj = MaybeNumberSignalPayload(**signal_data) # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode('utf-8'))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"
    
    def test_server_emit_maybe_name(self, server, mock_connection):
        """Test that the server can emit the 'maybe_name' signal."""
        signal_data = {
            "name": "apples",
            
        } # type: Dict[str, Any]
        server.emit_maybe_name(**signal_data)
        
        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/maybeName".format('+'))
        assert len(published_list) == 1, "No message was published for signal 'maybe_name'"
        
        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/maybeName".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"
        
        # Verify payload
        expected_obj = MaybeNameSignalPayload(**signal_data) # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode('utf-8'))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"
    
    def test_server_emit_now(self, server, mock_connection):
        """Test that the server can emit the 'now' signal."""
        signal_data = {
            "timestamp": datetime.now(UTC),
            
        } # type: Dict[str, Any]
        server.emit_now(**signal_data)
        
        # Verify that a message was published
        published_list = mock_connection.find_published("signalOnly/{}/signal/now".format('+'))
        assert len(published_list) == 1, "No message was published for signal 'now'"
        
        msg = published_list[0]
        expected_topic = "signalOnly/{}/signal/now".format(server.instance_id)
        assert msg.topic == expected_topic, f"Published topic '{msg.topic}' does not match expected '{expected_topic}'"
        
        # Verify payload
        expected_obj = NowSignalPayload(**signal_data) # type: ignore[arg-type]
        expected_dict = to_jsonified_dict(expected_obj)
        payload_dict = json.loads(msg.payload.decode('utf-8'))
        assert payload_dict == expected_dict, f"Published payload '{payload_dict}' does not match expected '{expected_dict}'"
    


