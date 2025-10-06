import logging
import uuid
from typing import Callable, Optional, Tuple, Any, Union, List
from paho.mqtt.client import Client as MqttClient, topic_matches_sub
from paho.mqtt.enums import MQTTProtocolVersion, CallbackAPIVersion
from paho.mqtt.properties import Properties as MqttProperties
from paho.mqtt.packettypes import PacketTypes
from queue import Queue, Empty
from abc import ABC, abstractmethod
from method_codes import *
from enum import StrEnum
from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)

MessageCallback = Callable[[str, str, dict[str, Any]], None]


class IBrokerConnection(ABC):

    @abstractmethod
    def publish(
        self,
        topic: str,
        msg: str,
        qos: int = 1,
        retain: bool = False,
        correlation_id: Union[str, bytes, None] = None,
        response_topic: Optional[str] = None,
        return_value: Optional[MethodReturnCode] = None,
        debug_info: Optional[str] = None,
    ):
        pass

    @abstractmethod
    def subscribe(self, topic: str, callback: Optional[MessageCallback] = None) -> int:
        pass

    @abstractmethod
    def add_message_callback(self, callback: MessageCallback) -> None:
        pass

    @abstractmethod
    def is_topic_sub(self, topic: str, sub: str) -> bool:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass


class MqttTransportType(StrEnum):
    """Defines all the ways to connect to an MQTT broker."""

    TCP = "tcp"
    WEBSOCKET = "websockets"
    UNIX = "unix"


class MqttTransport:
    """Defines the transport parameters for connecting to an MQTT broker."""

    def __init__(
        self,
        transport_type: MqttTransportType,
        host: str | None = None,
        port: int | None = None,
        socket_path: str | None = None,
    ):
        self.transport = transport_type
        self.host_or_path = socket_path if transport_type == MqttTransportType.UNIX else host
        self.port = 0 if transport_type == MqttTransportType.UNIX else (port or 1883)


class MqttBrokerConnection(IBrokerConnection):

    class PendingSubscription:
        def __init__(self, topic: str, subscription_id: int):
            self.topic = topic
            self.subscription_id = subscription_id

    def __init__(self, transport: MqttTransport, client_id: str | None = None):
        self._logger = logging.getLogger("Connection")
        self._logger.setLevel(logging.DEBUG)
        self._transport = transport
        self._client_id = client_id or str(uuid.uuid4())
        self._queued_messages = Queue()  # type: Queue[Tuple[str, str, int, bool, MqttProperties]]
        self._queued_subscriptions = Queue()  # type: Queue[BrokerConnection.PendingSubscription]
        self._connected: bool = False
        lwt_properties = MqttProperties(PacketTypes.PUBLISH)
        lwt_properties.ContentType = "application/json"
        lwt_properties.MessageExpiryInterval = 60 * 60 * 24  # 1 day
        self._lwt = {"topic": self.online_topic, "payload": '{"online":false}', "qos": 1, "retain": True, "properties": lwt_properties}
        self._client = MqttClient(CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5, transport=transport.transport.value, client_id=self._client_id, reconnect_on_failure=True)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.will_set(**self._lwt)
        self._client.connect(self._transport.host_or_path, self._transport.port)
        self._subscription_callbacks: Dict[int, MessageCallback] = dict()
        self._message_callbacks: List[MessageCallback] = []
        self._client.loop_start()
        self._next_subscription_id = 10

    def __del__(self):
        if self._last_will is not None:
            self._client.publish(**self._last_will).wait_for_publish()
        self._client.disconnect()
        self._client.loop_stop()

    @property
    def online_topic(self) -> str:
        return f"client/{self._client_id}/online"

    @property
    def client_id(self) -> str:
        return self._client_id

    def is_connected(self) -> bool:
        return self._connected

    def get_next_subscription_id(self) -> int:
        sub_id = self._next_subscription_id
        self._next_subscription_id += 1
        return sub_id

    def add_message_callback(self, callback: MessageCallback):
        self._message_callbacks.append(callback)

    def _on_message(self, client, userdata, msg):
        self._logger.debug("Got a message to %s", msg.topic)
        properties = msg.properties.__dict__ if hasattr(msg, "properties") else {}
        if "UserProperty" in properties:
            properties["UserProperty"] = dict(properties["UserProperty"])
        if "SubscriptionIdentifier" in properties:
            sub_ids = properties["SubscriptionIdentifier"] if isinstance(properties["SubscriptionIdentifier"], list) else [properties["SubscriptionIdentifier"]]
            for sub_id in sub_ids:
                if sub_id in self._subscription_callbacks:
                    self._subscription_callbacks[sub_id](msg.topic, msg.payload.decode(), properties)
                else:
                    self._logger.info("No callback registered for SubscriptionIdentifier %d", sub_id)
                    for callback in self._message_callbacks:
                        callback(msg.topic, msg.payload.decode(), properties)
        else:
            self._logger.info("No SubscriptionIdentifier in message properties")
            for callback in self._message_callbacks:
                callback(msg.topic, msg.payload.decode(), properties)

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:  # Connection successful
            self._connected = True
            self._logger.info("Connected to %s:%d", self._transport.host_or_path, self._transport.port)
            while not self._queued_subscriptions.empty():
                try:
                    pending_subscr = self._queued_subscriptions.get_nowait()
                except Empty:
                    break
                else:
                    self._logger.debug("Connected and subscribing to %s", pending_subscr.topic)
                    sub_props = MqttProperties(PacketTypes.SUBSCRIBE)
                    sub_props.SubscriptionIdentifier = pending_subscr.subscription_id
                    self._client.subscribe(pending_subscr.topic, qos=1, properties=sub_props)
            while not self._queued_messages.empty():
                try:
                    msg = self._queued_messages.get_nowait()
                except Empty:
                    break
                else:
                    self._logger.info(f"Publishing queued up message")
                    self._client.publish(*msg)
            online_msg = self._lwt.copy()
            online_msg["payload"] = '{"online":true}'
            self._client.publish(**online_msg)
        else:
            self._logger.error("Connection failed with reason code %d", reason_code)
            self._connected = False

    def publish(
        self,
        topic: str,
        msg: str,
        qos: int = 1,
        retain: bool = False,
        correlation_id: Union[str, bytes, None] = None,
        response_topic: Optional[str] = None,
        content_type: str = "application/json",
        expiry_seconds: int | None = None,
        user_properties: dict[str, str] | None = None,
    ):
        """Publish a message to mqtt."""
        properties = MqttProperties(PacketTypes.PUBLISH)
        properties.ContentType = content_type
        if isinstance(correlation_id, str):
            properties.CorrelationData = correlation_id.encode("utf-8")
        elif isinstance(correlation_id, bytes):
            properties.CorrelationData = correlation_id
        if expiry_seconds is not None:
            properties.MessageExpiryInterval = expiry_seconds
        if response_topic is not None:
            properties.ResponseTopic = response_topic
        user_property_list = list(user_properties.items()) if isinstance(user_properties, dict) else []
        if len(user_property_list) > 0:
            properties.UserProperty = user_property_list
        if self._connected:
            self._logger.info("Publishing %s", topic)
            self._client.publish(topic, msg, qos, retain, properties)
        else:
            self._logger.info("Queueing %s for publishing later", topic)
            self._queued_messages.put((topic, msg, qos, retain, properties))

    def publish_status(self, topic, status_message: BaseModel, expiry_seconds: int):
        self.publish(topic, status_message.model_dump_json(), qos=1, retain=True, expiry_seconds=expiry_seconds)

    def publish_error_response(self, topic: str, return_code: MethodReturnCode, correlation_id: Union[str, bytes], debug_info: Optional[str] = None):
        user_props = dict()
        user_props["ReturnCode"] = str(return_code.value)
        if debug_info is not None:
            user_props["DebugInfo"] = debug_info
        self.publish(topic, "{}", qos=1, retain=False, correlation_id=correlation_id, user_properties=user_props)

    def publish_response(self, response_topic: str, response_obj: BaseModel, correlation_id: Union[str, bytes]):
        self.publish(response_topic, response_obj.model_dump_json(), qos=1, retain=False, correlation_id=correlation_id, user_properties={"ReturnCode": str(MethodReturnCode.SUCCESS.value)})

    def publish_property_state(self, topic: str, state_obj: BaseModel, state_version: int | None = None):
        props = dict()
        if state_version is not None:
            props["PropertyVersion"] = str(state_version)
        self.publish(topic, state_obj.model_dump_json(), qos=1, retain=True, user_properties=props)

    def publish_request(self, topic: str, request_obj: BaseModel, response_topic: str, correlation_id: Optional[Union[str, bytes]] = None) -> str:
        if correlation_id is None:
            correlation_id = str(uuid.uuid4())
        self.publish(topic, request_obj.model_dump_json(), qos=1, retain=False, correlation_id=correlation_id, response_topic=response_topic)
        return correlation_id

    def unpublish_retained(self, topic):
        self.publish(topic, None, qos=1, retain=True)

    def subscribe(self, topic: str, callback: Optional[MessageCallback] = None) -> int:
        """Subscribes to a topic. If the connection is not established, the subscription is queued.
        Returns the subscription ID.
        """
        sub_id = self.get_next_subscription_id()
        if self._connected:
            self._logger.debug("Subscribing to %s", topic)
            sub_props = MqttProperties(PacketTypes.SUBSCRIBE)
            sub_props.SubscriptionIdentifier = sub_id
            self._client.subscribe(topic, qos=1, properties=sub_props)
        else:
            self._logger.debug("Pending subscription to %s", topic)
            self._queued_subscriptions.put(self.PendingSubscription(topic, sub_id))
        if callback is not None:
            self._subscription_callbacks[sub_id] = callback
        return sub_id

    def is_topic_sub(self, topic: str, sub: str) -> bool:
        return topic_matches_sub(sub, topic)
