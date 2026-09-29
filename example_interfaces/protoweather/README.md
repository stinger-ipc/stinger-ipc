# protoweather — protobuf payloads example

An interface whose payloads are a mix of JSON and protobuf messages.  Each pattern
appears twice, once each way, so the generated output shows both side by side:

| Pattern | protobuf | JSON |
|---|---|---|
| signal | `currentConditions` | `stationName` |
| method | `getForecast` | `convertToFahrenheit` |
| command | `refresh` | `resetCounters` |
| property | `currentConditions` | `stationId` |

An element declares either a payload of arguments or a protobuf message by
fully-qualified name, never both.  Stinger resolves the name against the `.proto`
files under the directory named by `[protobuf] path`
(see [protobuf-path.toml](../protobuf-path.toml)), relative to the interface file.

A protobuf property's value *is* the message.  Where a JSON property wraps its one
value in a generated model with a single named field, a protobuf property has no
wrapper: the getter returns the message, the setter takes it, and change callbacks
receive it.

## Generating

```
task markdown:generate:protoweather
task python:generate:protoweather
task cpp:generate:protoweather
task rust:generate:protoweather
```

## What the generated API looks like

A signal, command or method takes the **fields of its message** one by one and
builds the message itself, the same way a JSON element spreads its arguments.  A
JSON element keeps the unpacked form it has always had, plus a payload-object form
that a protobuf element does not have:

```python
# protobuf -- one parameter per field of the message
server.emit_current_conditions(21.5, "Sunny", 40)
future = client.get_forecast("Provo", 3)             # -> resolves to weather_pb2.Forecast
client.send_refresh(include_humidity=True)
client.send_do_nothing()                             # google.protobuf.Empty has no fields

# JSON
server.emit_station_name("Rooftop")                  # unpacked
server.emit_station_name_payload(StationNameSignalPayload(name="Rooftop"))
```

A receiver is handed the same fields, and a method handler returns the response
**message**, since the response is one object rather than a parameter list:

```python
@client_builder.receive_current_conditions
def on_conditions(temperature_celsius: float, description: str, humidity_percent: int): ...

@server.handle_get_forecast
async def get_forecast(location: str, days: int) -> weather_pb2.Forecast: ...

@server.receive_refresh
def on_refresh(include_humidity: bool): ...
```

A field that may be left unset -- a proto3 `optional`, or a member of a `oneof` --
is an optional parameter and comes last; a repeated field is a list, a map is a
dict, and a message-typed field keeps its own generated type.

The other languages follow the same rule, in their own idiom:

```rust
server.emit_current_conditions(21.5, "Sunny".to_string(), 40).await;
let forecast = client.get_forecast("Provo".to_string(), 3).await?;
```

```cpp
server.emitCurrentConditionsSignal(21.5f, "Sunny", 40);
std::future<::protoweather::v1::Forecast> f = client.getForecast("Provo", 3);
```

A property is the exception: its value *is* the message, whole.

```python
# a protobuf property's value is the message itself
server.current_conditions = weather_pb2.CurrentConditions(humidity_percent=40)
reading = server.current_conditions                  # -> weather_pb2.CurrentConditions
```

## Toolchain

Resolving message names needs `protoc`.  Stinger uses the one on `PATH`, falls back
to `uvx --from=protoc-wrapper@33.0 protoc`, and honours `[protobuf] protoc` if you
want to name a specific binary.

Building the generated code needs more, per language:

- **Python** — nothing extra.  Stinger runs `protoc --python_out` and the `_pb2`
  modules ship inside the generated package.
- **C++** — protobuf's C++ runtime and headers (`libprotobuf-dev`, or a local
  build pointed at with `-DCMAKE_PREFIX_PATH`).  The generated `CMakeLists.txt`
  uses `find_package(Protobuf CONFIG REQUIRED)`, because protobuf v22 and later
  depend on Abseil and only protobuf's own config package declares that.
- **Rust** — the `protoc-gen-prost` plugin on `PATH`
  (`cargo install protoc-gen-prost`), which stinger invokes to write the crate's
  `src/proto/` bindings.
