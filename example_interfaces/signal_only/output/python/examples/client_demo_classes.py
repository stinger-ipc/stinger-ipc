import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from pyqttier import Mqtt5Connection, MqttTransportType, MqttTransport
from signalonlyipc.client import SignalOnlyClient, SignalOnlyClientBuilder, SignalOnlyClientDiscoverer
from signalonlyipc.interface_types import *
import threading

client_builder = SignalOnlyClientBuilder()


class SuperAwesomeDoerOfThings:

    def __init__(self, label: str, connection: MqttBrokerConnection):
        self.counter = 0
        self.label = label
        discovery = SignalOnlyClientDiscoverer(connection, client_builder, build_binding=self)  # The build binding will bind all @client_builder decorated methods to this instance.
        self.client = discovery.get_singleton_client().result()
        threading.Thread(target=self.request_loop, daemon=True).start()

    @client_builder.receive_another_signal
    def print_anotherSignal_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'anotherSignal' : args={args}, kwargs={kwargs}")

    @client_builder.receive_bark
    def print_bark_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'bark' : args={args}, kwargs={kwargs}")

    @client_builder.receive_maybe_number
    def print_maybe_number_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'maybe_number' : args={args}, kwargs={kwargs}")

    @client_builder.receive_maybe_name
    def print_maybe_name_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'maybe_name' : args={args}, kwargs={kwargs}")

    @client_builder.receive_now
    def print_now_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'now' : args={args}, kwargs={kwargs}")


if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = Mqtt5Connection(transport)

    doer1 = SuperAwesomeDoerOfThings("Doer1", conn)

    print("Ctrl-C will stop the program.")
    signal.pause()
