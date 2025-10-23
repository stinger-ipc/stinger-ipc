# Stinger IPC

StingerIPC provides inter-process communications (IPC) between a server and multiple clients running on the same or separate hosts.  It uses an MQTT server to pass messages between processes, implementing several IPC patterns: signals, properties, and proceedures.

## Project Status

This project is in early stages of active development.  You should not use it in any of your projects, both because it doesn't have enough features yet to be useful, and also because things will probably be horribly broken on future updates.

## Interface Description

StingerIPC takes a interface description file (.singeripc), and will generate code and documentation from it.  A very brief example of a interface description is:

```yaml
stingeripc:
  version: 0.0.7

interface:
  name: Example
  version: 0.0.1

signals:

  foo:
    payload:
      - name: message
        type: string

methods:

  addNumbers:
    arguments:
      - name: left
        type: integer
      - name: right
        type: integer
    returnValues:
      - name: sum
        type: integer

```
## First class code generation 

From the StingerIPC description file, we directly generate server and client code for these languages: Python3, C++11, and Rust.

### Server Code

From the above description file, StingerIPC generates server code, which can be used like this:

```py
# Python
conn = MqttConnection('localhost', 1883)
server = ExampleServer(conn)

server.emit_foo("Hello World")

@server.handle_add_numbers
def add_numbers(left: int, right: int) -> int:
    return left + right
```

```c++
// C++
auto conn = std::make_shared<DefaultConnection>("localhost", 1883);
ExampleServer server(conn);
server.emitFoo("Hello World").wait();

server.registerAddNumbersHandler([](int left, int right) -> int
{
  return left + right;
});
```

```rust
// Rust
let connection = Connection::new(String::from("tcp://localhost:1883"));
let mut server = SignalOnlyServer::new(connection);
server.emit_foo("Hello World".to_string());

server.register_add_numbers_handler(|left, right| {
    left + right
});
```

### Client Code

From the above description file, StingerIPC generates client code which can be used like this:

```py
# Python
conn = MqttConnection('localhost', 1883)
client = ExampleClient(conn)

@client.receive_foo
def print_foo_receipt(message):
    print(f"Got a 'foo' signal with message: {message}")

future = client.add_numbers(1, 2)
timeout = 5
print(future.result(timeout))
```

```c++
// C++
auto conn = std::make_shared<DefaultConnection>("localhost", 1883);
ExampleClient client(conn);
client.registerFooCallback([](const std::string& message) {
    std::cout << message << std::endl;
});

std::cout << "One plus three is " << client.addNumbers(1, 3).wait() << std::endl;
```

```rust
// Rust
let connection = Connection::new(String::from("tcp://localhost:1883"));
let mut client = ExampleClient::new(connection);
client.set_signal_recv_callbacks_for_foo(|message| {
    println!("{}", message);
});

client.add_numbers(1, 4);
```

## AsyncAPI and second-class code generation

[AsyncAPI](https://www.asyncapi.com/) is a specification format for describing asynchronous message APIs.  Since StingerIPC uses and abstracts asynchonous messages between server and clients, we can describe a StingerIPC system with an AsyncAPI document.  

From that AsyncAPI document, we can [generate code and documentation](https://www.asyncapi.com/tools/generator) in additional languages.  While this code generation won't implement our standard IPC design patterns, it does make accessing the communications more easy.

## Inter-process communication (IPC)

The motivation for this project is that I've seen embedded Linux projects that run several daemons that need to talk to each other, and for whatever reasons D-Bus wasn't a good option.

So this project is a way for those daemons/programs to communicate with each other through an MQTT broker running on the same device.  The design goals of this project have been tuned toward this use case.

That being said, there is nothing prohibiting Stinger-IPC to be used for RPC: remote proceedure calls.  RPC typically involves being able to call into a system from a different system.  That certainly can be done by having the remote systems connect into the same MQTT broker as the local system.  However, this isn't the primary use case, and design goals aren't geared to make Stinger-IPC the best solution for RPC (though don't let that stop you from using it that way).  Specifically, Stinger-IPC requires the server and all clients to be running the same version of code.  For systems where all the software ships together, this usually isn't a problem, but could be a problem for systems with remote connections.  

### Comparison to gRPC

gRPC is probably a better solution for handling RPC and connections from remote clients.  It does a much better job at handling compatibility between different versions, supporting a wider number of languages, and transports messages more efficiently.

But gRPC, as most typically deployed, provide some challenges for use inside an embedded Linux system.  gRPC typically wants secured HTTP/2 connections, which are just overkill for communications within a single device.  Additionally, the protobuf code generation is just more complicated.  


## Design goals

 * Low learning curve.
 * No fancy/tricky code.  Generated code should look like a a human wrote it for humans to use it.
 * Useable for embedded Linux systems.
 * Be described by an AsyncAPI spec.

## License

### Generator Code

The stinger-ipc generator (Python scripts, templates, and related files) is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

### Generated Code

**Code generated by stinger-ipc is NOT subject to the MIT License.** As a special exception, you may use, modify, and distribute code generated by stinger-ipc under any license of your choosing, including proprietary licenses, without attribution or restriction.

This exception applies to all output produced by running the stinger-ipc code generator, regardless of the input files or configuration used. You are free to:

* Use generated code in commercial projects
* Relicense generated code under any terms
* Modify and distribute without attribution
* Include in proprietary software

The templates in `stingeripc/templates/` automatically include a license notice in generated files to clarify this.
