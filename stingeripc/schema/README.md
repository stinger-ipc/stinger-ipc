# Stinger Files

Stinger files are YAML files that describe interfaces for inter-process communication (IPC) using the Stinger IPC framework. These files define the structure and types of messages that can be sent and received between different components of a system.

## File Name

Stinger files should be named with the `.stinger.yaml` extension to indicate their purpose and format.
For example: `example_interface.stinger.yaml`

## Structure

A Stinger file typically contains the following:

- **Metadata**: Information about the interface, such as its name, version, title, and summary.
- **Types**: Enumerations and structures that define the data types used in the interface.
- **IPC Components**: Definitions of signals, methods, and properties that make up the interface.

## Minimal Example

Here is a minimal example that shows metadata and the sections for types and IPC components.  No types or components are defined in this example, which is why the sections are an empty mapping.

```yaml
stinger:
  version: 0.0.7

interface:
  name: example_interface
  version: 0.0.1
  title: Example Interface
  summary: An example Stinger interface

enums: {}

structs: {}

signals: {}

methods: {}

properties: {}

```

## Enums

An example enumeration definition:

```yaml
enums:
  Color:
    documentation: An enumeration of colors
    values:
      - name: RED
        description: The color red
      - name: GREEN
        description: The color green
      - name: BLUE
        description: The color blue
      - name: YELLOW
        description: The color yellow
```

## Structs

```yaml
structures:
  Point:
    documentation: A 2D point
    members:
      - name: x
        type: float
        description: The x coordinate
      - name: y
        type: float
        description: The y coordinate
```

## Signals

```yaml
signals:
  PositionUpdated:
    documentation: Signal emitted when the position is updated
    args:
      - name: position
        type: struct
        structName: Point
        description: The new position.
      - name: timestamp
        type: datetime
        description: The timestamp of the update.
```

## Methods

```yaml
methods:
  MoveTo:
    documentation: Move to a new position
    arguments:
      - name: position
        type: struct
        structName: Point
        description: The target position.
    returnValues:
      - name: success
        type: boolean
        description: True if the move was successful, false otherwise.
```

## Properties

```yaml
properties:
  position:
    documentation: The current position.
    values:
      - name: position
        type: struct
        structName: Point
        description: The current position.
      - name: color
        type: enum
        enumName: Color
        description: The color associated with the position.
```

## Validation
Stinger files can be validated against a schema to ensure they conform to the expected structure and types. 

```bash
uvx stinger validate path/to/your_file.stinger.yaml
```
