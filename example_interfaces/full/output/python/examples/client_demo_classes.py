import signal
from time import sleep
import concurrent.futures as futures
from typing import Optional, Union, List
from datetime import datetime, timedelta, UTC
from fullipc.connection import MqttBrokerConnection, MqttTransport, MqttTransportType
from fullipc.client import FullClient, FullClientBuilder, FullClientDiscoverer
from fullipc.interface_types import *
import threading

client_builder = FullClientBuilder()

class SuperAwesomeDoerOfThings:

    def __init__(self, label: str, connection: MqttBrokerConnection):
        self.counter = 0
        self.label = label
        discovery = FullClientDiscoverer(connection, client_builder, build_binding=self) # The build binding will bind all @client_builder decorated methods to this instance.
        self.client = discovery.get_singleton_client().result()
        threading.Thread(target=self.request_loop, daemon=True).start()

    
    @client_builder.receive_today_is
    def print_todayIs_signal(self, *args, **kwargs):
        self.counter += 1
        print(f"{self.label}-{self.counter} printing signal 'todayIs' : args={args}, kwargs={kwargs}")
    

    
    @client_builder.favorite_number_updated
    def print_new_favorite_number_value(self, value: int):
        print(f"{self.label}-{self.counter} printing signal 'favorite_number' : value={value}")
    
    @client_builder.favorite_foods_updated
    def print_new_favorite_foods_value(self, value: FavoriteFoodsProperty):
        print(f"{self.label}-{self.counter} printing signal 'favorite_foods' : value={value}")
    
    @client_builder.lunch_menu_updated
    def print_new_lunch_menu_value(self, value: LunchMenuProperty):
        print(f"{self.label}-{self.counter} printing signal 'lunch_menu' : value={value}")
    
    @client_builder.family_name_updated
    def print_new_family_name_value(self, value: str):
        print(f"{self.label}-{self.counter} printing signal 'family_name' : value={value}")
    
    @client_builder.last_breakfast_time_updated
    def print_new_last_breakfast_time_value(self, value: datetime):
        print(f"{self.label}-{self.counter} printing signal 'last_breakfast_time' : value={value}")
    
    @client_builder.breakfast_length_updated
    def print_new_breakfast_length_value(self, value: timedelta):
        print(f"{self.label}-{self.counter} printing signal 'breakfast_length' : value={value}")
    
    @client_builder.last_birthdays_updated
    def print_new_last_birthdays_value(self, value: LastBirthdaysProperty):
        print(f"{self.label}-{self.counter} printing signal 'last_birthdays' : value={value}")
    

    
    def request_loop(self):
        """Example request loop that runs in a separate thread."""
        sleep(30)
        while True:
            print("Making call to 'add_numbers'")
            future_resp = self.client.add_numbers(first=42, second=42, third=42)
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'add_numbers' call")
            sleep(5)
            
            print("Making call to 'do_something'")
            future_resp = self.client.do_something(a_string="apples")
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'do_something' call")
            sleep(5)
            
            print("Making call to 'echo'")
            future_resp = self.client.echo(message="apples")
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'echo' call")
            sleep(5)
            
            print("Making call to 'what_time_is_it'")
            future_resp = self.client.what_time_is_it(the_first_time=datetime.now(UTC))
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'what_time_is_it' call")
            sleep(5)
            
            print("Making call to 'set_the_time'")
            future_resp = self.client.set_the_time(the_first_time=datetime.now(UTC), the_second_time=datetime.now(UTC))
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'set_the_time' call")
            sleep(5)
            
            print("Making call to 'forward_time'")
            future_resp = self.client.forward_time(adjustment=timedelta(seconds=3536))
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'forward_time' call")
            sleep(5)
            
            print("Making call to 'how_off_is_the_clock'")
            future_resp = self.client.how_off_is_the_clock(actual_time=datetime.now(UTC))
            try:
                print(f"RESULT:  {future_resp.result(5)}")
            except futures.TimeoutError:
                print(f"Timed out waiting for response to 'how_off_is_the_clock' call")
            sleep(5)
            
            
            
            self.client.favorite_number = 42
             
            
            
            self.client.favorite_foods = FavoriteFoodsProperty(
                drink="apples",
                slices_of_pizza=42,
                breakfast="apples",
            )
             
            
            
            self.client.lunch_menu = LunchMenuProperty(
                monday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
                tuesday=Lunch(drink=True, sandwich="apples", crackers=3.14, day=DayOfTheWeek.SATURDAY, order_number=42, time_of_lunch=datetime.now(UTC), duration_of_lunch=timedelta(seconds=3536)),
            )
             
            
            
            self.client.family_name = "apples"
             
            
            
            self.client.last_breakfast_time = datetime.now(UTC)
             
            
            
            self.client.breakfast_length = timedelta(seconds=3536)
             
            
            
            self.client.last_birthdays = LastBirthdaysProperty(
                mom=datetime.now(UTC),
                dad=datetime.now(UTC),
                sister=datetime.now(UTC),
                brothers_age=42,
            )
             
             
            sleep(10)
     

if __name__ == '__main__':

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport)

    doer1 = SuperAwesomeDoerOfThings("Doer1", conn)    

    print("Ctrl-C will stop the program.")
    signal.pause()