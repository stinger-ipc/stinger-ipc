"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
"""

from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional


class InterfaceInfo(BaseModel):
    interfaceName: str = Field(default="SignalOnly")
    title: str = Field(default="SignalOnly")
    version: str = Field(default="0.0.1")
    instance: str
    connection_topic: str
    timestamp: str


class AnotherSignalSignalPayload(BaseModel):
    """Interface signal `anotherSignal`."""

    one: float
    two: bool
    three: str


class BarkSignalPayload(BaseModel):
    """Interface signal `bark`.

    Emitted when a dog barks.
    """

    word: str


class MaybeNumberSignalPayload(BaseModel):
    """Interface signal `maybe_number`.

    A signal with optionally no payload.
    """

    number: Optional[int]


class MaybeNameSignalPayload(BaseModel):
    """Interface signal `maybe_name`.

    A signal with optionally no payload.
    """

    name: Optional[str]


class NowSignalPayload(BaseModel):
    """Interface signal `now`.

    The current date and time.
    """

    timestamp: datetime
