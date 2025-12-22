"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

from pydantic import BaseModel, Field, PlainValidator, PlainSerializer, ConfigDict
from datetime import datetime, timedelta, UTC

from typing import Optional, Union, List
import base64

from typing import Annotated


def base64_decode_if_str(value: Union[str, bytes, None]) -> Optional[bytes]:
    """If the value is a string, decode it from base64 to bytes.  Otherwise return the bytes as-is."""
    if isinstance(value, str):
        return base64.b64decode(value)
    return value


class InterfaceInfo(BaseModel):
    interface_name: str = Field(default="SignalOnly")
    title: str = Field(default="SignalOnly")
    version: str = Field(default="0.0.1")
    instance: str
    connection_topic: str
    timestamp: str


class AnotherSignalSignalPayload(BaseModel):
    """Interface signal `anotherSignal`."""

    model_config = ConfigDict(populate_by_name=True)
    one: Annotated[float, Field()]
    two: Annotated[bool, Field()]
    three: Annotated[str, Field()]


class BarkSignalPayload(BaseModel):
    """Interface signal `bark`.

    Emitted when a dog barks.
    """

    model_config = ConfigDict(populate_by_name=True)
    word: Annotated[str, Field()]


class MaybeNumberSignalPayload(BaseModel):
    """Interface signal `maybe_number`.

    A signal with optionally no payload.
    """

    model_config = ConfigDict(populate_by_name=True)
    number: Annotated[Optional[int], Field()] = None


class MaybeNameSignalPayload(BaseModel):
    """Interface signal `maybe_name`.

    A signal with optionally no payload.
    """

    model_config = ConfigDict(populate_by_name=True)
    name: Annotated[Optional[str], Field()] = None


class NowSignalPayload(BaseModel):
    """Interface signal `now`.

    The current date and time.
    """

    model_config = ConfigDict(populate_by_name=True)
    timestamp: Annotated[datetime, Field()]
