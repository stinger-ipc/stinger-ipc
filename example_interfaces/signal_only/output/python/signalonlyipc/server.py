"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.
"""

import json
import logging
import threading
from time import sleep
from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
import isodate

logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from connection import IBrokerConnection
from method_codes import *
from interface_types import *
import interface_types as stinger_types


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
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json())
        self._conn.publish_status(topic, data, expiry)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message to %s", topic)

    def emit_another_signal(self, one: float, two: bool, three: str):
        """Server application code should call this method to emit the 'anotherSignal' signal.

        AnotherSignalSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = AnotherSignalSignalPayload(
            one=one,
            two=two,
            three=three,
        )
        self._conn.publish("signalOnly/{}/signal/anotherSignal".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_bark(self, word: str):
        """Server application code should call this method to emit the 'bark' signal.

        BarkSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = BarkSignalPayload(
            word=word,
        )
        self._conn.publish("signalOnly/{}/signal/bark".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_maybe_number(self, number: Optional[int]):
        """Server application code should call this method to emit the 'maybe_number' signal.

        MaybeNumberSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = MaybeNumberSignalPayload(
            number=number if number is not None else None,
        )
        self._conn.publish("signalOnly/{}/signal/maybeNumber".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_maybe_name(self, name: Optional[str]):
        """Server application code should call this method to emit the 'maybe_name' signal.

        MaybeNameSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = MaybeNameSignalPayload(
            name=name if name is not None else None,
        )
        self._conn.publish("signalOnly/{}/signal/maybeName".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)

    def emit_now(self, timestamp: datetime):
        """Server application code should call this method to emit the 'now' signal.

        NowSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        payload = NowSignalPayload(
            timestamp=timestamp,
        )
        self._conn.publish("signalOnly/{}/signal/now".format(self._instance_id), payload.model_dump_json(), qos=1, retain=False)


class SignalOnlyServerBuilder:
    """
    This is a builder for the SignalOnlyServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):
        pass

    def build(self, connection: IBrokerConnection) -> SignalOnlyServer:
        new_server = SignalOnlyServer(connection)

        return new_server


if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    import signal
    from connection import MqttBrokerConnection, MqttTransport, MqttTransportType

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport)
    server = SignalOnlyServer(conn, "demo")

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_another_signal(3.14, True, "apples")
            server.emit_bark("apples")
            server.emit_maybe_number(42)
            server.emit_maybe_name("apples")
            server.emit_now(datetime.now())

            sleep(4)
            server.emit_another_signal(one=3.14, two=True, three="apples")
            server.emit_bark(word="apples")
            server.emit_maybe_number(number=42)
            server.emit_maybe_name(name="apples")
            server.emit_now(timestamp=datetime.now())

            sleep(6)
        except KeyboardInterrupt:
            break

    signal.pause()
