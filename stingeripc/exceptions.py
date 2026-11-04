class InvalidStingerStructure(Exception):
    pass


class InvalidConfiguration(Exception):
    pass


class ProtobufError(InvalidStingerStructure):
    """A protobuf message could not be found, or protoc could not be run.

    Subclasses :class:`InvalidStingerStructure` because an interface naming a
    message that does not exist is a broken interface definition, and callers
    that already handle malformed stinger files should handle this the same way.
    """

    pass
