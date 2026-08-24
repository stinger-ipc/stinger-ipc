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
  (`config.topics.commands`, default `{interface_name}/{service_id}/command/{command_name}`).
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
