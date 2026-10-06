# CLAUDE.md

## What this project does

stinger-ipc is a **code generator for inter-process communication (IPC) API interfaces**.
Given a declarative description of an interface, it produces ready-to-use client and
server code in multiple target languages so that separate processes can communicate
against a shared, strongly-typed contract.

## How it works

1. **Interface definition files** — The project consumes interface definitions written
   as `*.stinger.yaml` files. Each file describes an IPC interface: its signals,
   methods, commands, properties, and the data types of their arguments. A signal and a
   struct each take a list of `values`, and a method and a command each a list of
   `arguments`, while a method's `returnValue` and a property's `value` are each a
   single arg. An argument may also
   carry an optional `schema:` block — a JSON Schema that further constrains its value
   (see "Schema validation" below). See [example_interfaces/](example_interfaces/) for
   samples (e.g. [weather.stinger.yaml](example_interfaces/weather/weather.stinger.yaml)).

2. **Parsing into data models** — The YAML definitions are loaded and validated into
   Python data models that represent the interface in memory. These models live in
   [stingeripc/](stingeripc/) and cover the core concepts:
   - [interface.py](stingeripc/interface.py) — the top-level interface model
   - [ipc_signal.py](stingeripc/ipc_signal.py), [ipc_method.py](stingeripc/ipc_method.py),
     [ipc_command.py](stingeripc/ipc_command.py), [ipc_property.py](stingeripc/ipc_property.py)
     — the interface elements
   - [arg_models.py](stingeripc/arg_models.py), [arg_datatypes.py](stingeripc/arg_datatypes.py),
     [args.py](stingeripc/args.py) — argument and data-type modeling

3. **Code generation via Jinja2 templates** — The data models are rendered through a
   collection of Jinja2 templates in [stingeripc/templates/](stingeripc/templates/) to
   emit the interface code. Each target language has its own template directory:
   - [python/](stingeripc/templates/python/)
   - [rust/](stingeripc/templates/rust/)
   - [cpp/](stingeripc/templates/cpp/)

   (Additional outputs such as `markdown`, `protobuf`, and `web` templates also exist.)

   Language-specific symbol/naming helpers ([python_symb.py](stingeripc/python_symb.py),
   [rust_symb.py](stingeripc/rust_symb.py), [cpp_symb.py](stingeripc/cpp_symb.py))
   handle per-language identifier and type conventions during rendering.

## The four interface patterns

A **pattern** is one of the parts an interface is built from. They differ in direction
and in whether a reply comes back:

| Pattern | Direction | Reply | YAML payload key |
|---|---|---|---|
| `signals` | server → client | none | `values` |
| `commands` | client → server | none | `arguments` |
| `methods` | client → server | response | `arguments` (+ `returnValue`) |
| `properties` | server owns, client reads/updates | update response | `value` |

A **command** is the mirror image of a signal — the same fire-and-forget message,
travelling the other way — or equivalently a method with no response. Its
implementation follows from that:

- Modeled by `IpcCommand` in [ipc_command.py](stingeripc/ipc_command.py), which mirrors
  `IpcMethod` minus the return value. Published on the `commands` topic template
  (`configuration.topics.commands` in the .stinger.yaml, default `{interface_name}/{service_id}/command/{command_name}`).
- The **server** may consume a command from **any number of places, all optional**, the
  way a *client* consumes signals. A command that arrives with nothing consuming it is
  logged and dropped. Each language uses its own idiom for this, mirroring however that
  language's *client* receives signals: Python and C++ register any number of callbacks,
  while Rust hands out `tokio::sync::broadcast` receivers.
- Because there is no response channel, a server that cannot deserialize or validate an
  incoming command logs and drops it. It must never publish an error back — there is
  nowhere to send one.
- The server does not learn which client sent a command; the topic carries no client id.
- Generated API: client `send_<command>(args…)`; payload type `<Name>CommandPayload`.
  On the server, Python is `receive_<command>(handler)` (usable as a decorator), C++ is
  `receive<Command>Command(handler)`, and Rust is
  `get_<command>_receiver() -> broadcast::Receiver<T>` — where `T` follows the same rule
  the Rust client uses for signals: `()` for no arguments, the argument's own type for
  exactly one, and `<Name>CommandPayload` for several. A Rust receiver must be subscribed
  before a command arrives, since a broadcast channel does not replay.
- Commands support the same `documentation`, `version`, `consumers`, `schema`, and
  `protobuf` features as signals and methods, and their versions are advertised in the
  discovery message's `commands` map alongside `methods`.

## Protobuf payloads

An element may declare `protobuf: <fully.qualified.Message>` instead of a JSON
argument list (a method declares `protobuf:` and `returnProtobuf:` together). The
message is resolved against the hand-written `.proto` sources named by
`[protobuf] path`, using a descriptor set from `protoc` rather than by parsing
`.proto` text — see [protobuf_compiler.py](stingeripc/protobuf_compiler.py).

- **Model** — protobuf is modeled at the *payload* level, not the argument level:
  a `Payload` ([payload.py](stingeripc/payload.py)) holds either `args` or a
  `ProtobufMessageRef`, never both, and `arg_list` is empty in the protobuf case.
  Resolving a reference fills in its descriptor and also resolves the message or
  enum each of its fields is typed with, so a signature can name those types.
- **The generated API takes the message's fields, not the message.** A signal,
  command or method spreads its message's fields into individual parameters exactly
  as a JSON payload spreads `arg_list`, and builds the message internally; receivers
  are handed the same fields. A method handler still *returns* the response message
  object, and a method caller's result is still that object, because a response is
  one value rather than a parameter list. `ProtobufMessageRef.param_fields` fixes
  the order every language uses: fields that must be supplied first, then those that
  may be left unset (a proto3 `optional` or a `oneof` member), each in declaration
  order. There is no whole-message entry point for a protobuf element.
- **Field types** follow the target language's protobuf bindings: repeated becomes
  `List`/`Vec`/`std::vector`, a map becomes `Dict`/`HashMap`/`std::map`, a
  message-typed field keeps its generated type, and an unsettable field becomes
  `Optional`/`Option`/`std::optional`. Rust is the one place a real `oneof` is a
  single parameter, because prost generates it as one `Option<Enum>` struct member.
  Per-language spellings live in `Python/Rust/CppProtobufFieldSymbols`.
- **Properties are the exception**: a protobuf property's value *is* the message.
  The getter returns it, the setter takes it, and change callbacks receive it.
  Rust's signal and command receivers likewise still yield the whole message, since
  a broadcast channel carries one item type.

### Bundled vs external bindings

By default (`[protobuf] mode = "bundled"`) each language's `partials/protoc.toml` recipe
copies the `.proto` sources into the output and compiles them there. That breaks a host
process that already loads its own bindings for the same files: protobuf's descriptor
pool is process-wide and keyed by `.proto` file name, so Python raises "duplicate file
name", C++ fails to link or aborts at startup, and Rust gets two incompatible copies of
each type.

`mode = "external"` leaves the bindings to the host. The messages are still resolved
against the `[protobuf] path` sources, since the generated field handling is built from
their descriptors, but `emit_protobuf_bindings` copies, compiles and rewrites nothing, and
the generated code references the host's bindings instead. `[protobuf.external]` says where
each language finds them (see [external-protobuf.toml](example_interfaces/external-protobuf.toml)):

- `python_package` — `from <pkg> import x_pb2`; empty means a top-level `import x_pb2`.
- `cpp_include_dir` / `cpp_cmake_target` — the `#include` prefix, and a CMake target linked
  to the generated library (through `BUILD_LOCAL_INTERFACE`, so it stays out of the exports).
- `rust_module` / `rust_dependency` — where the prost types live (a protobuf package nests
  below it one module per segment) and the `Cargo.toml` line that supplies the crate.

The host's bindings must come from the same `.proto` files at the same paths relative to
the source root, because that root decides Python module names and C++ header paths.
Well-known types come from each language's runtime in both modes. A ref's language symbols
only learn the mode through `ProtobufMessageRef.bind_config`, which
`resolve_protobuf_messages` calls once resolution is done.

## Schema validation

An argument's optional `schema:` constraint flows through the whole pipeline:

- **Definition** — `schema:` is limited to the subset of JSON Schema (Draft 4) that the
  RapidJSON C++ validator supports. This subset is itself defined as the `jsonSchema`
  `$def` in [schema.yaml](schemas/0.3/schema.yaml), so unsupported keywords are rejected
  at load time.
- **Model** — the constraint is parsed onto the base `Arg` model as `value_schema`
  (a dict, aliased from `schema`) in [arg_models.py](stingeripc/arg_models.py).
  `StingerSpec.uses_schemas()` reports whether any argument declares one, and
  `Arg.schema_allows(value)` answers whether a value satisfies it (always true when no
  constraint is declared).
- **Example values** — `Arg.get_random_example_value()` respects the constraint, because
  those values feed the generated demos, tests, and documentation and would otherwise be
  rejected by the generated validation code. Stock candidates are filtered to the
  conforming ones; failing that, a value is derived from the constraint's `enum` or its
  bounds (`minimum`/`maximum`/`multipleOf`/`minLength`/`maxLength`, and `minItems`/
  `maxItems` for how many elements an array example carries). Validation uses
  `jsonschema-rs` at Draft 4, matching what the generated code enforces. An argument with
  no constraint keeps exactly the value it had before, so generated output does not churn.
  A constraint that no value can satisfy — a `pattern`, or an empty range — raises
  `InvalidStingerStructure` at generation time rather than emitting an example the
  generated code would reject.
- **Generated code** — every generated payload model exposes a validation method that
  is **always present** and is a no-op success when the field has no schema:
  `validate_schema()` on Python (returns `bool`, raises `jsonschema.ValidationError`)
  and Rust (returns `Result<(), String>`), and `ValidateSchema()` (returns `bool`) on
  C++ method-payload structs. The generated Python/Rust projects gain a `jsonschema`
  dependency. The Rust **server** calls these at every publish/consume boundary
  (method request/response, property update/publish, signal emit), failing with the
  appropriate `MethodReturnCode` rather than sending non-conforming data.

## Layout

- [stingeripc/](stingeripc/) — the Python package: data models, language symbol helpers,
  and the Jinja2 templates.
- [stingeripc/tools/](stingeripc/tools/) — CLI and the generic generator entry points.
- [example_interfaces/](example_interfaces/) — sample `*.stinger.yaml` definitions.
- [generated/](generated/) — output of running the generator against the examples.
- [schemas/](schemas/) — schema(s) describing the `*.stinger.yaml` format. The
  authoritative schema for `*.stinger.yaml` files is [schema.yaml](schemas/0.3/schema.yaml).
- [Taskfile.yml](Taskfile.yml) — task runner entry points (e.g. `task generate`).

## Common tasks

- Generate code from the example interfaces: `task generate`
  (set `GENERATED_DIR=<dir>` to control the output location).
- See [README.md](README.md) for full usage and setup details.
