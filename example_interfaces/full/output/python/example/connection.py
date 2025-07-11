
import logging
from typing import Callable, Optional, Tuple, Any, Union
from paho.mqtt.client import Client as MqttClient, topic_matches_sub
from paho.mqtt.enums import MQTTProtocolVersion, CallbackAPIVersion
from paho.mqtt.properties import Properties as MqttProperties
from paho.mqtt.packettypes import PacketTypes
from queue import Queue, Empty
from abc import ABC, abstractmethod
from method_codes import *


logging.basicConfig(level=logging.DEBUG)

MessageCallback = Callable[[str, str, dict[str, Any]], None]

class BrokerConnection(ABC):
    
    @abstractmethod
    def publish(self, topic: str, msg: str, qos: int=1, retain: bool=False,
            correlation_id: Union[str, bytes, None] = None, response_topic: Optional[str] = None,
            return_value: Optional[MethodResultCode] = None, debug_info: Optional[str] = None):
        pass

    @abstractmethod
    def subscribe(self, topic):
        pass

    @abstractmethod
    def set_message_callback(self, callback: MessageCallback) -> None:
        pass

    @abstractmethod
    def is_topic_sub(self, topic: str, sub: str) -> bool:
        pass

    @abstractmethod
    def set_last_will(self, topic: str, payload: Optional[str]=None, qos: int=1, retain: bool=True):
        pass


class LocalConnection(BrokerConnection):

    def __init__(self):
        self._logger = logging.getLogger('Connection')
        self._logger.setLevel(logging.DEBUG)
        self._host: str = "127.0.0.1"
        self._port: int = 1883
        self._last_will: Optional[Tuple[str, Optional[str], int, bool]] = None
        self._queued_messages = Queue() # type: Queue[Tuple[str, str, int, bool, MqttProperties]]
        self._queued_subscriptions = Queue() # type: Queue[str]
        self._connected: bool = False
        self._client = MqttClient(CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(self._host, self._port)
        self._message_callback: Optional[MessageCallback] = None
        self._client.loop_start()

    def __del__(self):
        if self._last_will is not None:
            self._client.publish(*self._last_will).wait_for_publish()
        self._client.disconnect()
        self._client.loop_stop()

    def set_last_will(self, topic: str, payload: Optional[str]=None, qos: int=1, retain: bool=True):
        self._last_will = (topic, payload, qos, retain)
        self._client.will_set(*self._last_will)

    def set_message_callback(self, callback: MessageCallback):
        self._message_callback = callback

    def _on_message(self, client, userdata, msg):
        if self._message_callback:
            properties = msg.properties.__dict__.items() if hasattr(msg, 'properties') else {}
            self._message_callback(msg.topic, msg.payload.decode(), properties)

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:  # Connection successful 
            self._connected = True
            self._logger.info("Connected to %s:%d", self._host, self._port)
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
        else:
            self._logger.error("Connection failed with reason code %d", reason_code)
            self._connected = False
        
    
    def publish(self, topic: str, msg: str, qos: int=1, retain: bool=False,
            correlation_id: Union[str, bytes, None] = None, response_topic: Optional[str] = None,
            return_value: Optional[MethodResultCode] = None, debug_info: Optional[str] = None):
        properties = MqttProperties(PacketTypes.PUBLISH)
        properties.ContentType = "application/json"
        if isinstance(correlation_id, str):
            properties.CorrelationData = correlation_id.encode('utf-8')
        elif isinstance(correlation_id, bytes):
            properties.CorrelationData = correlation_id
        if response_topic is not None:
            properties.ResponseTopic = response_topic
        user_properties = []
        if return_value is not None:
            user_properties.append(("ReturnValue", str(return_value)))
        if debug_info is not None:
            user_properties.append(("DebugInfo", debug_info))
        if len(user_properties) > 0:
            properties.UserProperties = user_properties
        if self._connected:
            self._logger.info("Publishing %s", topic)
            self._client.publish(topic, msg, qos, retain, properties)
        else:
            self._logger.info("Queueing %s for publishing later", topic)
            self._queued_messages.put((topic, msg, qos, retain, properties))

    def subscribe(self, topic: str):
        if self._connected:
            self._logger.debug("Subscribing to %s", topic)
            self._client.subscribe(topic)
        else:
            self._logger.debug("Pending subscription to %s", topic)
            self._queued_subscriptions.put(topic)
    
    def is_topic_sub(self, topic: str, sub: str) -> bool:
        return topic_matches_sub(sub, topic)

