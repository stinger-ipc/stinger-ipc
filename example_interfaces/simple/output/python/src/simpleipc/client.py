"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

from typing import Dict, Callable, List, Any, Optional
from uuid import uuid4
from functools import partial, wraps
import json
import logging
from datetime import datetime, timedelta, UTC
from isodate import parse_duration

import asyncio
import concurrent.futures as futures
from .method_codes import *
from .interface_types import *
import threading

from .connection import IBrokerConnection

from .property import SimpleInitialPropertyValues

from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)

PersonEnteredSignalCallbackType = Callable[[Person], None]
TradeNumbersMethodResponseCallbackType = Callable[[int], None]

SchoolPropertyUpdatedCallbackType = Callable[[str], None]


class DiscoveredInstance(BaseModel):
    instance_id: str
    initial_property_values: SimpleInitialPropertyValues


class SimpleClient:

    def __init__(self, connection: IBrokerConnection, instance_info: DiscoveredInstance):
        """Constructor for a `SimpleClient` object."""
        self._logger = logging.getLogger("SimpleClient")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SimpleClient with %s", instance_info.initial_property_values)
        self._conn = connection
        self._conn.add_message_callback(self._receive_message)
        self._service_id = instance_info.instance_id

        self._pending_method_responses: dict[str, Callable[..., None]] = {}

        self._property_school = instance_info.initial_property_values.school  # type: str
        self._property_school_mutex = threading.Lock()
        self._property_school_version = instance_info.initial_property_values.school_version
        self._conn.subscribe("simple/{}/property/school/value".format(self._service_id), self._receive_school_property_update_message)
        self._changed_value_callbacks_for_school: list[SchoolPropertyUpdatedCallbackType] = []
        self._signal_recv_callbacks_for_person_entered: list[PersonEnteredSignalCallbackType] = []
        self._conn.subscribe(f"client/{self._conn.client_id}/Simple/methodResponse", self._receive_any_method_response_message)

        self._property_response_topic = f"client/{self._conn.client_id}/Simple/propertyUpdateResponse"
        self._conn.subscribe(self._property_response_topic, self._receive_any_property_response_message)

    @property
    def school(self) -> str:
        """Property 'school' getter."""
        with self._property_school_mutex:
            return self._property_school

    @school.setter
    def school(self, value: str):
        """Serializes and publishes the 'school' property."""
        if not isinstance(value, str):
            raise ValueError("The 'school' property must be a str")
        property_obj = SchoolProperty(name=value)
        self._logger.debug("Setting 'school' property to %s", property_obj)
        with self._property_school_mutex:
            self._conn.publish_property_update_request("simple/{}/property/school/setValue".format(self._service_id), property_obj, str(self._property_school_version), self._property_response_topic)

    def school_changed(self, handler: SchoolPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'school' property changes.
        Can be used as a decorator.
        """
        with self._property_school_mutex:
            self._changed_value_callbacks_for_school.append(handler)
            if call_immediately and self._property_school is not None:
                handler(self._property_school)
        return handler

    def _do_callbacks_for(self, callbacks: List[Callable[..., None]], **kwargs):
        """Call each callback in the callback dictionary with the provided args."""
        for cb in callbacks:
            cb(**kwargs)

    @staticmethod
    def _filter_for_args(args: Dict[str, Any], allowed_args: List[str]) -> Dict[str, Any]:
        """Given a dictionary, reduce the dictionary so that it only has keys in the allowed list."""
        filtered_args = {}
        for k, v in args.items():
            if k in allowed_args:
                filtered_args[k] = v
        return filtered_args

    def _receive_person_entered_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'person_entered' signal with non-JSON content type")
            return

        model = PersonEnteredSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_person_entered, **kwargs)

    def _receive_any_method_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle '' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_any_property_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", {})
        return_code = user_properties.get("ReturnCode")
        if return_code is not None and int(return_code) != MethodReturnCode.SUCCESS.value:
            debug_info = user_properties.get("DebugInfo", "")
            self._logger.warning("Received error return value %s from property update: %s", return_code, debug_info)

    def _receive_school_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'school' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'school' property change with non-JSON content type")
            return
        try:
            prop_obj = SchoolProperty.model_validate_json(payload)
            user_properties = properties.get("UserProperty", {})
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_school_mutex:
                self._property_school = prop_obj.name
                self._property_school_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_school, value=prop_obj.name)

        except Exception as e:
            self._logger.exception("Error processing 'school' property change: %s", exc_info=e)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.warning("Receiving message sent to %s, but without a handler", topic)

    def receive_person_entered(self, handler: PersonEnteredSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_person_entered.append(handler)
        if len(self._signal_recv_callbacks_for_person_entered) == 1:
            self._conn.subscribe("simple/{}/signal/personEntered".format(self._service_id), self._receive_person_entered_signal_message)
        return handler

    def trade_numbers(self, your_number: int) -> futures.Future:
        """Calling this initiates a `trade_numbers` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_trade_numbers_response, fut)
        payload = TradeNumbersMethodRequest(
            your_number=your_number,
        )
        json_payload = payload.model_dump_json(by_alias=True)
        self._logger.debug("Calling 'trade_numbers' method with payload %s", json_payload)
        response_topic = f"client/{self._conn.client_id}/Simple/methodResponse"
        self._conn.publish("simple/{}/method/tradeNumbers".format(self._service_id), json_payload, qos=2, retain=False, correlation_id=correlation_id, response_topic=response_topic)
        return fut

    def _handle_trade_numbers_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `trade_numbers` IPC method call."""
        self._logger.debug("Handling trade_numbers response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'trade_numbers' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = TradeNumbersMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'trade_numbers' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.my_number)
        else:
            self._logger.warning("Future for 'trade_numbers' method was already done!")


class SimpleClientBuilder:
    """Using decorators from SimpleClient doesn't work if you are trying to create multiple instances of SimpleClient.
    Instead, use this builder to create a registry of callbacks, and then build clients using the registry.

    When ready to create a SimpleClient instance, call the `build(broker, service_instance_id)` method.
    """

    def __init__(self):
        """Creates a new SimpleClientBuilder."""
        self._logger = logging.getLogger("SimpleClientBuilder")
        self._signal_recv_callbacks_for_person_entered = []  # type: List[PersonEnteredSignalCallbackType]
        self._property_updated_callbacks_for_school: list[SchoolPropertyUpdatedCallbackType] = []

    def receive_person_entered(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_person_entered.append(wrapper)
        return wrapper

    def school_updated(self, handler: SchoolPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_school.append(wrapper)
        return wrapper

    def build(self, broker: IBrokerConnection, instance_info: DiscoveredInstance, binding: Optional[Any] = None) -> SimpleClient:
        """Builds a new SimpleClient."""
        self._logger.debug("Building SimpleClient for service instance %s", instance_info.instance_id)
        client = SimpleClient(broker, instance_info)

        for cb in self._signal_recv_callbacks_for_person_entered:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.receive_person_entered(bound_cb)
            else:
                client.receive_person_entered(cb)

        for cb in self._property_updated_callbacks_for_school:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.school_changed(bound_cb)
            else:
                client.school_changed(cb)

        return client


class SimpleClientDiscoverer:

    def __init__(self, connection: IBrokerConnection, builder: Optional[SimpleClientBuilder] = None, build_binding: Optional[Any] = None):
        """Creates a new SimpleClientDiscoverer."""
        self._conn = connection
        self._builder = builder
        self._build_binding = build_binding
        self._logger = logging.getLogger("SimpleClientDiscoverer")
        self._logger.setLevel(logging.DEBUG)
        service_discovery_topic = "simple/{}/interface".format("+")
        self._conn.subscribe(service_discovery_topic, self._process_service_discovery_message)
        self._conn.subscribe("simple/+/property/+/value", self._process_property_value_message)
        self._mutex = threading.Lock()
        self._pending_futures: List[futures.Future] = []
        self._removed_service_callbacks: List[Callable[[str], None]] = []

        # For partially discovered services
        self._discovered_interface_infos = dict()  # type: Dict[str, InterfaceInfo]
        self._discovered_properties = dict()  # type: Dict[str, Dict[str, Any]]

        # For fully discovered services
        self._discovered_services: Dict[str, DiscoveredInstance] = {}
        self._discovered_service_callbacks: List[Callable[[DiscoveredInstance], None]] = []

    def add_discovered_service_callback(self, callback: Callable[[DiscoveredInstance], None]):
        """Adds a callback to be called when a new service is discovered."""
        with self._mutex:
            for instance in self._discovered_services.values():
                callback(instance)
            self._discovered_service_callbacks.append(callback)

    def add_removed_service_callback(self, callback: Callable[[str], None]):
        """Adds a callback to be called when a service is removed."""
        with self._mutex:
            self._removed_service_callbacks.append(callback)

    def get_service_instance_ids(self) -> List[str]:
        """Returns a list of currently discovered service instance IDs."""
        with self._mutex:
            return list(self._discovered_services.keys())

    def get_discovery_info(self, instance_id: str) -> Optional[DiscoveredInstance]:
        """Returns the DiscoveredInstance for a discovered service instance ID, or None if not found."""
        with self._mutex:
            return self._discovered_services.get(instance_id, None)

    def get_singleton_client(self) -> futures.Future[SimpleClient]:
        """Returns a SimpleClient for the single discovered service.
        Raises an exception if there is not exactly one discovered service.
        """
        fut = futures.Future()  # type: futures.Future[SimpleClient]
        with self._mutex:
            if len(self._discovered_services) > 0:
                instance_info = next(iter(self._discovered_services))
                if self._builder is None:
                    fut.set_result(SimpleClient(self._conn, instance_info))
                else:
                    new_client = self._builder.build(self._conn, instance_info, self._build_binding)
                    fut.set_result(new_client)
            else:
                self._pending_futures.append(fut)
        return fut

    def _check_for_fully_discovered(self, instance_id: str):
        """Checks if all properties have been discovered for the given instance ID."""
        with self._mutex:
            if instance_id in self._discovered_properties and len(self._discovered_properties[instance_id]) == 2 and instance_id in self._discovered_interface_infos:

                entry = DiscoveredInstance(instance_id=instance_id, initial_property_values=SimpleInitialPropertyValues(**self._discovered_properties[instance_id]))
                is_new_entry = not instance_id in self._discovered_services

                self._discovered_services[instance_id] = entry
                while self._pending_futures:
                    self._logger.info("Creating a client object id=%s and returning as future result", instance_id)
                    fut = self._pending_futures.pop(0)
                    if not fut.done():
                        if self._builder is not None:
                            fut.set_result(self._builder.build(self._conn, entry, self._build_binding))
                        else:
                            fut.set_result(SimpleClient(self._conn, entry))
                if is_new_entry:
                    self._logger.info("Discovered service: %s", instance_id)
                    for cb in self._discovered_service_callbacks:
                        cb(entry)
                else:
                    self._logger.debug("Updated info for service: %s", instance_id)

    def _process_service_discovery_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """Processes a service discovery message."""
        self._logger.debug("Processing service discovery message on topic %s", topic)
        if len(payload) > 0:
            try:
                service_info = InterfaceInfo.model_validate_json(payload)
                with self._mutex:
                    self._discovered_interface_infos[service_info.instance] = service_info
            except Exception as e:
                self._logger.warning("Failed to process service discovery message: %s", e)
            self._check_for_fully_discovered(service_info.instance)

        else:  # Empty payload means the service is going away
            instance_id = topic.split("/")[-2]
            with self._mutex:
                if instance_id in self._discovered_services:
                    self._logger.info("Service %s is going away", instance_id)
                    if instance_id in self._discovered_services:
                        del self._discovered_services[instance_id]
                    if instance_id in self._discovered_interface_infos:
                        del self._discovered_interface_infos[instance_id]
                    if instance_id in self._discovered_properties:
                        del self._discovered_properties[instance_id]
                    for cb in self._removed_service_callbacks:
                        cb(instance_id)

    def _process_property_value_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """Processes a property value message for discovery purposes."""
        self._logger.debug("Processing property value message on topic %s", topic)
        instance_id = topic.split("/")[1]
        property_name = topic.split("/")[3]
        user_properties = properties.get("UserProperty", {})
        prop_version = user_properties.get("PropertyVersion", -1)
        try:
            prop_obj = json.loads(payload)
            with self._mutex:
                if instance_id not in self._discovered_properties:
                    self._discovered_properties[instance_id] = dict()

                if property_name == "school":

                    self._discovered_properties[instance_id]["school"] = prop_obj.get("name")

                    self._discovered_properties[instance_id]["school_version"] = prop_version

            self._check_for_fully_discovered(instance_id)

        except Exception as e:
            self._logger.warning("Failed to process property value message: %s", e)
