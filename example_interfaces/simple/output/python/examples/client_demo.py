import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from pyqttier import Mqtt5Connection, MqttTransportType, MqttTransport
from simpleipc.client import SimpleClient, SimpleClientBuilder, SimpleClientDiscoverer
from simpleipc.interface_types import *
import threading


def request_loop(client: SimpleClient):
    """Example request loop that runs in a separate thread."""
    sleep(30)
    while True:
        print("Making call to 'trade_numbers'")
        future_resp = client.trade_numbers(your_number=42)
        try:
            print(f"RESULT:  {future_resp.result(5)}")
        except futures.TimeoutError:
            print(f"Timed out waiting for response to 'trade_numbers' call")
        sleep(5)

        client.school = "apples"

        sleep(10)


if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = Mqtt5Connection(transport)

    client_builder = SimpleClientBuilder()

    @client_builder.receive_person_entered
    def print_person_entered_receipt(person: Person):
        """
        @param person Person
        """
        print(f"Got a 'person_entered' signal: person={ person } ")

    @client_builder.school_updated
    def print_new_school_value(value: str):
        """ """
        print(f"Property 'school' has been updated to: {value}")

    discovery = SimpleClientDiscoverer(conn, client_builder)
    fut_client = discovery.get_singleton_client()
    try:
        client = fut_client.result(10)
    except futures.TimeoutError:
        print("Timed out waiting for a service to appear")
        exit(1)

    sleep(2)

    threading.Thread(target=request_loop, args=(client,), daemon=True).start()

    print("Ctrl-C will stop the program.")
    signal.pause()
