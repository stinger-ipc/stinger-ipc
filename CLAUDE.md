# CLAUDE.md

## What this project does

stinger-ipc is a **code generator for inter-process communication (IPC) API interfaces**.
Given a declarative description of an interface, it produces ready-to-use client and
server code in multiple target languages so that separate processes can communicate
against a shared, strongly-typed contract.

## How it works

1. **Interface definition files** — The project consumes interface definitions written
   as `*.stinger.yaml` files. Each file describes an IPC interface: its signals,
   methods, properties, and the data types of their arguments. An argument may also
   carry an optional `schema:` block — a JSON Schema that further constrains its value
   (see "Schema validation" below). See [example_interfaces/](example_interfaces/) for
   samples (e.g. [weather.stinger.yaml](example_interfaces/weather/weather.stinger.yaml)).

2. **Parsing into data models** — The YAML definitions are loaded and validated into
   Python data models that represent the interface in memory. These models live in
   [stingeripc/](stingeripc/) and cover the core concepts:
   - [interface.py](stingeripc/interface.py) — the top-level interface model
   - [ipc_signal.py](stingeripc/ipc_signal.py), [ipc_method.py](stingeripc/ipc_method.py),
     [ipc_property.py](stingeripc/ipc_property.py) — the interface elements
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

## Schema validation

An argument's optional `schema:` constraint flows through the whole pipeline:

- **Definition** — `schema:` is limited to the subset of JSON Schema (Draft 4) that the
  RapidJSON C++ validator supports. This subset is itself defined as the `jsonSchema`
  `$def` in [schema.yaml](schemas/schema.yaml), so unsupported keywords are rejected
  at load time.
- **Model** — the constraint is parsed onto the base `Arg` model as `value_schema`
  (a dict, aliased from `schema`) in [arg_models.py](stingeripc/arg_models.py).
  `StingerSpec.uses_schemas()` reports whether any argument declares one.
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
  authoritative schema for `*.stinger.yaml` files is [schema.yaml](schemas/schema.yaml).
- [Taskfile.yml](Taskfile.yml) — task runner entry points (e.g. `task generate`).

## Common tasks

- Generate code from the example interfaces: `task generate`
  (set `GENERATED_DIR=<dir>` to control the output location).
- See [README.md](README.md) for full usage and setup details.
