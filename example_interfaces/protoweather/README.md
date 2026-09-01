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

A protobuf element takes and hands back the message itself; a JSON element keeps
the unpacked form it has always had, plus a payload-object form:

```python
# protobuf
server.emit_current_conditions_payload(weather_pb2.CurrentConditions(temperature_celsius=21.5))
future = client.call_get_forecast(weather_pb2.ForecastRequest(location="Provo", days=3))

# JSON
server.emit_station_name("Rooftop")                  # unpacked
server.emit_station_name_payload(StationNameSignalPayload(name="Rooftop"))

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
