# _Fully Featured Example Interface_ API Overview 
_Example StingerAPI interface which demonstrates most features._


[[_TOC_]]

## Connections

A connection object is a wrapper around an MQTT client and provides specific functionality to support both clients and servers.
Generally, you only need one connection object per daemon/program, as it can support multiple clients and servers.  

### Connection code Examples

<details>
  <summary>Python</summary>

```python
from connection import LocalConnection

connection_object = LocalConnection()
```

The `connection_object` will be passed to client and server constructors.

</details>

<details>
  <summary>Rust</summary>

```rust
use mqttier::MqttierClient;

MqttierClient::new("localhost", 1883, Some("mqtt_client_id".to_string())).expect("Failed to create MQTT client");
```

The `connection_object` will be passed to client and server constructors.

</details>

<details>
  <summary>C++</summary>

```c++
#include "broker.hpp"

auto connection_object = std::make_shared<LocalConnection>("Full");
```

The `connection_object` will be passed to client and server constructors.

</details>

## Server

A server is a _provider_ of functionality.  It sends signals, handles method calls, and owns property values.

### Server Code Examples

<details>
  <summary>Python Server</summary>

```python
from fullipc.client import FullServer

server = FullServer(connection_object)
```

The `server` object provides methods for emitting signals and updating properties.  It also allows for decorators to indicate method call handlers.

A full example can be viewed by looking at the `if __name__ == "__main__":` section of the generated `fullipc.server.py` module.

</details>



<details>
  <summary>C++ Server</summary>

```c++

```

The `server` object provides methods for emitting signals and updating properties.  It also allows for decorators to indicate method call handlers.

A full example can be viewed by looking at the generated `examples/server_main.cpp` file.`

</details>

## Client

A client is a _utilizer_ of functionality.  It receives signals, makes method calls, reads property values, or requests updates to property values.

<details>
  <summary>Rust</summary>

```rust
let mut api_client = FullClient::new(&mut connection).await;
```

A full example can be viewed by looking at the generated `client/examples/client.rs` file.

</details>

<details>
  <summary>C++ Client</summary>

A full example can be viewed by looking at the generated `examples/client_main.cpp` file.

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
|   dayOfWeek   |[Enum DayOfTheWeek](#enum-DayOfTheWeek) (optional)||

#### Code Examples

<details>
  <summary>Python Client</summary>

The `todayIs` signal can be subscribed to by using the client's `receive_today_is` decorator on a callback function. The name of the function does not matter. The function is called any time the signal is received.

```python
@client.receive_today_is
def on_today_is(dayOfMonth: int, dayOfWeek: stinger_types.DayOfTheWeek | None):
    print(f"Got a 'todayIs' signal: dayOfMonth={ dayOfMonth } dayOfWeek={ dayOfWeek } ")
```

</details>

<details>
  <summary>Python Server</summary>

A server can emit a `todayIs` signal simply by calling the server's `emit_today_is` method.

```python
server.emit_today_is(42, stinger_types.DayOfTheWeek.MONDAY)
```

</details>

<details>
  <summary>Rust Client</summary>

A Rust client receives signals through a `tokio::broadcast` channel.  Receiving from the channel returns a `Result<T, RecvError>` object.  

Since receiving a message through the channel blocks, it may be best to put this into a separate async task.

```rust
let mut today_is_signal_rx = client.get_today_is_receiver();
print("Got a 'todayIs' signal: {:?}", today_is_signal_rx.recv().await);
```

</details>

<details>
  <summary>Rust Server</summary>

A server can emit a `todayIs` signal simply by calling the server's `emit_today_is` method.

```rust
server.emit_today_is(42, Some(DayOfTheWeek::Monday)).await;
```

</details>

<details>
  <summary>C++ Client</summary>

A client can register a callback function to be called when a `todayIs` signal is received.  The callback function should take the same parameters as the signal.  In this example, we are using a lambda as the callback function.

```cpp
client.registerTodayIsCallback([](int dayOfMonth, boost::optional<DayOfTheWeek> dayOfWeek) {
    std::cout << "dayOfMonth=" <<dayOfMonth << " | " << "dayOfWeek=" << "None" <<  std::endl;
});
```

</details>

<details>
  <summary>C++ Server</summary>

A `todayIs` signal can be emitted by calling the server's `emitTodayIsSignal` method.  This returns a `std::future` that can be waited on if desired.  The future is resolved when the signal is sent.

```cpp
auto todayIsFuture = server.emitTodayIsSignal(42, DayOfTheWeek::MONDAY);
todayIsFuture.wait(); // Optional, to block until signal is sent.
```

</details>


### Signal `bark`

Emitted when a dog barks.

#### Signal Parameters for `bark`

| Name          | Type     |Description|
|---------------|----------|-----------|
|      word     |  string  ||

#### Code Examples

<details>
  <summary>Python Client</summary>

The `bark` signal can be subscribed to by using the client's `receive_bark` decorator on a callback function. The name of the function does not matter. The function is called any time the signal is received.

```python
@client.receive_bark
def on_bark(word: str):
    print(f"Got a 'bark' signal: word={ word } ")
```

</details>

<details>
  <summary>Python Server</summary>

A server can emit a `bark` signal simply by calling the server's `emit_bark` method.

```python
server.emit_bark("apples")
```

</details>

<details>
  <summary>Rust Client</summary>

A Rust client receives signals through a `tokio::broadcast` channel.  Receiving from the channel returns a `Result<T, RecvError>` object.  

Since receiving a message through the channel blocks, it may be best to put this into a separate async task.

```rust
let mut bark_signal_rx = client.get_bark_receiver();
print("Got a 'bark' signal: {:?}", bark_signal_rx.recv().await);
```

</details>

<details>
  <summary>Rust Server</summary>

A server can emit a `bark` signal simply by calling the server's `emit_bark` method.

```rust
server.emit_bark("apples".to_string()).await;
```

</details>

<details>
  <summary>C++ Client</summary>

A client can register a callback function to be called when a `bark` signal is received.  The callback function should take the same parameters as the signal.  In this example, we are using a lambda as the callback function.

```cpp
client.registerBarkCallback([](const std::string& word) {
    std::cout << "word=" <<word <<  std::endl;
});
```

</details>

<details>
  <summary>C++ Server</summary>

A `bark` signal can be emitted by calling the server's `emitBarkSignal` method.  This returns a `std::future` that can be waited on if desired.  The future is resolved when the signal is sent.

```cpp
auto barkFuture = server.emitBarkSignal("apples");
barkFuture.wait(); // Optional, to block until signal is sent.
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
  <summary>Python Client</summary>

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
  <summary>Python Server</summary>

The server provides an implementation for the `addNumbers` method by using the `@server.handle_add_numbers` decorator on a function.  The name of the function does not matter. 
The decorated method is called everytime the a request for the method is received.  In an error, the method can raise on of the exceptions found in `method_codes.py`.

```python
@server.handle_add_numbers 
def add_numbers(first: int, second: int, third: int | None) -> int:
    """ This is an example handler for the 'addNumbers' method.  """
    print(f"Running add_numbers'({first}, {second}, {third})'")
    return 42
```

</details>

<details>
  <summary>Rust Client</summary>

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
|    aString    |  string  ||

#### Return Parameters


| Name          | Type     |Description|
|---------------|----------|-----------|
|     label     |  string  ||
|   identifier  | integer  ||
|      day      |[Enum DayOfTheWeek](#enum-DayOfTheWeek)||
#### Code Examples

<details>
  <summary>Python Client</summary>

The `doSomething` method can be called by calling the clients's `do_something` method.
This returns a `Future` object.  In this example, we wait up to 5 seconds for the result.

```python
from futures import Future

future = client.do_something(aString="apples")
try:
    print(f"RESULT:  {future.result(5)}")
except futures.TimeoutError:
    print(f"Timed out waiting for response to 'do_something' call")
```

</details>

<details>
  <summary>Python Server</summary>

The server provides an implementation for the `doSomething` method by using the `@server.handle_do_something` decorator on a function.  The name of the function does not matter. 
The decorated method is called everytime the a request for the method is received.  In an error, the method can raise on of the exceptions found in `method_codes.py`.

```python
@server.handle_do_something 
def do_something(aString: str) -> stinger_types.DoSomethingReturnValue:
    """ This is an example handler for the 'doSomething' method.  """
    print(f"Running do_something'({aString})'")
    return ['"apples"', 42, 'stinger_types.DayOfTheWeek.MONDAY']
```

</details>

<details>
  <summary>Rust Client</summary>

The `FullClient` provides an implementation for the `doSomething` method.  It will block and return a Result object of either the return payload value, or an error.

```rust
let result = api_client.do_something("apples".to_string()).await.expect("Failed to call doSomething");
println!("doSomething response: {:?}", result);
```

</details>


### Method `echo`

Echo back the received message.

#### Request Parameters
| Name          | Type     |Description|
|---------------|----------|-----------|
|    message    |  string  ||

#### Return Parameters

The return value type is `string`.
#### Code Examples

<details>
  <summary>Python Client</summary>

The `echo` method can be called by calling the clients's `echo` method.
This returns a `Future` object.  In this example, we wait up to 5 seconds for the result.

```python
from futures import Future

future = client.echo(message="apples")
try:
    print(f"RESULT:  {future.result(5)}")
except futures.TimeoutError:
    print(f"Timed out waiting for response to 'echo' call")
```

</details>

<details>
  <summary>Python Server</summary>

The server provides an implementation for the `echo` method by using the `@server.handle_echo` decorator on a function.  The name of the function does not matter. 
The decorated method is called everytime the a request for the method is received.  In an error, the method can raise on of the exceptions found in `method_codes.py`.

```python
@server.handle_echo 
def echo(message: str) -> str:
    """ This is an example handler for the 'echo' method.  """
    print(f"Running echo'({message})'")
    return "apples"
```

</details>

<details>
  <summary>Rust Client</summary>

The `FullClient` provides an implementation for the `echo` method.  It will block and return a Result object of either the return payload value, or an error.

```rust
let result = api_client.echo("apples".to_string()).await.expect("Failed to call echo");
println!("echo response: {:?}", result);
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

### Property `favorite_foods`

_No documentation is available for this property_

| Name          | Type     |Description|
|---------------|----------|-----------|
|     drink     |  string  ||
|slices_of_pizza| integer  ||
|   breakfast   |  string   (optional)||

### Property `lunch_menu`

_No documentation is available for this property_

| Name          | Type     |Description|
|---------------|----------|-----------|
|     monday    |[Struct Lunch](#enum-Lunch)||
|    tuesday    |[Struct Lunch](#enum-Lunch)||

### Property `family_name`

This is to test a property with a single string value.

| Name          | Type     |Description|
|---------------|----------|-----------|
|  family_name  |  string  ||


## Enums

### Enum `DayOfTheWeek`

<a name="Enum-DayOfTheWeek"></a>The days of the week.

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
