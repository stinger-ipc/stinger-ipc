from time import sleep
import signal
from typing import Optional, Union
from datetime import datetime, timedelta
from fullipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from fullipc.server import FullServer
from fullipc import interface_types

if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport, client_id="py-server-demo")
    server = FullServer(conn, "py-server-demo:1")

    server.favorite_number = 42

    server.favorite_foods = interface_types.FavoriteFoodsProperty(
        drink="apples",
        slices_of_pizza=42,
        breakfast="apples",
    )

    server.lunch_menu = interface_types.LunchMenuProperty(
        monday=interface_types.Lunch(
            drink=True, sandwich="apples", crackers=3.14, day=interface_types.DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(), duration_of_lunch=timedelta(seconds=3536)
        ),
        tuesday=interface_types.Lunch(
            drink=True, sandwich="apples", crackers=3.14, day=interface_types.DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(), duration_of_lunch=timedelta(seconds=3536)
        ),
    )

    server.family_name = "apples"

    server.last_breakfast_time = datetime.now()

    server.breakfast_length = timedelta(seconds=3536)

    server.last_birthdays = interface_types.LastBirthdaysProperty(
        mom=datetime.now(),
        dad=datetime.now(),
        sister=datetime.now(),
        brothers_age=42,
    )

    @server.handle_add_numbers
    def add_numbers(first: int, second: int, third: Optional[int]) -> int:
        """This is an example handler for the 'addNumbers' method."""
        print(f"Running add_numbers'({first}, {second}, {third})'")
        return 42

    @server.handle_do_something
    def do_something(aString: str) -> interface_types.DoSomethingMethodResponse:
        """This is an example handler for the 'doSomething' method."""
        print(f"Running do_something'({aString})'")
        return interface_types.DoSomethingMethodResponse(label="apples", identifier=42, day=interface_types.DayOfTheWeek.SATURDAY)

    @server.handle_echo
    def echo(message: str) -> str:
        """This is an example handler for the 'echo' method."""
        print(f"Running echo'({message})'")
        return "apples"

    @server.handle_what_time_is_it
    def what_time_is_it(the_first_time: datetime) -> datetime:
        """This is an example handler for the 'what_time_is_it' method."""
        print(f"Running what_time_is_it'({the_first_time})'")
        return datetime.now()

    @server.handle_set_the_time
    def set_the_time(the_first_time: datetime, the_second_time: datetime) -> interface_types.SetTheTimeMethodResponse:
        """This is an example handler for the 'set_the_time' method."""
        print(f"Running set_the_time'({the_first_time}, {the_second_time})'")
        return interface_types.SetTheTimeMethodResponse(timestamp=datetime.now(), confirmation_message="apples")

    @server.handle_forward_time
    def forward_time(adjustment: timedelta) -> datetime:
        """This is an example handler for the 'forward_time' method."""
        print(f"Running forward_time'({adjustment})'")
        return datetime.now()

    @server.handle_how_off_is_the_clock
    def how_off_is_the_clock(actual_time: datetime) -> timedelta:
        """This is an example handler for the 'how_off_is_the_clock' method."""
        print(f"Running how_off_is_the_clock'({actual_time})'")
        return timedelta(seconds=3536)

    @server.on_favorite_number_updates
    def on_favorite_number_update(number: int):
        print(f"Received update for 'favorite_number' property: { number= }")

    @server.on_favorite_foods_updates
    def on_favorite_foods_update(drink: str, slices_of_pizza: int, breakfast: Optional[str]):
        print(f"Received update for 'favorite_foods' property: { drink= }, { slices_of_pizza= }, { breakfast= }")

    @server.on_lunch_menu_updates
    def on_lunch_menu_update(monday: interface_types.Lunch, tuesday: interface_types.Lunch):
        print(f"Received update for 'lunch_menu' property: { monday= }, { tuesday= }")

    @server.on_family_name_updates
    def on_family_name_update(family_name: str):
        print(f"Received update for 'family_name' property: { family_name= }")

    @server.on_last_breakfast_time_updates
    def on_last_breakfast_time_update(timestamp: datetime):
        print(f"Received update for 'last_breakfast_time' property: { timestamp= }")

    @server.on_breakfast_length_updates
    def on_breakfast_length_update(length: timedelta):
        print(f"Received update for 'breakfast_length' property: { length= }")

    @server.on_last_birthdays_updates
    def on_last_birthdays_update(mom: datetime, dad: datetime, sister: Optional[datetime], brothers_age: Optional[int]):
        print(f"Received update for 'last_birthdays' property: { mom= }, { dad= }, { sister= }, { brothers_age= }")

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_today_is(42, interface_types.DayOfTheWeek.SATURDAY, datetime.now(), timedelta(seconds=3536), b"example binary data")

            sleep(4)
            server.emit_today_is(dayOfMonth=42, dayOfWeek=interface_types.DayOfTheWeek.SATURDAY, timestamp=datetime.now(), process_time=timedelta(seconds=3536), memory_segment=b"example binary data")

            sleep(16)
        except KeyboardInterrupt:
            break

    signal.pause()
