"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

from typing import Dict, Callable, List, Any, Optional
from uuid import uuid4
from functools import partial
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

logging.basicConfig(level=logging.DEBUG)

PersonEnteredSignalCallbackType = Callable[[Person], None]
TradeNumbersMethodResponseCallbackType = Callable[[int], None]

SchoolPropertyUpdatedCallbackType = Callable[[str], None]


class SimpleClient:

    def __init__(self, connection: IBrokerConnection, service_instance_id: str):
        """Constructor for a `SimpleClient` object."""
        self._logger = logging.getLogger("SimpleClient")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SimpleClient")
        self._conn = connection
        self._conn.add_message_callback(self._receive_message)
        self._service_id = service_instance_id

        self._pending_method_responses: dict[str, Callable[..., None]] = {}

        self._property_school = None  # type: Optional[str]
        self._property_school_mutex = threading.Lock()
        self._property_school_version = -1
        self._conn.subscribe("simple/{}/property/school/value".format(self._service_id), self._receive_school_property_update_message)
        self._changed_value_callbacks_for_school: list[SchoolPropertyUpdatedCallbackType] = []
        self._signal_recv_callbacks_for_person_entered: list[PersonEnteredSignalCallbackType] = []
        self._conn.subscribe(f"client/{self._conn.client_id}/trade_numbers/response", self._receive_trade_numbers_response_message)

    @property
    def school(self) -> Optional[str]:
        """Property 'school' getter."""
        return self._property_school

    @school.setter
    def school(self, value: str):
        """Serializes and publishes the 'school' property."""
        if not isinstance(value, str):
            raise ValueError("The 'school' property must be a str")
        serialized = json.dumps({"name": value.name})
        self._logger.debug("Setting 'school' property to %s", serialized)
        self._conn.publish("simple/{}/property/school/setValue".format(self._service_id), serialized, qos=1)

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

    def _receive_trade_numbers_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'trade_numbers' method response.
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

    def _receive_school_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'school' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'school' property change with non-JSON content type")
            return
        try:
            prop_obj = SchoolProperty.model_validate_json(payload)
            with self._property_school_mutex:
                self._property_school = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_school_version:
                        self._property_school_version = int(ver)

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
        self._conn.publish(
            "simple/{}/method/tradeNumbers".format(self._service_id),
            json_payload,
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/trade_numbers/response",
        )
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
        self._signal_recv_callbacks_for_person_entered.append(handler)

    def school_updated(self, handler: SchoolPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_school.append(handler)

    def build(self, broker: IBrokerConnection, service_instance_id: str) -> SimpleClient:
        """Builds a new SimpleClient."""
        self._logger.debug("Building SimpleClient for service instance %s", service_instance_id)
        client = SimpleClient(broker, service_instance_id)

        for cb in self._signal_recv_callbacks_for_person_entered:
            client.receive_person_entered(cb)

        for cb in self._property_updated_callbacks_for_school:
            client.school_changed(cb)

        return client


class SimpleClientDiscoverer:

    def __init__(self, connection: IBrokerConnection, builder: Optional[SimpleClientBuilder] = None):
        """Creates a new SimpleClientDiscoverer."""
        self._conn = connection
        self._builder = builder
        self._logger = logging.getLogger("SimpleClientDiscoverer")
        self._logger.setLevel(logging.DEBUG)
        service_discovery_topic = "simple/{}/interface".format("+")
        self._conn.subscribe(service_discovery_topic, self._process_service_discovery_message)
        self._mutex = threading.Lock()
        self._discovered_services: Dict[str, InterfaceInfo] = {}
        self._discovered_service_callbacks: List[Callable[[InterfaceInfo], None]] = []
        self._pending_futures: List[futures.Future] = []
        self._removed_service_callbacks: List[Callable[[str], None]] = []

    def add_discovered_service_callback(self, callback: Callable[[InterfaceInfo], None]):
        """Adds a callback to be called when a new service is discovered."""
        with self._mutex:
            self._discovered_service_callbacks.append(callback)

    def add_removed_service_callback(self, callback: Callable[[str], None]):
        """Adds a callback to be called when a service is removed."""
        with self._mutex:
            self._removed_service_callbacks.append(callback)

    def get_service_instance_ids(self) -> List[str]:
        """Returns a list of currently discovered service instance IDs."""
        with self._mutex:
            return list(self._discovered_services.keys())

    def get_singleton_client(self) -> futures.Future[SimpleClient]:
        """Returns a SimpleClient for the single discovered service.
        Raises an exception if there is not exactly one discovered service.
        """
        fut = futures.Future()
        with self._mutex:
            if len(self._discovered_services) > 0:
                service_instance_id = next(iter(self._discovered_services))
                if self._builder is None:
                    fut.set_result(SimpleClient(self._conn, service_instance_id))
                else:
                    new_client = self._builder.build(self._conn, service_instance_id)
                    fut.set_result(new_client)
            else:
                self._pending_futures.append(fut)
        return fut

    def _process_service_discovery_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """Processes a service discovery message."""
        self._logger.debug("Processing service discovery message on topic %s", topic)
        if len(payload) > 0:
            try:
                service_info = InterfaceInfo.model_validate_json(payload)
            except Exception as e:
                self._logger.warning("Failed to process service discovery message: %s", e)
            with self._mutex:
                self._discovered_services[service_info.instance] = service_info
                while self._pending_futures:
                    fut = self._pending_futures.pop(0)
                    if not fut.done():
                        if self._builder is not None:
                            fut.set_result(self._builder.build(self._conn, service_info.instance))
                        else:
                            fut.set_result(SimpleClient(self._conn, service_info.instance))
                if not service_info.instance in self._discovered_services:
                    self._logger.info("Discovered service: %s.instance", service_info.instance)
                    for cb in self._discovered_service_callbacks:
                        cb(service_info)
                else:
                    self._logger.debug("Updated info for service: %s", service_info.instance)
        else:  # Empty payload means the service is going away
            instance_id = topic.split("/")[-2]
            with self._mutex:
                if instance_id in self._discovered_services:
                    self._logger.info("Service %s is going away", instance_id)
                    del self._discovered_services[instance_id]
                    for cb in self._removed_service_callbacks:
                        cb(instance_id)
