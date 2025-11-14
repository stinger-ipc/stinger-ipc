import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from simpleipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from simpleipc.client import SimpleClient, SimpleClientBuilder, SimpleClientDiscoverer
from simpleipc.interface_types import *
import threading

client_builder = SimpleClientBuilder()


class SuperAwesomeDoerOfThings:

    def __init__(self, label: str, connection: MqttBrokerConnection):
        self.counter = 0
        self.label = label
        discovery = SimpleClientDiscoverer(connection, client_builder, build_binding=self)  # The build binding will bind all @client_builder decorated methods to this instance.
        self.client = discovery.get_singleton_client().result()
        threading.Thread(target=self.request_loop, daemon=True).start()

    @client_builder.receive_person_entered
    def print_person_entered_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'person_entered' : args={args}, kwargs={kwargs}")

    @client_builder.school_updated
    def print_new_school_value(self, value: str):
        print(f"{self.label}-{self.counter} printing signal 'school' : value={value}")

    def request_loop(self):
        """Example request loop that runs in a separate thread."""
        sleep(30)
        while True:
            print("Making call to 'trade_numbers'")
            future_resp = self.client.trade_numbers(your_number=42)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'trade_numbers' call")
            sleep(5)

            self.client.school = "apples"

            sleep(10)


if __name__ == "__main__":

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport)

    doer1 = SuperAwesomeDoerOfThings("Doer1", conn)

    print("Ctrl-C will stop the program.")
    signal.pause()
