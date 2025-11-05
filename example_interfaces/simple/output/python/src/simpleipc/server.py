"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

import json
import logging
import threading
from time import sleep
from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
import isodate

logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel, ValidationError
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from .connection import IBrokerConnection
from .method_codes import *
from .interface_types import *


T = TypeVar("T")


@dataclass
class PropertyControls(Generic[T]):
    value: T | None = None
    mutex = threading.Lock()
    version: int = -1
    subscription_id: Optional[int] = None
    callbacks: List[Callable[[T], None]] = field(default_factory=list)


@dataclass
class MethodControls:
    subscription_id: Optional[int] = None
    callback: Optional[Callable] = None


class SimpleServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str):
        self._logger = logging.getLogger(f"SimpleServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SimpleServer instance %s", instance_id)
        self._instance_id = instance_id
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)

        self._property_school: PropertyControls[str, str] = PropertyControls()
        self._property_school.subscription_id = self._conn.subscribe("simple/{}/property/school/setValue".format(self._instance_id), self._receive_school_update_request_message)

        self._method_trade_numbers = MethodControls()
        self._method_trade_numbers.subscription_id = self._conn.subscribe("simple/{}/method/tradeNumbers".format(self._instance_id), self._process_trade_numbers_call)

        self._advertise_thread = threading.Thread(target=self.loop_publishing_interface_info)
        self._advertise_thread.start()

    def __del__(self):
        self._running = False
        self._conn.unpublish_retained(self._conn.online_topic)
        self._advertise_thread.join()

    def loop_publishing_interface_info(self):
        while self._conn.is_connected() and self._running:
            self._publish_interface_info()
            sleep(self._re_advertise_server_interval_seconds)

    def _publish_interface_info(self):
        data = InterfaceInfo(instance=self._instance_id, connection_topic=self._conn.online_topic, timestamp=datetime.now(UTC).isoformat())
        expiry = int(self._re_advertise_server_interval_seconds * 1.2)  # slightly longer than the re-advertise interval
        topic = "simple/{}/interface".format(self._instance_id)
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json(by_alias=True))
        self._conn.publish_status(topic, data, expiry)

    def _send_reply_error_message(self, return_code: MethodReturnCode, request_properties: Dict[str, Any], debug_info: Optional[str] = None):
        correlation_id = request_properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = request_properties.get("ResponseTopic")  # type: Optional[str]
        if response_topic is not None:
            self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_info)

    def _receive_school_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = str(payload_obj["name"])
        with self._property_school.mutex:
            self._property_school.value = prop_value
            self._property_school.version += 1
        for callback in self._property_school.callbacks:
            callback(prop_value)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message to %s", topic)

    def emit_person_entered(self, person: Person):
        """Server application code should call this method to emit the 'person_entered' signal.

        PersonEnteredSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(person, Person), f"The 'person' argument must be of type Person, but was {type(person)}"

        payload = PersonEnteredSignalPayload(
            person=person,
        )
        self._conn.publish("simple/{}/signal/personEntered".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def handle_trade_numbers(self, handler: Callable[[int], int]):
        """This is a decorator to decorate a method that will handle the 'trade_numbers' method calls."""
        if self._method_trade_numbers.callback is None and handler is not None:
            self._method_trade_numbers.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_trade_numbers_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'trade_numbers' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = TradeNumbersMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'trade_numbers' request: %s", correlation_id)
        if self._method_trade_numbers.callback is not None:
            method_args = [
                payload.your_number,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_trade_numbers.callback(*method_args)

                    if not isinstance(return_values, int):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type int, but was {type(return_values)}")
                    ret_obj = TradeNumbersMethodResponse(my_number=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling trade_numbers: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling trade_numbers", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    @property
    def school(self) -> Optional[str]:
        """This property returns the last received value for the 'school' property."""
        with self._property_school_mutex:
            return self._property_school

    @school.setter
    def school(self, name: str):
        """This property sets (publishes) a new value for the 'school' property."""

        if not isinstance(name, str):
            raise ValueError(f"The value must be str .")

        prop_obj = SchoolProperty(name=name)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_school.value is None or name != self._property_school.value.name:
            with self._property_school.mutex:
                self._property_school.value = prop_obj
                self._property_school.version += 1
            self._conn.publish("simple/{}/property/school/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_school.callbacks:
                callback(prop_obj.name)

    def set_school(self, name: str):
        """This method sets (publishes) a new value for the 'school' property."""
        if not isinstance(name, str):
            raise ValueError(f"The 'name' value must be str.")

        obj = name

        # Use the property.setter to do that actual work.
        self.school = obj

    def on_school_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'school' property update is received."""
        if handler is not None:
            self._property_school.callbacks.append(handler)


class SimpleServerBuilder:
    """
    This is a builder for the SimpleServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):

        self._trade_numbers_method_handler: Optional[Callable[[int], int]] = None

        self._school_property_callbacks: List[Callable[[str], None]] = []

    def handle_trade_numbers(self, handler: Callable[[int], int]):
        if self._trade_numbers_method_handler is None and handler is not None:
            self._trade_numbers_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def on_school_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'school' property update is received."""
        self._school_property_callbacks.append(handler)

    def build(self, connection: IBrokerConnection) -> SimpleServer:
        new_server = SimpleServer(connection)

        if self._trade_numbers_method_handler is not None:
            new_server.handle_trade_numbers(self._trade_numbers_method_handler)

        for callback in self._school_property_callbacks:
            new_server.on_school_updates(callback)

        return new_server
