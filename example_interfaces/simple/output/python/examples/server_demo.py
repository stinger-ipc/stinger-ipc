from time import sleep
import signal
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from simpleipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from simpleipc.server import SimpleServer, SimpleInitialPropertyValues
from simpleipc.interface_types import *

if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """

    initial_property_values = SimpleInitialPropertyValues(
        school="apples",
    )

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport, client_id="py-server-demo")
    server = SimpleServer(conn, "py-server-demo:1", initial_property_values)

    @server.handle_trade_numbers
    def trade_numbers(your_number: int) -> int:
        """This is an example handler for the 'trade_numbers' method."""
        print(f"--> Running trade_numbers({your_number})'")
        return 42

    @server.on_school_updates
    def on_school_update(name: str):
        """Example callback for when the 'school' property is updated."""
        print(f"~~> Received update for 'school' property: { name= }")

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_person_entered(Person(name="apples", gender=Gender.MALE))

            sleep(4)
            server.emit_person_entered(person=Person(name="apples", gender=Gender.MALE))

            sleep(42)
        except KeyboardInterrupt:
            break

    signal.pause()
