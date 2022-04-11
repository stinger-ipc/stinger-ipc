from typing import Callable
from paho.mqtt import client as mqtt_client
from queue import Queue, Empty

class Connection:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._queued_messages = Queue()
        self._connected = False
        self._client = mqtt_client.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(self._host, self._port)
        self._message_callback = None

    def set_message_callback(self, callback: Callable[[str, str], None]):
        self._message_callback = callback

    def _on_message(self, client, userdata, msg):
        if self._message_callback:
            self._message_callback(msg.topic, msg.payload.decode())

    def _on_connect(self, client, userdata, flags, rc):
        self._connected = True
        while not self._queued_messages.empty():
            try:
                msg = self._queued_messages.get_nowait()
            except Empty:
                break
            else:
                self._client.publish(*msg)
    
    def publish(self, topic, msg, qos=1, retain=False):
        if self._connected:
            self._client.publish(topic, msg, qos, retain)
        else:
            self._queued_messages.push((topic, msg, qos, retain))

    def subscribe(self, topic):
        self._client.subscribe(topic)
    
    def is_topic_sub(self, topic, sub) -> bool:
        return topic == sub