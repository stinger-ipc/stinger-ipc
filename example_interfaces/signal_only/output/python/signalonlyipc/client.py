"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
"""

from typing import Dict, Callable, List, Any
from uuid import uuid4
from functools import partial
import json
import logging

from connection import BrokerConnection


logging.basicConfig(level=logging.DEBUG)

AnotherSignalSignalCallbackType = Callable[[float, bool, str], None]
BarkSignalCallbackType = Callable[[str], None]
MaybeNumberSignalCallbackType = Callable[[int | None], None]
MaybeNameSignalCallbackType = Callable[[str | None], None]
NowSignalCallbackType = Callable[[datetime.datetime], None]


class SignalOnlyClient:

    def __init__(self, connection: BrokerConnection):
        """Constructor for a `SignalOnlyClient` object."""
        self._logger = logging.getLogger("SignalOnlyClient")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SignalOnlyClient")
        self._client_id = str(uuid4())
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)

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

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.debug("Receiving message sent to %s", topic)
        # Handle 'anotherSignal' signal.
        if self._conn.is_topic_sub(topic, "signalOnly/signal/anotherSignal"):
            if "ContentType" not in properties or properties["ContentType"] != "application/json":
                self._logger.warning("Received 'anotherSignal' signal with non-JSON content type")
                return
            allowed_args = [
                "one",
                "two",
                "three",
            ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)
            kwargs["one"] = float(kwargs["one"])
            kwargs["two"] = bool(kwargs["two"])
            kwargs["three"] = str(kwargs["three"])

            self._do_callbacks_for(self._signal_recv_callbacks_for_another_signal, **kwargs)
        # Handle 'bark' signal.
        elif self._conn.is_topic_sub(topic, "signalOnly/signal/bark"):
            if "ContentType" not in properties or properties["ContentType"] != "application/json":
                self._logger.warning("Received 'bark' signal with non-JSON content type")
                return
            allowed_args = [
                "word",
            ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)
            kwargs["word"] = str(kwargs["word"])

            self._do_callbacks_for(self._signal_recv_callbacks_for_bark, **kwargs)
        # Handle 'maybe_number' signal.
        elif self._conn.is_topic_sub(topic, "signalOnly/signal/maybeNumber"):
            if "ContentType" not in properties or properties["ContentType"] != "application/json":
                self._logger.warning("Received 'maybe_number' signal with non-JSON content type")
                return
            allowed_args = [
                "number",
            ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)
            kwargs["number"] = int | None(kwargs["number"]) if kwargs.get("number") else None

            self._do_callbacks_for(self._signal_recv_callbacks_for_maybe_number, **kwargs)
        # Handle 'maybe_name' signal.
        elif self._conn.is_topic_sub(topic, "signalOnly/signal/maybeName"):
            if "ContentType" not in properties or properties["ContentType"] != "application/json":
                self._logger.warning("Received 'maybe_name' signal with non-JSON content type")
                return
            allowed_args = [
                "name",
            ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)
            kwargs["name"] = str | None(kwargs["name"]) if kwargs.get("name") else None

            self._do_callbacks_for(self._signal_recv_callbacks_for_maybe_name, **kwargs)
        # Handle 'now' signal.
        elif self._conn.is_topic_sub(topic, "signalOnly/signal/now"):
            if "ContentType" not in properties or properties["ContentType"] != "application/json":
                self._logger.warning("Received 'now' signal with non-JSON content type")
                return
            allowed_args = [
                "timestamp",
            ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)
            kwargs["timestamp"] = datetime.datetime(kwargs["timestamp"])

            self._do_callbacks_for(self._signal_recv_callbacks_for_now, **kwargs)

    def receive_another_signal(self, handler: AnotherSignalSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_another_signal.append(handler)
        if len(self._signal_recv_callbacks_for_another_signal) == 1:
            self._conn.subscribe("signalOnly/signal/anotherSignal")
        return handler

    def receive_bark(self, handler: BarkSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_bark.append(handler)
        if len(self._signal_recv_callbacks_for_bark) == 1:
            self._conn.subscribe("signalOnly/signal/bark")
        return handler

    def receive_maybe_number(self, handler: MaybeNumberSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_maybe_number.append(handler)
        if len(self._signal_recv_callbacks_for_maybe_number) == 1:
            self._conn.subscribe("signalOnly/signal/maybeNumber")
        return handler

    def receive_maybe_name(self, handler: MaybeNameSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_maybe_name.append(handler)
        if len(self._signal_recv_callbacks_for_maybe_name) == 1:
            self._conn.subscribe("signalOnly/signal/maybeName")
        return handler

    def receive_now(self, handler: NowSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_now.append(handler)
        if len(self._signal_recv_callbacks_for_now) == 1:
            self._conn.subscribe("signalOnly/signal/now")
        return handler


class SignalOnlyClientBuilder:

    def __init__(self, broker: BrokerConnection):
        """Creates a new SignalOnlyClientBuilder."""
        self._conn = broker
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

    def build(self) -> SignalOnlyClient:
        """Builds a new SignalOnlyClient."""
        self._logger.debug("Building SignalOnlyClient")
        client = SignalOnlyClient(self._conn)

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


if __name__ == "__main__":
    import signal

    from connection import DefaultConnection

    conn = DefaultConnection("localhost", 1883)
    client_builder = SignalOnlyClientBuilder(conn)

    @client_builder.receive_another_signal
    def print_anotherSignal_receipt(one: float, two: bool, three: str):
        """
        @param one float
        @param two bool
        @param three str
        """
        print(f"Got a 'anotherSignal' signal: one={ one } two={ two } three={ three } ")

    @client_builder.receive_bark
    def print_bark_receipt(word: str):
        """
        @param word str
        """
        print(f"Got a 'bark' signal: word={ word } ")

    @client_builder.receive_maybe_number
    def print_maybe_number_receipt(number: int | None):
        """
        @param number int | None
        """
        print(f"Got a 'maybe_number' signal: number={ number } ")

    @client_builder.receive_maybe_name
    def print_maybe_name_receipt(name: str | None):
        """
        @param name str | None
        """
        print(f"Got a 'maybe_name' signal: name={ name } ")

    @client_builder.receive_now
    def print_now_receipt(timestamp: datetime.datetime):
        """
        @param timestamp datetime.datetime
        """
        print(f"Got a 'now' signal: timestamp={ timestamp } ")

    client = client_builder.build()

    print("Ctrl-C will stop the program.")
    signal.pause()
