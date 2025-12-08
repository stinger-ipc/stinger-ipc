import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from pyqttier import Mqtt5Connection, MqttTransportType, MqttTransport
from signalonlyipc.client import SignalOnlyClient, SignalOnlyClientBuilder, SignalOnlyClientDiscoverer
from signalonlyipc.interface_types import *
import threading


if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = Mqtt5Connection(transport)

    client_builder = SignalOnlyClientBuilder()

    @client_builder.receive_another_signal
    def print_anotherSignal_receipt(one: float, two: bool, three: str):
        """
        @param one float
        @param two bool
        @param three str
        """
        print(f"Got a 'anotherSignal' signal: one={ one} two={ two} three={ three} ")

    @client_builder.receive_bark
    def print_bark_receipt(word: str):
        """
        @param word str
        """
        print(f"Got a 'bark' signal: word={ word} ")

    @client_builder.receive_maybe_number
    def print_maybe_number_receipt(number: Optional[int]):
        """
        @param number Optional[int]
        """
        print(f"Got a 'maybe_number' signal: number={ number} ")

    @client_builder.receive_maybe_name
    def print_maybe_name_receipt(name: Optional[str]):
        """
        @param name Optional[str]
        """
        print(f"Got a 'maybe_name' signal: name={ name} ")

    @client_builder.receive_now
    def print_now_receipt(timestamp: datetime):
        """
        @param timestamp datetime
        """
        print(f"Got a 'now' signal: timestamp={ timestamp} ")

    discovery = SignalOnlyClientDiscoverer(conn, client_builder)
    fut_client = discovery.get_singleton_client()
    try:
        client = fut_client.result(10)
    except futures.TimeoutError:
        print("Timed out waiting for a service to appear")
        exit(1)

    sleep(2)

    print("Ctrl-C will stop the program.")
    signal.pause()
