from typing import Callable, Optional
from paho.mqtt import client as mqtt_client
from queue import Queue, Empty

class IBrokerConnection:
    pass


class DefaultConnection(IBrokerConnection):

    def __init__(self, host: str, port: int):
        self._host: str = host
        self._port: int = port
        self._queued_messages = Queue()
        self._connected: bool = False
        self._client = mqtt_client.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(self._host, self._port)
        self._message_callback: Optional[Callable[[str, str], None]] = None
        self._client.loop_start()

    def __del__(self):
        self._client.loop_stop()

    def set_message_callback(self, callback: Callable[[str, str], None]):
        self._message_callback = callback

    def _on_message(self, client, userdata, msg):
        if self._message_callback:
            self._message_callback(msg.topic, msg.payload.decode())

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected")
        while not self._queued_messages.empty():
            try:
                msg = self._queued_messages.get_nowait()
            except Empty:
                break
            else:
                print(f"Publishing queued up message")
                self._client.publish(*msg)
        self._connected = True
    
    def publish(self, topic, msg, qos=1, retain=False):
        if self._connected:
            print(f"Publishing {topic}")
            self._client.publish(topic, msg, qos, retain)
        else:
            print(f"Queueing {topic} for publishing later")
            self._queued_messages.put((topic, msg, qos, retain))

    def subscribe(self, topic):
        self._client.subscribe(topic)
    
    def is_topic_sub(self, topic, sub) -> bool:
        return topic == sub

