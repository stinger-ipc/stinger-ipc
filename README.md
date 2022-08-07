# Stinger IPC

StingerIPC provides inter-process communications (IPC) between a server and multiple clients running on the same or separate hosts.  It uses an MQTT server to pass messages between processes, implementing several IPC patterns: signals, properties, and proceedures.

## Interface Description

StingerIPC takes a interface description file (.singeripc), and will generate code and documentation from it.  A very brief example of a interface description is:

```yaml
stingeripc:
  version: 0.0.5

interface:
  name: Example
  version: 0.0.1

signals:

  foo:
    payload:
      - name: message
        type: string
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
```

```c++
// C++
auto conn = std::make_shared<LocalConnection>();
ExampleServer server(conn);
server.emitFoo("Hello World").wait();
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
```

```c++
// C++
auto conn = std::make_shared<LocalConnection>();
ExampleClient client(conn);
client.registerFooCallback([](const std::string& message) {
    std::cout << message <<  std::endl;
});
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

LGPLv2
