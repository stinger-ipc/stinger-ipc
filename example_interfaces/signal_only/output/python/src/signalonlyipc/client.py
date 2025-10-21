"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
"""

from typing import Dict, Callable, List, Any, Optional
from uuid import uuid4
from functools import partial
import json
import logging
from datetime import datetime, timedelta, UTC
from isodate import parse_duration

from .connection import IBrokerConnection

logging.basicConfig(level=logging.DEBUG)

AnotherSignalSignalCallbackType = Callable[[float, bool, str], None]
BarkSignalCallbackType = Callable[[str], None]
MaybeNumberSignalCallbackType = Callable[[Optional[int]], None]
MaybeNameSignalCallbackType = Callable[[Optional[str]], None]
NowSignalCallbackType = Callable[[datetime], None]


class SignalOnlyClient:

    def __init__(self, connection: IBrokerConnection, service_instance_id: str):
        """Constructor for a `SignalOnlyClient` object."""
        self._logger = logging.getLogger("SignalOnlyClient")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SignalOnlyClient")
        self._conn = connection
        self._conn.add_message_callback(self._receive_message)
        self._service_id = service_instance_id

        self._signal_recv_callbacks_for_another_signal: list[AnotherSignalSignalCallbackType] = []
        self._signal_recv_callbacks_for_bark: list[BarkSignalCallbackType] = []
        self._signal_recv_callbacks_for_maybe_number: list[MaybeNumberSignalCallbackType] = []
        self._signal_recv_callbacks_for_maybe_name: list[MaybeNameSignalCallbackType] = []
        self._signal_recv_callbacks_for_now: list[NowSignalCallbackType] = []

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

    def _receive_another_signal_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'anotherSignal' signal with non-JSON content type")
            return

        model = AnotherSignalSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_another_signal, **kwargs)

    def _receive_bark_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'bark' signal with non-JSON content type")
            return

        model = BarkSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_bark, **kwargs)

    def _receive_maybe_number_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'maybe_number' signal with non-JSON content type")
            return

        model = MaybeNumberSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_maybe_number, **kwargs)

    def _receive_maybe_name_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'maybe_name' signal with non-JSON content type")
            return

        model = MaybeNameSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_maybe_name, **kwargs)

    def _receive_now_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'now' signal with non-JSON content type")
            return

        model = NowSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_now, **kwargs)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.warning("Receiving message sent to %s, but without a handler", topic)

    def receive_another_signal(self, handler: AnotherSignalSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_another_signal.append(handler)
        if len(self._signal_recv_callbacks_for_another_signal) == 1:
            self._conn.subscribe("signalOnly/{}/signal/anotherSignal".format(self._service_id), self._receive_another_signal_signal_message)
        return handler

    def receive_bark(self, handler: BarkSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_bark.append(handler)
        if len(self._signal_recv_callbacks_for_bark) == 1:
            self._conn.subscribe("signalOnly/{}/signal/bark".format(self._service_id), self._receive_bark_signal_message)
        return handler

    def receive_maybe_number(self, handler: MaybeNumberSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_maybe_number.append(handler)
        if len(self._signal_recv_callbacks_for_maybe_number) == 1:
            self._conn.subscribe("signalOnly/{}/signal/maybeNumber".format(self._service_id), self._receive_maybe_number_signal_message)
        return handler

    def receive_maybe_name(self, handler: MaybeNameSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_maybe_name.append(handler)
        if len(self._signal_recv_callbacks_for_maybe_name) == 1:
            self._conn.subscribe("signalOnly/{}/signal/maybeName".format(self._service_id), self._receive_maybe_name_signal_message)
        return handler

    def receive_now(self, handler: NowSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_now.append(handler)
        if len(self._signal_recv_callbacks_for_now) == 1:
            self._conn.subscribe("signalOnly/{}/signal/now".format(self._service_id), self._receive_now_signal_message)
        return handler


class SignalOnlyClientBuilder:
    """Using decorators from SignalOnlyClient doesn't work if you are trying to create multiple instances of SignalOnlyClient.
    Instead, use this builder to create a registry of callbacks, and then build clients using the registry.

    When ready to create a SignalOnlyClient instance, call the `build(broker, service_instance_id)` method.
    """

    def __init__(self):
        """Creates a new SignalOnlyClientBuilder."""
        self._logger = logging.getLogger("SignalOnlyClientBuilder")
        self._signal_recv_callbacks_for_another_signal = []  # type: List[AnotherSignalSignalCallbackType]
        self._signal_recv_callbacks_for_bark = []  # type: List[BarkSignalCallbackType]
        self._signal_recv_callbacks_for_maybe_number = []  # type: List[MaybeNumberSignalCallbackType]
        self._signal_recv_callbacks_for_maybe_name = []  # type: List[MaybeNameSignalCallbackType]
        self._signal_recv_callbacks_for_now = []  # type: List[NowSignalCallbackType]

    def receive_another_signal(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_another_signal.append(handler)

    def receive_bark(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_bark.append(handler)

    def receive_maybe_number(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_maybe_number.append(handler)

    def receive_maybe_name(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_maybe_name.append(handler)

    def receive_now(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_now.append(handler)

    def build(self, broker: IBrokerConnection, service_instance_id: str) -> SignalOnlyClient:
        """Builds a new SignalOnlyClient."""
        self._logger.debug("Building SignalOnlyClient for service instance %s", service_instance_id)
        client = SignalOnlyClient(broker, service_instance_id)

        for cb in self._signal_recv_callbacks_for_another_signal:
            client.receive_another_signal(cb)

        for cb in self._signal_recv_callbacks_for_bark:
            client.receive_bark(cb)

        for cb in self._signal_recv_callbacks_for_maybe_number:
            client.receive_maybe_number(cb)

        for cb in self._signal_recv_callbacks_for_maybe_name:
            client.receive_maybe_name(cb)

        for cb in self._signal_recv_callbacks_for_now:
            client.receive_now(cb)

        return client


class SignalOnlyClientDiscoverer:

    def __init__(self, connection: IBrokerConnection, builder: Optional[SignalOnlyClientBuilder] = None):
        """Creates a new SignalOnlyClientDiscoverer."""
        self._conn = connection
        self._builder = builder
        self._logger = logging.getLogger("SignalOnlyClientDiscoverer")
        self._logger.setLevel(logging.DEBUG)
        service_discovery_topic = "signalOnly/{}/interface".format("+")
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

    def get_singleton_client(self) -> futures.Future[SignalOnlyClient]:
        """Returns a SignalOnlyClient for the single discovered service.
        Raises an exception if there is not exactly one discovered service.
        """
        fut = futures.Future()
        with self._mutex:
            if len(self._discovered_services) > 0:
                service_instance_id = next(iter(self._discovered_services))
                if self._builder is None:
                    fut.set_result(SignalOnlyClient(self._conn, service_instance_id))
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
                            fut.set_result(SignalOnlyClient(self._conn, service_info.instance))
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
