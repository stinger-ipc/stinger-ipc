# Stinger IPC

Stinger IPC is an application layer on top of [AsyncAPI](https://asyncapio.org).  

It provides inter-process communications (IPC) using an MQTT broker to pass messages between processes.

It takes a interface description file (.singeripc):

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

From the above description file, it generates server code, which can be used like this:

```py
conn = MqttConnection('localhost', 1883)
server = ExampleServer(conn)

server.emit_foo("Hello World")
```

and it generates client code which can be used like this:

```py
conn = MqttConnection('localhost', 1883)
client = ExampleClient(conn)

@client.receive_foo
def print_foo_receipt(message):
    print(f"Got a 'foo' signal with message: {message}")
```

## Design goals

 * Low learning curve.
 * No fancy/tricky code.  Generated code should look like a a human wrote it for humans to use it.
 * Useable for embedded systems.
 * Be described by an AsyncAPI spec.

## License

LGPLv2
