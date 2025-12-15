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
import functools
from concurrent.futures import Future

logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel, ValidationError
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from pyqttier.interface import IBrokerConnection
from pyqttier.message import Message
from .method_codes import *
from .interface_types import *


from .property import SimpleInitialPropertyValues


T = TypeVar("T")


@dataclass
class PropertyControls(Generic[T]):
    value: T
    mutex = threading.RLock()
    version: int = -1
    subscription_id: Optional[int] = None
    callbacks: List[Callable[[T], None]] = field(default_factory=list)

    def get_value(self) -> T:
        with self.mutex:
            return self.value

    def set_value(self, new_value: T) -> T:
        with self.mutex:
            self.value = new_value
            return self.value


@dataclass
class MethodControls:
    subscription_id: Optional[int] = None
    callback: Optional[Callable] = None


class SimpleServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str, initial_property_values: SimpleInitialPropertyValues):
        self._logger = logging.getLogger(f"SimpleServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SimpleServer instance %s", instance_id)
        self._instance_id = instance_id
        self._service_advert_topic = "simple/{}/interface".format(self._instance_id)
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)

        self._property_school: PropertyControls[str] = PropertyControls(value=initial_property_values.school, version=initial_property_values.school_version)
        self._property_school.subscription_id = self._conn.subscribe("simple/{}/property/school/setValue".format(self._instance_id), self._receive_school_update_request_message)

        self._method_trade_numbers = MethodControls()
        self._method_trade_numbers.subscription_id = self._conn.subscribe("simple/{}/method/tradeNumbers".format(self._instance_id), self._process_trade_numbers_call)

        self._publish_all_properties()
        self._logger.debug("Starting interface advertisement thread")
        self._advertise_thread = threading.Thread(target=self._loop_publishing_interface_info, daemon=True)
        self._advertise_thread.start()

    def __del__(self):
        self.shutdown()

    def shutdown(self, timeout: float = 5.0):
        """Gracefully shutdown the server and stop the advertisement thread."""
        if not self._running:
            return
        self._running = False
        self._conn.unpublish_retained(self._service_advert_topic)
        if hasattr(self, "_advertise_thread") and self._advertise_thread.is_alive():
            self._advertise_thread.join(timeout=timeout)

    @property
    def instance_id(self) -> str:
        """The instance ID of this server instance."""
        return self._instance_id

    def _loop_publishing_interface_info(self):
        """We have a discovery topic separate from the MQTT client discovery topic.
        We publish it periodically, but with a Message Expiry interval."""
        while self._running:
            if self._conn.is_connected():
                self.publish_interface_info()
                time_left = self._re_advertise_server_interval_seconds
                while self._running and time_left > 0:
                    sleep(4)
                    time_left -= 4
            else:
                sleep(2)

    def publish_interface_info(self):
        """Publishes the interface info message to the interface info topic with an expiry interval."""
        data = InterfaceInfo(instance=self._instance_id, connection_topic=(self._conn.online_topic or ""), timestamp=datetime.now(UTC).isoformat())
        expiry = int(self._re_advertise_server_interval_seconds * 1.2)  # slightly longer than the re-advertise interval
        topic = self._service_advert_topic
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json(by_alias=True))
        msg = Message.status_message(topic, data, expiry)
        self._conn.publish(msg)

    def _publish_all_properties(self):
        with self._property_school.mutex:
            school_prop_obj = SchoolProperty(name=self._property_school.get_value())
            state_msg = Message.property_state_message("simple/{}/property/school/value".format(self._instance_id), school_prop_obj, self._property_school.version)
            self._conn.publish(state_msg)

    def _receive_school_update_request_message(self, message: Message):
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]

        existing_prop_obj = SchoolProperty(name=self._property_school.get_value())

        try:
            if int(prop_version) != int(self._property_school.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", message.topic, prop_version, self._property_school.version)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_school.version),
                        MethodReturnCode.OUT_OF_SYNC.value,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_school.version}",
                    )
                    self._conn.publish(prop_resp_msg)
                return

            try:
                prop_obj = SchoolProperty.model_validate_json(message.payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", message.topic, e)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic, existing_prop_obj, str(self._property_school.version), MethodReturnCode.CLIENT_DESERIALIZATION_ERROR.value, correlation_id, str(e)
                    )
                    self._conn.publish(prop_resp_msg)
                return
            prop_value = prop_obj.name
            with self._property_school.mutex:
                self._property_school.version += 1
                self._property_school.set_value(prop_value)

                prop_obj = SchoolProperty(name=self._property_school.get_value())

                state_msg = Message.property_state_message("simple/{}/property/school/value".format(self._instance_id), prop_obj, self._property_school.version)
                self._conn.publish(state_msg)

            if response_topic is not None:

                prop_obj = SchoolProperty(name=self._property_school.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_school.version), MethodReturnCode.SUCCESS.value, correlation_id)
                self._conn.publish(prop_resp_msg)
            else:
                self._logger.warning("No response topic provided for property update of %s", message.topic)

            for callback in self._property_school.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", message.topic, exc_info=e)
            if response_topic is not None:
                prop_obj = SchoolProperty(name=self._property_school.get_value())
                prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_school.version), MethodReturnCode.SERVER_ERROR.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)

    def _receive_message(self, message: Message):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message: %s", message)

    def emit_person_entered(self, person: Person):
        """Server application code should call this method to emit the 'person_entered' signal.

        PersonEnteredSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(person, Person), f"The 'person' argument must be of type Person, but was {type(person)}"

        payload = PersonEnteredSignalPayload(
            person=person,
        )
        sig_msg = Message.signal_message("simple/{}/signal/personEntered".format(self._instance_id), payload)
        self._conn.publish(sig_msg)

    def handle_trade_numbers(self, handler: Callable[[int], int]):
        """This is a decorator to decorate a method that will handle the 'trade_numbers' method calls."""
        if self._method_trade_numbers.callback is None and handler is not None:
            self._method_trade_numbers.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_trade_numbers_call(self, message: Message):
        """This processes a call to the 'trade_numbers' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = TradeNumbersMethodRequest.model_validate_json(message.payload)
        correlation_id = message.correlation_data
        response_topic = message.response_topic
        self._logger.debug("Correlation data for 'trade_numbers' request: %s", correlation_id)
        if self._method_trade_numbers.callback is not None:
            method_args = [
                payload.your_number,
            ]  # type: List[Any]

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
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling trade_numbers", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                else:
                    msg = Message.response_message(response_topic, return_json, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    @property
    def school(self) -> Optional[str]:
        """This property returns the last received value for the 'school' property."""
        return self._property_school.get_value()

    @school.setter
    def school(self, name: str):
        """This property sets (publishes) a new value for the 'school' property."""

        if not isinstance(name, str):
            raise ValueError(f"The value must be str .")

        prop_obj = SchoolProperty(name=name)
        payload = prop_obj.model_dump_json(by_alias=True)

        with self._property_school.mutex:
            if name != self._property_school.value:
                self._property_school.value = name
                self._property_school.version += 1
                state_msg = Message.property_state_message("simple/{}/property/school/value".format(self._instance_id), prop_obj, self._property_school.version)
                self._conn.publish(state_msg)
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

            def wrapper(value: SchoolProperty):
                handler(value.name)

            self._property_school.callbacks.append(handler)


class SimpleServerBuilder:
    """
    This is a builder for the SimpleServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):

        self._trade_numbers_method_handler: Optional[Callable[[int], int]] = None

        self._school_property_callbacks: List[Callable[[str], None]] = []

    def handle_trade_numbers(self, handler: Callable[[int], int]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._trade_numbers_method_handler is None and handler is not None:
            self._trade_numbers_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def on_school_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'school' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._school_property_callbacks.append(wrapper)
        return wrapper

    def build(self, connection: IBrokerConnection, instance_id: str, initial_property_values: SimpleInitialPropertyValues, binding: Optional[Any] = None) -> SimpleServer:
        new_server = SimpleServer(connection, instance_id, initial_property_values)

        if self._trade_numbers_method_handler is not None:
            if binding:
                binding_cb = self._trade_numbers_method_handler.__get__(binding, binding.__class__)
                new_server.handle_trade_numbers(binding_cb)
            else:
                new_server.handle_trade_numbers(self._trade_numbers_method_handler)

        for callback in self._school_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_school_updates(binding_cb)
            else:
                new_server.on_school_updates(callback)

        return new_server
