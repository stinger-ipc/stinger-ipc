# _Example Interface_ API Overview 

<!--
This is automatically generated documentation.
LICENSE: This generated content is not subject to any license restrictions.
TODO: Get license text from stinger file
--> 
_Example StingerAPI interface which demonstrates many features._


[[_TOC_]]

## Connections

A connection object is a wrapper around an MQTT client and provides specific functionality to support both clients and servers.
Generally, you only need one connection object per daemon/program, as it can support multiple clients and servers.  
For most languages, Stinger-IPC does not require a specific connection object implementation, as long as it implements the required interface.

The application code is responsible for creating and managing the connection object, including connecting to the MQTT broker.

### Connection code Examples

<details>
  <summary>Python MQTT Connection Example</summary>

Rather than including connection code in each generated client and server, Stinger-IPC for Python uses the [PYQTtier](https://pypi.org/project/pyqttier/) library to provide MQTT connection objects.  PYQTtier is a wrapper around the [paho-mqtt](https://pypi.org/project/paho-mqtt/) library and handles serialization, message queuing, and acknowledgments.

```python
from pyqttier import Mqtt5Connection, MqttTransportType, MqttTransport

transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883) # Or: MqttTransport(MqttTransportType.UNIX, socket_path="/path/to/socket")
connection_object = Mqtt5Connection(transport)
```

The `connection_object` will be passed to client and server constructors.

</details>

<details>
  <summary>Rust MQTT Connection Example</summary>

Stinger-IPC instances only require an MQTT connection object that implements the [`stinger_mqtt_trait::Mqtt5PubSub` trait](https://docs.rs/stinger-mqtt-trait/latest/stinger_mqtt_trait/trait.Mqtt5PubSub.html). 

The [MQTTier](https://crates.io/crates/mqttier) crate provides an implementation of the `Mqtt5PubSub` trait, and is shown in this documentation as an example.  MQTTier is a wrapper around the [rumqttc](https://crates.io/crates/rumqttc) crate and handles serialization, message queuing, and acknowledgments.'

Here is an example showing how to create an MQTTier client connection object:

```rust
use mqttier::{MqttierClient, MqttierOptionsBuilder, Connection};

let mqttier_options = MqttierOptionsBuilder::default()
    .connection(Connection::TcpLocalhost(1883))
    .client_id("rust-client-demo".to_string())
    .build().unwrap();
let mut connection_object = MqttierClient::new(mqttier_options).unwrap();
let _ = connection_object.start().await;
```

The `connection_object` will be passed to client and server constructors.

</details>

<details>
  <summary>C++ MQTT Connection Example</summary>

The C++ connection object is a wrapper around the [libmosquitto](https://mosquitto.org/api/files/mosquitto-h.html) C library.  This library only supports TCP and WebSocket connections.  Unix Domain Socket support may be added in the future.

```c++
#include "broker.hpp"

auto connection_object = std::make_shared<MqttBrokerConnection>("localhost", 1883, "daemon-name");
```

The `connection_object` will be passed to client and server constructors.

</details>

## Discovery

Because there may be multiple instances of the same Stinger Interface, a discovery mechanism is provided to find and connect to them.  A discovery class is provided which connects to
the MQTT broker and listens for Stinger Interface announcements.  The discovery class can then provide FullClient client instances.  Additionally, the discovery class
find all the current property values for discovered interfaces in order to initialize the client instance.

### Discovery Code Examples

<details>
  <summary>Python Discovery Example</summary>

```python
from fullipc.client import FullClientDiscoverer

discovery = FullClientDiscoverer(connection_object)

# To get a single client instance (waits until one is found):
client = discovery.get_singleton_client().result()

# To get all currently available client instances (does not wait):
discovered_service_ids = discovery.get_service_instance_ids()
clients = [discovery.get_client_for_instance(service_id) for service_id in discovered_service_ids]
```
</details>

<details>
  <summary>Rust Discovery Example</summary>

```rust
use full_ipc::discovery::FullDiscovery;

let discovered_singleton_info = {
    let service_discovery = FullDiscovery::new(&mut connection_object).await.unwrap();
    service_discovery.get_singleton_instance_info().await // Blocks until a service is discovered.
}
let full_client = FullClient::new(&mut connection_object, &discovered_singleton_info).await;
```

</details>

## Server

A server is a _provider_ of functionality.  It sends signals and handles method calls and owns property values.

When constructing a server instance, a connection object and initial property values must be provided.

### Server Code Examples

<details>
  <summary>Python Server Object Construction</summary>

```python
from fullipc.server import FullServer, FullInitialPropertyValues

# Ideally, you would load these initial property values from a configuration file or database.

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

    last_birthdays=
        LastBirthdaysProperty(
            
            mom=datetime.now(UTC),
            
            dad=datetime.now(UTC),
            
            sister=None,
            
            brothers_age=42,
            
        ),
    last_birthdays_version=6,

)


service_id = "py-server-demo:1" # Can be anything. When there is a single instance of the interface, 'singleton' is often used.
server = FullServer(connection_object, service_id, initial_property_values)
```

The `server` object provides methods for emitting signals and updating properties.  It also allows for decorators to indicate method call handlers.

A full example can be viewed by looking at the `example/server_demo.py` file of the generated code.

When decorating class methods, especially when there might be multiple instances of the class with methods being decorated, the Python implementation provides a `FullClientBuilder`
class to help capture decorated methods and bind them to a specific instance at runtime. Here is an example of how to use it in a class:

```python
from fullipc.client import FullClientBuilder

full_builder = FullClientBuilder()

class MyClass:
    def __init__(self, label: str, connection: MqttBrokerConnection):
        instance_info = ... # Create manually or use discovery to get this
        self.client = full_builder.build(connection_object, instance_info, binding=self) # The binding param binds all decorated methods to the `self` instance.

    @full_builder.receive_a_signal
    def on_a_signal(self, param1: int, param2: str):
        ...
```

A more complete example, including use with the discovery mechanism, can be viewed by looking at the generated `examples/server_demo_classes.py` file.

</details>

<details>
  <summary>Rust Server Struct Creation</summary>

Service code for Rust is only available when using the `server` feature:

```sh
cargo add full_ipc --features=server
```

Here is an example of how to create a server instance:

```rust
use full_ipc::server::FullServer;
use full_ipc::property::FullInitialPropertyValues;

let service_id = String::from("rust-server-demo:1");

let initial_property_values = FullInitialPropertyValues {
    
    favorite_number:42,
    favorite_number_version: 1,
    
    favorite_foods:FavoriteFoodsProperty {
            drink: "apples".to_string(),
            slices_of_pizza: 42,
            breakfast: Some("apples".to_string()),
    },
    favorite_foods_version: 1,
    
    lunch_menu:LunchMenuProperty {
            monday: Lunch {drink: true, sandwich: "apples".to_string(), crackers: 3.14, day: DayOfTheWeek::Saturday, order_number: Some(42), time_of_lunch: chrono::Utc::now(), duration_of_lunch: chrono::Duration::seconds(3536)},
            tuesday: Lunch {drink: true, sandwich: "apples".to_string(), crackers: 3.14, day: DayOfTheWeek::Saturday, order_number: Some(42), time_of_lunch: chrono::Utc::now(), duration_of_lunch: chrono::Duration::seconds(3536)},
    },
    lunch_menu_version: 1,
    
    family_name:"apples".to_string(),
    family_name_version: 1,
    
    last_breakfast_time:chrono::Utc::now(),
    last_breakfast_time_version: 1,
    
    last_birthdays:LastBirthdaysProperty {
            mom: chrono::Utc::now(),
            dad: chrono::Utc::now(),
            sister: Some(chrono::Utc::now()),
            brothers_age: Some(42),
    },
    last_birthdays_version: 1,
    
};


// Create the server object.
let mut server = FullServer::new(connection_object, method_handlers.clone(), service_id, initial_property_values, ).await;


```

Providing method handlers is better described in the [Methods](#methods) section.  

A full example can be viewed by looking at the generated `examples/server_demo.rs` example and can be compiled with `cargo run --example full_server_demo --features=server` in the generated Rust project.

</details>

<details>
  <summary>C++ Server Object Construction</summary>

```c++
// To be written
```

The `server` object provides methods for emitting signals and updating properties.  It also allows for decorators to indicate method call handlers.

A full example can be viewed by looking at the generated `examples/server_main.cpp` file.`

</details>

## Client

A client is a _utilizer_ of functionality.  It receives signals, makes method calls, reads property values, or requests updates to property values.

<details>
  <summary>Rust Client Struct Creation</summary>

The best way to create a client instance is to use the discovery class to find an instance of the service, and then create the client from the discovered instance information.
An example of that is shown in the [Discovery](#discovery) section.  However, if you already know the service instance IDand initial property values, you can create a client directly:

```rust
use full_ipc::client::FullClient;

let instance_info = DiscoveredInstance {
    service_instance_id: String::from("singleton"),
    
    initial_property_values: FullInitialPropertyValues {
        
        favorite_number:42,
        favorite_number_version: 1,
        
        favorite_foods:FavoriteFoodsProperty {
                drink: "apples".to_string(),
                slices_of_pizza: 42,
                breakfast: Some("apples".to_string()),
        },
        favorite_foods_version: 1,
        
        lunch_menu:LunchMenuProperty {
                monday: Lunch {drink: true, sandwich: "apples".to_string(), crackers: 3.14, day: DayOfTheWeek::Saturday, order_number: Some(42), time_of_lunch: chrono::Utc::now(), duration_of_lunch: chrono::Duration::seconds(3536)},
                tuesday: Lunch {drink: true, sandwich: "apples".to_string(), crackers: 3.14, day: DayOfTheWeek::Saturday, order_number: Some(42), time_of_lunch: chrono::Utc::now(), duration_of_lunch: chrono::Duration::seconds(3536)},
        },
        lunch_menu_version: 1,
        
        family_name:"apples".to_string(),
        family_name_version: 1,
        
        last_breakfast_time:chrono::Utc::now(),
        last_breakfast_time_version: 1,
        
        last_birthdays:LastBirthdaysProperty {
                mom: chrono::Utc::now(),
                dad: chrono::Utc::now(),
                sister: Some(chrono::Utc::now()),
                brothers_age: Some(42),
        },
        last_birthdays_version: 1,
        
    },
    
};

let mut full_client = FullClient::new(connection_object.clone(), instance_info).await;
```

A full example can be viewed by looking at the generated `client/examples/client_demo.rs` file.

</details>

<details>
  <summary>Python Client Object Construction</summary>

```python
from fullipc.server import FullServer, FullInitialPropertyValues


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

    last_birthdays=
        LastBirthdaysProperty(
            
            mom=datetime.now(UTC),
            
            dad=datetime.now(UTC),
            
            sister=datetime.now(UTC),
            
            brothers_age=42,
            
        ),
    last_birthdays_version=6,

)


service_instance_id="singleton"
server = FullServer(connection_object, service_instance_id, initial_property_values)
```

A full example can be viewed by looking at the generated `examples/client_main.py` file.

Like the Python client, there is a `FullServerBuilder` class to help capture decorated methods and bind them to a specific instance at runtime.

```python

</details>

<details>
  <summary>C++ Client Object Construction</summary>

A full example can be viewed by looking at the generated `examples/client_main.cpp` file.

</details>

## Logging

Each generated language has different ways of handling logging.  

### Python

Python uses the standard Python `logging` module.  

### Rust

Rust uses the `tracing` crate for logging.

### C++

C++ uses a user-provided logging function.  The function should take two parameters: an integer log level and a string message. 

Log levels are re-used from the `syslog.h` header file, although no other syslog mechanisms are used.  Client and server classes use the logging provided by the `MqttBrokerConnection` object.

<details>
  <summary>Example C++ Log Setup</summary>

```c++
#include <syslog.h>

auto connnection = std::make_shared<MqttBrokerConnection>(...);
connnection->SetLogLevel(LOG_DEBUG);
connnection->SetLogFunction([](int level, const char* msg)
{
    std::cout << "[" << level << "] " << msg << std::endl;
});
```

</details>




## Signals

Signals are messages from a server to clients.

```plantuml
@startuml
Client <<- Server : Signal(Parameters)
@enduml
```

### Signal `todayIs`

_No documentation for this signal_

#### Signal Parameters for `todayIs`

| Name          | Type     |Description|
|---------------|----------|-----------|
|   dayOfMonth  | integer  ||
|   dayOfWeek   |[Enum DayOfTheWeek](#enum-DayOfTheWeek)||

#### Code Examples

<details>
  <summary>Python Client code for receiving 'todayIs' signal</summary>

The `todayIs` signal can be subscribed to by using the client's `receive_today_is` decorator on a callback function. The name of the function does not matter. The function is called any time the signal is received.

```python
@client.receive_today_is
def on_today_is(dayOfMonth: int, dayOfWeek: DayOfTheWeek):
    print(f"Got a 'todayIs' signal: dayOfMonth={ dayOfMonth } dayOfWeek={ dayOfWeek } ")
```

</details>

<details>
  <summary>Python Server code for emitting 'todayIs' signal</summary>

A server can emit a `todayIs` signal simply by calling the server's `emit_today_is` method.

```python
server.emit_today_is(42, DayOfTheWeek.SATURDAY)
```

</details>

<details>
  <summary>Rust Client code for receiving 'todayIs' signal</summary>

A Rust client receives signals through a `tokio::broadcast` channel.  Receiving from the channel returns a `Result<T, RecvError>` object.  

Since receiving a message through the channel blocks, it may be best to put this into a separate async task.

```rust
let mut today_is_signal_rx = client.get_today_is_receiver();
print("Got a 'todayIs' signal: {:?}", today_is_signal_rx.recv().await);
```

</details>

<details>
  <summary>Rust Server code for emitting 'todayIs' signal</summary>

A server can emit a `todayIs` signal simply by calling the server's `emit_today_is` method.

```rust
let publish_result = server.emit_today_is(42, DayOfTheWeek::Saturday).await;
```

The return type is a **Pinned Boxed Future** that resolves to a `Result<(), MethodReturnCode>`.  The future is resolved when the signal is sent (with "publish complete" acknowledgment) or when an error occurs.  If you need to block until the signal is received by the MQTT broker, you can `.await` the future.

</details>

<details>
  <summary>C++ Client code for registering a 'todayIs' signal callback</summary>

A client can register a callback function to be called when a `todayIs` signal is received.  The callback function should take the same parameters as the signal.  In this example, we are using a lambda as the callback function.

```cpp
client.registerTodayIsCallback([](int dayOfMonth, DayOfTheWeek dayOfWeek) {
    std::cout << "dayOfMonth=" <<dayOfMonth << " | " << "dayOfWeek=" <<dayOfTheWeekStrings[static_cast<int>(dayOfWeek)] <<  std::endl;
});
```

</details>

<details>
  <summary>C++ Server code for emitting a 'todayIs' signal</summary>

A `todayIs` signal can be emitted by calling the server's `emitTodayIsSignal` method.  This returns a `std::future` that can be waited on if desired.  The future is resolved when the signal is sent.

```cpp
auto todayIsFuture = server.emitTodayIsSignal(42, DayOfTheWeek::SATURDAY);
todayIsFuture.wait(); // Optional, to block until signal is sent.
```

</details>


### Signal `randomWord`

_No documentation for this signal_

#### Signal Parameters for `randomWord`

| Name          | Type     |Description|
|---------------|----------|-----------|
|      word     |  string  ||
|      time     |          ||

#### Code Examples

<details>
  <summary>Python Client code for receiving 'randomWord' signal</summary>

The `randomWord` signal can be subscribed to by using the client's `receive_random_word` decorator on a callback function. The name of the function does not matter. The function is called any time the signal is received.

```python
@client.receive_random_word
def on_random_word(word: str, time: datetime):
    print(f"Got a 'randomWord' signal: word={ word } time={ time } ")
```

</details>

<details>
  <summary>Python Server code for emitting 'randomWord' signal</summary>

A server can emit a `randomWord` signal simply by calling the server's `emit_random_word` method.

```python
server.emit_random_word("apples", datetime.now(UTC))
```

</details>

<details>
  <summary>Rust Client code for receiving 'randomWord' signal</summary>

A Rust client receives signals through a `tokio::broadcast` channel.  Receiving from the channel returns a `Result<T, RecvError>` object.  

Since receiving a message through the channel blocks, it may be best to put this into a separate async task.

```rust
let mut random_word_signal_rx = client.get_random_word_receiver();
print("Got a 'randomWord' signal: {:?}", random_word_signal_rx.recv().await);
```

</details>

<details>
  <summary>Rust Server code for emitting 'randomWord' signal</summary>

A server can emit a `randomWord` signal simply by calling the server's `emit_random_word` method.

```rust
let publish_result = server.emit_random_word("apples".to_string(), chrono::Utc::now()).await;
```

The return type is a **Pinned Boxed Future** that resolves to a `Result<(), MethodReturnCode>`.  The future is resolved when the signal is sent (with "publish complete" acknowledgment) or when an error occurs.  If you need to block until the signal is received by the MQTT broker, you can `.await` the future.

</details>

<details>
  <summary>C++ Client code for registering a 'randomWord' signal callback</summary>

A client can register a callback function to be called when a `randomWord` signal is received.  The callback function should take the same parameters as the signal.  In this example, we are using a lambda as the callback function.

```cpp
client.registerRandomWordCallback([](std::string word, std::chrono::time_point<std::chrono::system_clock> time) {
    std::cout << "word=" <<word << " | " << "time=" <<time <<  std::endl;
});
```

</details>

<details>
  <summary>C++ Server code for emitting a 'randomWord' signal</summary>

A `randomWord` signal can be emitted by calling the server's `emitRandomWordSignal` method.  This returns a `std::future` that can be waited on if desired.  The future is resolved when the signal is sent.

```cpp
auto randomWordFuture = server.emitRandomWordSignal("apples", std::chrono::system_clock::now());
randomWordFuture.wait(); // Optional, to block until signal is sent.
```

</details>


## Methods

Methods are requests from a client to a server and the server provides a response back to the client:

```plantuml
@startuml
Client ->> Server : Request(Parameters)
Client <<-- Server: Response(Parameters)
@enduml
```


### Method `addNumbers`

_No documentation for this method_

#### Request Parameters
| Name          | Type     |Description|
|---------------|----------|-----------|
|     first     | integer  ||
|     second    | integer  ||
|     third     | integer   (optional)||

#### Return Parameters

The return value type is `integer`.
#### Code Examples

<details>
  <summary>Python Client code for calling the 'addNumbers' method</summary>

The `addNumbers` method can be called by calling the clients's `add_numbers` method.
This returns a `Future` object.  In this example, we wait up to 5 seconds for the result.

```python
from futures import Future

future = client.add_numbers(first=42, second=42, third=42)
try:
    print(f"RESULT:  {future.result(5)}")
except futures.TimeoutError:
    print(f"Timed out waiting for response to 'add_numbers' call")
```

</details>

<details>
  <summary>Python Server code for handling the 'addNumbers' method</summary>

The server provides an implementation for the `addNumbers` method by using the `@server.handle_add_numbers` decorator on a function.  The name of the function does not matter. 
The decorated method is called everytime the a request for the method is received.  In an error, the method can raise on of the exceptions found in `method_codes.py`.

```python
@server.handle_add_numbers 
def add_numbers(first: int, second: int, third: Optional[int]) -> int:
    """ This is an example handler for the 'addNumbers' method.  """
    print(f"Running add_numbers'({first}, {second}, {third})'")
    return 42
```

</details>

<details>
  <summary>Rust Client code for calling the 'addNumbers' method</summary>

The `FullClient` provides an implementation for the `addNumbers` method.  It will block and return a Result object of either the return payload value, or an error.

```rust
let result = api_client.add_numbers(42, 42, Some(42)).await.expect("Failed to call addNumbers");
println!("addNumbers response: {:?}", result);
```

</details>


### Method `doSomething`

_No documentation for this method_

#### Request Parameters
| Name          | Type     |Description|
|---------------|----------|-----------|
|   task_to_do  |  string  ||

#### Return Parameters

The return value type is ``.
#### Code Examples

<details>
  <summary>Python Client code for calling the 'doSomething' method</summary>

The `doSomething` method can be called by calling the clients's `do_something` method.
This returns a `Future` object.  In this example, we wait up to 5 seconds for the result.

```python
from futures import Future

future = client.do_something(task_to_do="apples")
try:
    print(f"RESULT:  {future.result(5)}")
except futures.TimeoutError:
    print(f"Timed out waiting for response to 'do_something' call")
```

</details>

<details>
  <summary>Python Server code for handling the 'doSomething' method</summary>

The server provides an implementation for the `doSomething` method by using the `@server.handle_do_something` decorator on a function.  The name of the function does not matter. 
The decorated method is called everytime the a request for the method is received.  In an error, the method can raise on of the exceptions found in `method_codes.py`.

```python
@server.handle_do_something 
def do_something(task_to_do: str) -> DoSomethingMethodResponse:
    """ This is an example handler for the 'doSomething' method.  """
    print(f"Running do_something'({task_to_do})'")
    return DoSomethingMethodResponse(label="apples", identifier=42)
```

</details>

<details>
  <summary>Rust Client code for calling the 'doSomething' method</summary>

The `FullClient` provides an implementation for the `doSomething` method.  It will block and return a Result object of either the return payload value, or an error.

```rust
let result = api_client.do_something("apples".to_string()).await.expect("Failed to call doSomething");
println!("doSomething response: {:?}", result);
```

</details>


### Method `what_time_is_it`

Get the current date and time.

#### Request Parameters

There are no arguments for this request.

#### Return Parameters

The return value type is ``.
#### Code Examples

<details>
  <summary>Python Client code for calling the 'what_time_is_it' method</summary>

The `what_time_is_it` method can be called by calling the clients's `what_time_is_it` method.
This returns a `Future` object.  In this example, we wait up to 5 seconds for the result.

```python
from futures import Future

future = client.what_time_is_it()
try:
    print(f"RESULT:  {future.result(5)}")
except futures.TimeoutError:
    print(f"Timed out waiting for response to 'what_time_is_it' call")
```

</details>

<details>
  <summary>Python Server code for handling the 'what_time_is_it' method</summary>

The server provides an implementation for the `what_time_is_it` method by using the `@server.handle_what_time_is_it` decorator on a function.  The name of the function does not matter. 
The decorated method is called everytime the a request for the method is received.  In an error, the method can raise on of the exceptions found in `method_codes.py`.

```python
@server.handle_what_time_is_it 
def what_time_is_it() -> datetime:
    """ This is an example handler for the 'what_time_is_it' method.  """
    print(f"Running what_time_is_it'()'")
    return datetime.now(UTC)
```

</details>

<details>
  <summary>Rust Client code for calling the 'what_time_is_it' method</summary>

The `FullClient` provides an implementation for the `what_time_is_it` method.  It will block and return a Result object of either the return payload value, or an error.

```rust
let result = api_client.what_time_is_it().await.expect("Failed to call what_time_is_it");
println!("what_time_is_it response: {:?}", result);
```

</details>


### Method `hold_temperature`

Hold a temperature for a specified duration.

#### Request Parameters
| Name          | Type     |Description|
|---------------|----------|-----------|
|temperature_celsius|  number  ||

#### Return Parameters

The return value type is `boolean`.
#### Code Examples

<details>
  <summary>Python Client code for calling the 'hold_temperature' method</summary>

The `hold_temperature` method can be called by calling the clients's `hold_temperature` method.
This returns a `Future` object.  In this example, we wait up to 5 seconds for the result.

```python
from futures import Future

future = client.hold_temperature(temperature_celsius=3.14)
try:
    print(f"RESULT:  {future.result(5)}")
except futures.TimeoutError:
    print(f"Timed out waiting for response to 'hold_temperature' call")
```

</details>

<details>
  <summary>Python Server code for handling the 'hold_temperature' method</summary>

The server provides an implementation for the `hold_temperature` method by using the `@server.handle_hold_temperature` decorator on a function.  The name of the function does not matter. 
The decorated method is called everytime the a request for the method is received.  In an error, the method can raise on of the exceptions found in `method_codes.py`.

```python
@server.handle_hold_temperature 
def hold_temperature(temperature_celsius: float) -> bool:
    """ This is an example handler for the 'hold_temperature' method.  """
    print(f"Running hold_temperature'({temperature_celsius})'")
    return True
```

</details>

<details>
  <summary>Rust Client code for calling the 'hold_temperature' method</summary>

The `FullClient` provides an implementation for the `hold_temperature` method.  It will block and return a Result object of either the return payload value, or an error.

```rust
let result = api_client.hold_temperature(3.14).await.expect("Failed to call hold_temperature");
println!("hold_temperature response: {:?}", result);
```

</details>


## Properties

Properties are values (or a set of values) held by the server.   They are re-published when the value changes. 

```plantuml
@startuml
Server -> Server : Set Property
Client <<- Server: Property Updated
@enduml
```

### Property `favorite_number`

My favorite number


| Name          | Type     |Description|
|---------------|----------|-----------|
|     number    | integer  ||

### Code Examples

<details>
  <summary>Rust Server code for reading and writing the 'favorite_number' property</summary>

A server hold the "source of truth" for the value of `favorite_number`.  An `Arc` pointer can be copied and moved that points to the server's property value.   Here is how to write a new value:

```rust
let favorite_number_handle = server.get_favorite_number_handle();
{
    let mut favorite_number_guard = favorite_number_handle.write().await;
    *favorite_number_guard = 2022;
    // Optional, block until the property is published to the MQTT broker:
    favorite_number_guard.commit(std::time::Duration::from_secs(2)).await;

    // If not committed, the property will be published when the guard is dropped in "fire-and-forget" mode.
}

```

If only reading the value, a read guard can be used:

```rust
let favorite_number_guard = favorite_number_handle.read().await;
```

Application code can subscribe to property updates by subscribing to a `tokio::sync::watch` channel which can be obtained by:

```rust
let favorite_number_watch_rx = client.watch_favorite_number();

if favorite_number_watch_rx.changed().await.is_ok() {
    let latest = favorite_number_watch_rx.borrow().clone();
    println!("Property updated: {:?}", latest);
}
```
</details>

<details>
  <summary>Rust Client code for reading and writing  the 'favorite_number' property</summary>

  A Rust client works with properties the same was as the server.  
  When using the `commit()` method on the write guard, the client will send a request to the server to update the property value and block until the server acknowledges the update.
  

</details>


### Property `favorite_foods`

_No documentation is available for this property_

| Name          | Type     |Description|
|---------------|----------|-----------|
|     drink     |  string  ||
|slices_of_pizza| integer  ||
|   breakfast   |  string   (optional)||

### Code Examples

<details>
  <summary>Rust Server code for reading and writing the 'favorite_foods' property</summary>

A server hold the "source of truth" for the value of `favorite_foods`.  An `Arc` pointer can be copied and moved that points to the server's property value.   Here is how to write a new value:

```rust
let favorite_foods_handle = server.get_favorite_foods_handle();
{
    let mut favorite_foods_guard = favorite_foods_handle.write().await;
    let new_favorite_foods_value = FavoriteFoodsProperty {
            drink: "foo".to_string(),
            slices_of_pizza: 2022,
            breakfast: Some("foo".to_string()),
    };
    *favorite_foods_guard = new_favorite_foods_value;
    // Optional, block until the property is published to the MQTT broker:
    favorite_foods_guard.commit(std::time::Duration::from_secs(2)).await;

    // If not committed, the property will be published when the guard is dropped in "fire-and-forget" mode.
}

```

If only reading the value, a read guard can be used:

```rust
let favorite_foods_guard = favorite_foods_handle.read().await;
```

Application code can subscribe to property updates by subscribing to a `tokio::sync::watch` channel which can be obtained by:

```rust
let favorite_foods_watch_rx = client.watch_favorite_foods();

if favorite_foods_watch_rx.changed().await.is_ok() {
    let latest = favorite_foods_watch_rx.borrow().clone();
    println!("Property updated: {:?}", latest);
}
```
</details>

<details>
  <summary>Rust Client code for reading and writing  the 'favorite_foods' property</summary>

  A Rust client works with properties the same was as the server.  
  When using the `commit()` method on the write guard, the client will send a request to the server to update the property value and block until the server acknowledges the update.
  

</details>


### Property `lunch_menu`

_No documentation is available for this property_

This property is **read-only**.  It can only be modified by the server.

| Name          | Type     |Description|
|---------------|----------|-----------|
|     monday    |[Struct Lunch](#enum-Lunch)||
|    tuesday    |[Struct Lunch](#enum-Lunch)|Tuesday's lunch menu.|

### Code Examples

<details>
  <summary>Rust Server code for reading and writing the 'lunch_menu' property</summary>

A server hold the "source of truth" for the value of `lunch_menu`.  An `Arc` pointer can be copied and moved that points to the server's property value.   Here is how to write a new value:

```rust
let lunch_menu_handle = server.get_lunch_menu_handle();
{
    let mut lunch_menu_guard = lunch_menu_handle.write().await;
    let new_lunch_menu_value = LunchMenuProperty {
            monday: Lunch {drink: true, sandwich: "foo".to_string(), crackers: 1.0, day: DayOfTheWeek::Monday, order_number: Some(2022), time_of_lunch: chrono::Utc::now(), duration_of_lunch: chrono::Duration::seconds(967)},
            tuesday: Lunch {drink: true, sandwich: "foo".to_string(), crackers: 1.0, day: DayOfTheWeek::Monday, order_number: Some(2022), time_of_lunch: chrono::Utc::now(), duration_of_lunch: chrono::Duration::seconds(967)},
    };
    *lunch_menu_guard = new_lunch_menu_value;
    // Optional, block until the property is published to the MQTT broker:
    lunch_menu_guard.commit(std::time::Duration::from_secs(2)).await;

    // If not committed, the property will be published when the guard is dropped in "fire-and-forget" mode.
}

```

If only reading the value, a read guard can be used:

```rust
let lunch_menu_guard = lunch_menu_handle.read().await;
```

Application code can subscribe to property updates by subscribing to a `tokio::sync::watch` channel which can be obtained by:

```rust
let lunch_menu_watch_rx = client.watch_lunch_menu();

if lunch_menu_watch_rx.changed().await.is_ok() {
    let latest = lunch_menu_watch_rx.borrow().clone();
    println!("Property updated: {:?}", latest);
}
```
</details>

<details>
  <summary>Rust Client code for reading  the 'lunch_menu' property</summary>

  A Rust client works with properties the same was as the server.  However, since this property is read-only, the client cannot get a write handle to modify the value.
  

</details>


### Property `family_name`

This is to test a property with a single string value.

| Name          | Type     |Description|
|---------------|----------|-----------|
|  family_name  |  string  ||

### Code Examples

<details>
  <summary>Rust Server code for reading and writing the 'family_name' property</summary>

A server hold the "source of truth" for the value of `family_name`.  An `Arc` pointer can be copied and moved that points to the server's property value.   Here is how to write a new value:

```rust
let family_name_handle = server.get_family_name_handle();
{
    let mut family_name_guard = family_name_handle.write().await;
    *family_name_guard = "foo".to_string();
    // Optional, block until the property is published to the MQTT broker:
    family_name_guard.commit(std::time::Duration::from_secs(2)).await;

    // If not committed, the property will be published when the guard is dropped in "fire-and-forget" mode.
}

```

If only reading the value, a read guard can be used:

```rust
let family_name_guard = family_name_handle.read().await;
```

Application code can subscribe to property updates by subscribing to a `tokio::sync::watch` channel which can be obtained by:

```rust
let family_name_watch_rx = client.watch_family_name();

if family_name_watch_rx.changed().await.is_ok() {
    let latest = family_name_watch_rx.borrow().clone();
    println!("Property updated: {:?}", latest);
}
```
</details>

<details>
  <summary>Rust Client code for reading and writing  the 'family_name' property</summary>

  A Rust client works with properties the same was as the server.  
  When using the `commit()` method on the write guard, the client will send a request to the server to update the property value and block until the server acknowledges the update.
  

</details>


### Property `last_breakfast_time`

This is to test a property with a single datetime value.

| Name          | Type     |Description|
|---------------|----------|-----------|
|   timestamp   |          ||

### Code Examples

<details>
  <summary>Rust Server code for reading and writing the 'last_breakfast_time' property</summary>

A server hold the "source of truth" for the value of `last_breakfast_time`.  An `Arc` pointer can be copied and moved that points to the server's property value.   Here is how to write a new value:

```rust
let last_breakfast_time_handle = server.get_last_breakfast_time_handle();
{
    let mut last_breakfast_time_guard = last_breakfast_time_handle.write().await;
    *last_breakfast_time_guard = chrono::Utc::now();
    // Optional, block until the property is published to the MQTT broker:
    last_breakfast_time_guard.commit(std::time::Duration::from_secs(2)).await;

    // If not committed, the property will be published when the guard is dropped in "fire-and-forget" mode.
}

```

If only reading the value, a read guard can be used:

```rust
let last_breakfast_time_guard = last_breakfast_time_handle.read().await;
```

Application code can subscribe to property updates by subscribing to a `tokio::sync::watch` channel which can be obtained by:

```rust
let last_breakfast_time_watch_rx = client.watch_last_breakfast_time();

if last_breakfast_time_watch_rx.changed().await.is_ok() {
    let latest = last_breakfast_time_watch_rx.borrow().clone();
    println!("Property updated: {:?}", latest);
}
```
</details>

<details>
  <summary>Rust Client code for reading and writing  the 'last_breakfast_time' property</summary>

  A Rust client works with properties the same was as the server.  
  When using the `commit()` method on the write guard, the client will send a request to the server to update the property value and block until the server acknowledges the update.
  

</details>


### Property `last_birthdays`

This is to test a property with multiple datetime values.

| Name          | Type     |Description|
|---------------|----------|-----------|
|      mom      |          ||
|      dad      |          ||
|     sister    |           (optional)||
|  brothers_age | integer   (optional)||

### Code Examples

<details>
  <summary>Rust Server code for reading and writing the 'last_birthdays' property</summary>

A server hold the "source of truth" for the value of `last_birthdays`.  An `Arc` pointer can be copied and moved that points to the server's property value.   Here is how to write a new value:

```rust
let last_birthdays_handle = server.get_last_birthdays_handle();
{
    let mut last_birthdays_guard = last_birthdays_handle.write().await;
    let new_last_birthdays_value = LastBirthdaysProperty {
            mom: chrono::Utc::now(),
            dad: chrono::Utc::now(),
            sister: Some(chrono::Utc::now()),
            brothers_age: Some(2022),
    };
    *last_birthdays_guard = new_last_birthdays_value;
    // Optional, block until the property is published to the MQTT broker:
    last_birthdays_guard.commit(std::time::Duration::from_secs(2)).await;

    // If not committed, the property will be published when the guard is dropped in "fire-and-forget" mode.
}

```

If only reading the value, a read guard can be used:

```rust
let last_birthdays_guard = last_birthdays_handle.read().await;
```

Application code can subscribe to property updates by subscribing to a `tokio::sync::watch` channel which can be obtained by:

```rust
let last_birthdays_watch_rx = client.watch_last_birthdays();

if last_birthdays_watch_rx.changed().await.is_ok() {
    let latest = last_birthdays_watch_rx.borrow().clone();
    println!("Property updated: {:?}", latest);
}
```
</details>

<details>
  <summary>Rust Client code for reading and writing  the 'last_birthdays' property</summary>

  A Rust client works with properties the same was as the server.  
  When using the `commit()` method on the write guard, the client will send a request to the server to update the property value and block until the server acknowledges the update.
  

</details>



## Enums


### Enum `DayOfTheWeek`

<a name="Enum-DayOfTheWeek"></a>_No description exists for this enumeration._

* Sunday (1)
* Monday (2)
* Tuesday (3)
* Wednesday (4)
* Thursday (5)
* Friday (6)
* Saturday (7)


## Structures

Structures are a group of values and may be used as an argument in signals, methods, or properties.  Defining a structure allows for easy reuse.

### Struct `Lunch`

<a name="Struct-Lunch"></a>_No general description exists for this structure_

| Name          | Type     |Description|
|---------------|----------|-----------|
|     drink     | boolean  ||
|    sandwich   |  string  ||
|    crackers   |  number  ||
|      day      |[Enum DayOfTheWeek](#enum-DayOfTheWeek)||
|  order_number | integer   (optional)||
| time_of_lunch |          ||
|duration_of_lunch|          ||
