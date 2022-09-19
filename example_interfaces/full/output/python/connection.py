
import logging
from typing import Callable, Optional, Tuple
from paho.mqtt import client as mqtt_client
from queue import Queue, Empty
from abc import ABC, abstractmethod
from enum import Enum

logging.basicConfig(level=logging.DEBUG)

class MethodResultCode(Enum):
    SUCCESS = 0
    CLIENT__ERROR = 1
    SERVER__ERROR = 2
    TRANSPORT__ERROR = 3

class BrokerConnection(ABC):
    
    @abstractmethod
    def publish(self, topic, msg, qos=1, retain=False):
        pass

    @abstractmethod
    def subscribe(self, topic):
        pass


class LocalConnection(BrokerConnection):

    def __init__(self):
        self._logger = logging.getLogger('Connection')
        self._logger.setLevel(logging.DEBUG)
        self._host: str = "127.0.0.1"
        self._port: int = 1883
        self._last_will: Optional[Tuple[str, Optional[str], int, bool]] = None
        self._queued_messages = Queue()
        self._queued_subscriptions = Queue()
        self._connected: bool = False
        self._client = mqtt_client.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(self._host, self._port)
        self._message_callback: Optional[Callable[[str, str], None]] = None
        self._client.loop_start()

    def __del__(self):
        if self._last_will is not None:
            self._client.publish(*self._last_will).wait_for_publish()
        self._client.disconnect()
        self._client.loop_stop()

    def set_last_will(self, topic: str, payload: Optional[str]=None, qos: int=1, retain: bool=True):
        self._last_will = (topic, payload, qos, retain)
        self._client.will_set(*self._last_will)

    def set_message_callback(self, callback: Callable[[str, str], None]):
        self._message_callback = callback

    def _on_message(self, client, userdata, msg):
        if self._message_callback:
            self._message_callback(msg.topic, msg.payload.decode())

    def _on_connect(self, client, userdata, flags, rc):
        self._connected = True
        self._logger.info("Connected")
        while not self._queued_subscriptions.empty():
            try:
                topic = self._queued_subscriptions.get_nowait()
            except Empty:
                break
            else:
                self._logger.debug("Connected and subscribing to %s", topic)
                self._client.subscribe(topic)
        while not self._queued_messages.empty():
            try:
                msg = self._queued_messages.get_nowait()
            except Empty:
                break
            else:
                self._logger.info(f"Publishing queued up message")
                self._client.publish(*msg)
        
    
    def publish(self, topic: str, msg: str, qos: int=1, retain: bool=False):
        if self._connected:
            self._logger.info("Publishing %s", topic)
            self._client.publish(topic, msg, qos, retain)
        else:
            self._logger.info("Queueing %s for publishing later", topic)
            self._queued_messages.put((topic, msg, qos, retain))

    def subscribe(self, topic: str):
        if self._connected:
            self._logger.debug("Subscribing to %s", topic)
            self._client.subscribe(topic)
        else:
            self._logger.debug("Pending subscription to %s", topic)
            self._queued_subscriptions.put(topic)
    
    def is_topic_sub(self, topic: str, sub: str) -> bool:
        return mqtt_client.topic_matches_sub(sub, topic)

