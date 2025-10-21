from time import sleep
import signal
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from signalonlyipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from signalonlyipc.server import SignalOnlyServer
from signalonlyipc.interface_types import *

if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport, client_id="py-server-demo")
    server = SignalOnlyServer(conn, "py-server-demo:1")

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_another_signal(3.14, True, "apples")
            server.emit_bark("apples")
            server.emit_maybe_number(42)
            server.emit_maybe_name("apples")
            server.emit_now(datetime.now(UTC))

            sleep(4)
            server.emit_another_signal(one=3.14, two=True, three="apples")
            server.emit_bark(word="apples")
            server.emit_maybe_number(number=42)
            server.emit_maybe_name(name="apples")
            server.emit_now(timestamp=datetime.now(UTC))

            sleep(16)
        except KeyboardInterrupt:
            break

    signal.pause()
