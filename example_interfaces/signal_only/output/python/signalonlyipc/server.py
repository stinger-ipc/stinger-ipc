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
import datetime

logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from connection import BrokerConnection
from method_codes import *
from interface_types import InterfaceInfo
import interface_types as stinger_types


T = TypeVar("T")


@dataclass
class PropertyControls(Generic[T]):
    value: T | None = None
    mutex = threading.Lock()
    version: int = -1
    subscription_id: int | None = None
    callbacks: List[Callable[[T], None]] = field(default_factory=list)


@dataclass
class MethodControls:
    subscription_id: int | None = None
    callback: Optional[Callable] = None


class SignalOnlyServer:

    def __init__(self, connection: BrokerConnection, instance_id: str):
        self._logger = logging.getLogger(f"SignalOnlyServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SignalOnlyServer instance %s", instance_id)
        self._instance_id = instance_id
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.set_message_callback(self._receive_message)

        self._advertise_thread = threading.Thread(target=self.loop_publishing_interface_info)
        self._advertise_thread.start()

    def __del__(self):
        self._running = False
        self._conn.unpublish_retained(self._conn.online_topic)
        self._advertise_thread.join()

    def prepend_topic_prefix(self, topic: str) -> str:
        return f"/{self._instance_id}/{topic}"

    def loop_publishing_interface_info(self):
        while self._conn.is_connected() and self._running:
            self._publish_interface_info()
            sleep(self._re_advertise_server_interval_seconds)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.debug("Received message to %s", topic)

    def _publish_interface_info(self):
        data = InterfaceInfo(instance=self._instance_id, connection_topic=self._conn.online_topic, timestamp=datetime.utcnow().isoformat())
        expiry = int(self._re_advertise_server_interval_seconds * 1.2)  # slightly longer than the re-advertise interval
        self._conn.publish_status(topic, data, expiry)

    def emit_anotherSignal(self, one: float, two: bool, three: str):
        """Server application code should call this method to emit the 'anotherSignal' signal."""
        if not isinstance(one, float):
            raise ValueError(f"The 'one' value must be float.")
        if not isinstance(two, bool):
            raise ValueError(f"The 'two' value must be bool.")
        if not isinstance(three, str):
            raise ValueError(f"The 'three' value must be str.")

        payload = {
            "one": float(one),
            "two": bool(two),
            "three": str(three),
        }
        self._conn.publish("signalOnly/{}/signal/anotherSignal", json.dumps(payload), qos=1, retain=False)

    def emit_bark(self, word: str):
        """Server application code should call this method to emit the 'bark' signal."""
        if not isinstance(word, str):
            raise ValueError(f"The 'word' value must be str.")

        payload = {
            "word": str(word),
        }
        self._conn.publish("signalOnly/{}/signal/bark", json.dumps(payload), qos=1, retain=False)

    def emit_maybe_number(self, number: int | None):
        """Server application code should call this method to emit the 'maybe_number' signal."""
        if not isinstance(number, int | None) and number is not None:
            raise ValueError(f"The 'number' value must be int | None.")

        payload = {
            "number": int | None(number) if number is not None else None,
        }
        self._conn.publish("signalOnly/{}/signal/maybeNumber", json.dumps(payload), qos=1, retain=False)

    def emit_maybe_name(self, name: str | None):
        """Server application code should call this method to emit the 'maybe_name' signal."""
        if not isinstance(name, str | None) and name is not None:
            raise ValueError(f"The 'name' value must be str | None.")

        payload = {
            "name": str | None(name) if name is not None else None,
        }
        self._conn.publish("signalOnly/{}/signal/maybeName", json.dumps(payload), qos=1, retain=False)


class SignalOnlyServerBuilder:
    """
    This is a builder for the SignalOnlyServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self, connection: BrokerConnection):
        self._conn = connection

    def build(self) -> SignalOnlyServer:
        new_server = SignalOnlyServer(self._conn)

        return new_server


if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    import signal
    from connection import MqttBrokerConnection

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    service_id = "1"
    conn = MqttBrokerConnection(transport)
    server = SignalOnlyServer(conn, service_id)

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_anotherSignal(3.14, True, "apples")
            server.emit_bark("apples")
            server.emit_maybe_number(42)
            server.emit_maybe_name("apples")

            sleep(4)
            server.emit_anotherSignal(one=3.14, two=True, three="apples")
            server.emit_bark(word="apples")
            server.emit_maybe_number(number=42)
            server.emit_maybe_name(name="apples")

            sleep(6)
        except KeyboardInterrupt:
            break

    signal.pause()
