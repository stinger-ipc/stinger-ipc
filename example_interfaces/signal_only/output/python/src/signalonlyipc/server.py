"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.

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
    value: T
    mutex = threading.Lock()
    version: int = -1
    subscription_id: Optional[int] = None
    callbacks: List[Callable[[T], None]] = field(default_factory=list)


@dataclass
class MethodControls:
    subscription_id: Optional[int] = None
    callback: Optional[Callable] = None


class SignalOnlyServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str):
        self._logger = logging.getLogger(f"SignalOnlyServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SignalOnlyServer instance %s", instance_id)
        self._instance_id = instance_id
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)

        self._publish_all_properties()
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
        topic = "signalOnly/{}/interface".format(self._instance_id)
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json(by_alias=True))
        self._conn.publish_status(topic, data, expiry)

    def _send_reply_error_message(self, return_code: MethodReturnCode, request_properties: Dict[str, Any], debug_info: Optional[str] = None):
        correlation_id = request_properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = request_properties.get("ResponseTopic")  # type: Optional[str]
        if response_topic is not None:
            self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_info)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message to %s", topic)

    def emit_another_signal(self, one: float, two: bool, three: str):
        """Server application code should call this method to emit the 'anotherSignal' signal.

        AnotherSignalSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(one, float), f"The 'one' argument must be of type float, but was {type(one)}"

        assert isinstance(two, bool), f"The 'two' argument must be of type bool, but was {type(two)}"

        assert isinstance(three, str), f"The 'three' argument must be of type str, but was {type(three)}"

        payload = AnotherSignalSignalPayload(
            one=one,
            two=two,
            three=three,
        )
        self._conn.publish("signalOnly/{}/signal/anotherSignal".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_bark(self, word: str):
        """Server application code should call this method to emit the 'bark' signal.

        BarkSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(word, str), f"The 'word' argument must be of type str, but was {type(word)}"

        payload = BarkSignalPayload(
            word=word,
        )
        self._conn.publish("signalOnly/{}/signal/bark".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_maybe_number(self, number: Optional[int]):
        """Server application code should call this method to emit the 'maybe_number' signal.

        MaybeNumberSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(number, int) or number is None, f"The 'number' argument must be of type Optional[int], but was {type(number)}"

        payload = MaybeNumberSignalPayload(
            number=number if number is not None else None,
        )
        self._conn.publish("signalOnly/{}/signal/maybeNumber".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_maybe_name(self, name: Optional[str]):
        """Server application code should call this method to emit the 'maybe_name' signal.

        MaybeNameSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(name, str) or name is None, f"The 'name' argument must be of type Optional[str], but was {type(name)}"

        payload = MaybeNameSignalPayload(
            name=name if name is not None else None,
        )
        self._conn.publish("signalOnly/{}/signal/maybeName".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

    def emit_now(self, timestamp: datetime):
        """Server application code should call this method to emit the 'now' signal.

        NowSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(timestamp, datetime), f"The 'timestamp' argument must be of type datetime, but was {type(timestamp)}"

        payload = NowSignalPayload(
            timestamp=timestamp,
        )
        self._conn.publish("signalOnly/{}/signal/now".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)


class SignalOnlyServerBuilder:
    """
    This is a builder for the SignalOnlyServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):
        pass

    def build(self, connection: IBrokerConnection, instance_id: str) -> SignalOnlyServer:
        new_server = SignalOnlyServer(connection, instance_id)

        return new_server
