Usage
=====

Stinger-IPC turns a declarative interface description (a ``*.stinger.yaml``
file) into client and server code for Python 3, C++11, and Rust.

Defining an interface
---------------------

A very brief example of an interface description is:

.. code-block:: yaml

   stingeripc:
     version: 0.3.0

   interface:
     name: Example
     version: 0.0.1

   signals:

     foo:
       values:
         - name: message
           type: string

   methods:

     addNumbers:
       arguments:
         - name: left
           type: integer
         - name: right
           type: integer
       returnValue:
         name: sum
         type: integer

   commands:

     set_volume:
       arguments:
         - name: level
           type: integer

   properties:

     favorite_number:
       value:
         name: number
         type: integer

The ``stinger-ipc`` command provides two main subcommands for working with
Stinger interface files.

Generate code
-------------

Generate code from a Stinger interface YAML file:

.. code-block:: bash

   uvx stinger-ipc generate INPUT_FILE OUTPUT_DIR [OPTIONS]

**Arguments**

* ``INPUT_FILE`` — Path to the ``.stinger.yaml`` interface description file
* ``OUTPUT_DIR`` — Directory where generated files will be written

**Options**

* ``-l, --language TEXT`` — Language to generate: ``rust``, ``python``,
  ``markdown``, ``cpp``, ``web``, ``protobuf``
* ``--template-pkg TEXT`` — Python package(s) containing custom templates
  (advanced)
* ``--template-path PATH`` — Filesystem path(s) to custom template directories
  (advanced)
* ``--consumer TEXT`` — Consumer name/identifier for filtering interface
  (advanced)
* ``--config PATH`` — TOML configuration file(s); later files override earlier
  ones (can be specified multiple times)

**Examples**

.. code-block:: bash

   # Generate Python code
   uvx stinger-ipc generate my_interface.stinger.yaml ./output --language python

Validate an interface
---------------------

Validate a Stinger interface YAML file against the schema:

.. code-block:: bash

   uvx stinger-ipc validate INPUT_FILE

First-class code generation
---------------------------

From the StingerIPC description file, server and client code is generated
directly for Python3, C++11, and Rust.

Server code
~~~~~~~~~~~

From the description file above, StingerIPC generates server code which can be
used like this:

.. code-block:: python

   # Python
   conn = MqttConnection('localhost', 1883)
   server = ExampleServer(conn)

   server.emit_foo("Hello World")

   @server.handle_add_numbers
   def add_numbers(left: int, right: int) -> int:
       return left + right

.. code-block:: cpp

   // C++
   auto conn = std::make_shared<DefaultConnection>("localhost", 1883);
   ExampleServer server(conn);
   server.emitFoo("Hello World").wait();

   server.registerAddNumbersHandler([](int left, int right) -> int
   {
     return left + right;
   });

.. code-block:: rust

   // Rust
   let connection = Connection::new(String::from("tcp://localhost:1883"));
   let mut server = SignalOnlyServer::new(connection);
   server.emit_foo("Hello World".to_string());

   server.register_add_numbers_handler(|left, right| {
       left + right
   });

Commands
--------

A **command** is a fire-and-forget message sent from a client to a server.  The
client publishes the command's arguments and never learns whether the server
acted on them.  Because there is no response channel, a server that cannot
deserialize or validate an incoming command can only log and drop it.

A command declares its payload with ``arguments:``, the same key a method uses:

.. code-block:: yaml

   commands:

     set_volume:
       documentation: Tell the server to change the playback volume.
       arguments:
         - name: level
           type: integer

Clients send a command, and servers register handlers for it.  Unlike a method,
a command may have **any number of handlers, and all of them are optional** —
a command that arrives with no handler registered is logged and dropped.

.. code-block:: python

   # Python client
   client.send_set_volume(level=7)

   # Python server
   @server.receive_set_volume
   def on_set_volume(level: int):
       print(f"Setting volume to {level}")

Schema validation
-----------------

An argument may carry an optional ``schema:`` block — a JSON Schema that
further constrains its value.  Every generated payload model exposes a
validation method that is **always present** and is a no-op success when the
field has no schema:

* ``validate_schema()`` on **Python** (returns ``bool``, raises
  ``jsonschema.ValidationError``)
* ``validate_schema()`` on **Rust** (returns ``Result<(), String>``)
* ``ValidateSchema()`` (returns ``bool``) on **C++** method-payload structs

The Rust **server** calls these at every publish/consume boundary (method
request/response, property update/publish, signal emit), failing with the
appropriate ``MethodReturnCode`` rather than sending non-conforming data.

The example values that appear in generated demos, tests, and documentation also
respect the constraint, so generated code never rejects its own examples.  If a
constraint is written so that no example value can satisfy it — a ``pattern``, or
a range with nothing in it — generation fails with a message naming the argument,
rather than quietly emitting a value that would be rejected.
