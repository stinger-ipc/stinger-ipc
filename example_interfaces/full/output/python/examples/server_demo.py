from time import sleep
import signal
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from fullipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from fullipc.server import FullServer, FullInitialPropertyValues
from fullipc.interface_types import *

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    
    initial_property_values = FullInitialPropertyValues(
    
        favorite_number=42,
            
        favorite_number_version=1,
    
        favorite_foods=
            FavoriteFoodsProperty(
                
                drink="apples",
                
                slices_of_pizza=42,
                
                breakfast="apples",
                
            ),
        favorite_foods_version=2,
    
        lunch_menu=
            LunchMenuProperty(
                
                monday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
                
                tuesday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
                
            ),
        lunch_menu_version=3,
    
        family_name="apples",
            
        family_name_version=4,
    
        last_breakfast_time=datetime.now(UTC),
            
        last_breakfast_time_version=5,
    
        breakfast_length=timedelta(seconds=3536),
            
        breakfast_length_version=6,
    
        last_birthdays=
            LastBirthdaysProperty(
                
                mom=datetime.now(UTC),
                
                dad=datetime.now(UTC),
                
                sister=datetime.now(UTC),
                
                brothers_age=42,
                
            ),
        last_birthdays_version=7,
    
    )
    

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport, client_id="py-server-demo")
    server = FullServer(conn, "py-server-demo:1", initial_property_values)

    
    @server.handle_add_numbers 
    def add_numbers(first: int, second: int, third: Optional[int]) -> int:
        """ This is an example handler for the 'addNumbers' method.  """
        print(f"--> Running add_numbers({first}, {second}, {third})'")
        return 42
    
    @server.handle_do_something 
    def do_something(aString: str) -> DoSomethingMethodResponse:
        """ This is an example handler for the 'doSomething' method.  """
        print(f"--> Running do_something({aString})'")
        return DoSomethingMethodResponse(label="apples", identifier=42, day=DayOfTheWeek.SATURDAY)
    
    @server.handle_echo 
    def echo(message: str) -> str:
        """ This is an example handler for the 'echo' method.  """
        print(f"--> Running echo({message})'")
        return "apples"
    
    @server.handle_what_time_is_it 
    def what_time_is_it(the_first_time: datetime) -> datetime:
        """ This is an example handler for the 'what_time_is_it' method.  """
        print(f"--> Running what_time_is_it({the_first_time})'")
        return datetime.now(UTC)
    
    @server.handle_set_the_time 
    def set_the_time(the_first_time: datetime, the_second_time: datetime) -> SetTheTimeMethodResponse:
        """ This is an example handler for the 'set_the_time' method.  """
        print(f"--> Running set_the_time({the_first_time}, {the_second_time})'")
        return SetTheTimeMethodResponse(timestamp=datetime.now(UTC), confirmation_message="apples")
    
    @server.handle_forward_time 
    def forward_time(adjustment: timedelta) -> datetime:
        """ This is an example handler for the 'forward_time' method.  """
        print(f"--> Running forward_time({adjustment})'")
        return datetime.now(UTC)
    
    @server.handle_how_off_is_the_clock 
    def how_off_is_the_clock(actual_time: datetime) -> timedelta:
        """ This is an example handler for the 'how_off_is_the_clock' method.  """
        print(f"--> Running how_off_is_the_clock({actual_time})'")
        return timedelta(seconds=3536)
    

    
    @server.on_favorite_number_updates
    def on_favorite_number_update(number: int):
        """ Example callback for when the 'favorite_number' property is updated. """
        print(f"~~> Received update for 'favorite_number' property: { number= }")
    
    @server.on_favorite_foods_updates
    def on_favorite_foods_update(drink: str, slices_of_pizza: int, breakfast: Optional[str]):
        """ Example callback for when the 'favorite_foods' property is updated. """
        print(f"~~> Received update for 'favorite_foods' property: { drink= }, { slices_of_pizza= }, { breakfast= }")
    
    @server.on_lunch_menu_updates
    def on_lunch_menu_update(monday: Lunch, tuesday: Lunch):
        """ Example callback for when the 'lunch_menu' property is updated. """
        print(f"~~> Received update for 'lunch_menu' property: { monday= }, { tuesday= }")
    
    @server.on_family_name_updates
    def on_family_name_update(family_name: str):
        """ Example callback for when the 'family_name' property is updated. """
        print(f"~~> Received update for 'family_name' property: { family_name= }")
    
    @server.on_last_breakfast_time_updates
    def on_last_breakfast_time_update(timestamp: datetime):
        """ Example callback for when the 'last_breakfast_time' property is updated. """
        print(f"~~> Received update for 'last_breakfast_time' property: { timestamp= }")
    
    @server.on_breakfast_length_updates
    def on_breakfast_length_update(length: timedelta):
        """ Example callback for when the 'breakfast_length' property is updated. """
        print(f"~~> Received update for 'breakfast_length' property: { length= }")
    
    @server.on_last_birthdays_updates
    def on_last_birthdays_update(mom: datetime, dad: datetime, sister: Optional[datetime], brothers_age: Optional[int]):
        """ Example callback for when the 'last_birthdays' property is updated. """
        print(f"~~> Received update for 'last_birthdays' property: { mom= }, { dad= }, { sister= }, { brothers_age= }")
    

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_today_is(42, DayOfTheWeek.SATURDAY, datetime.now(UTC), timedelta(seconds=3536), b"example binary data")
            
            sleep(4)
            server.emit_today_is(dayOfMonth=42, dayOfWeek=DayOfTheWeek.SATURDAY, timestamp=datetime.now(UTC), process_time=timedelta(seconds=3536), memory_segment=b"example binary data")
            
            sleep(42)
        except KeyboardInterrupt:
            break

    signal.pause()