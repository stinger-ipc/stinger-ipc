"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
"""

from pydantic import BaseModel, Field


class InterfaceInfo(BaseModel):
    interfaceName: str = Field(default="SignalOnly")
    title: str = Field(default="SignalOnly")
    version: str = Field(default="0.0.1")
    instance: str
    connection_topic: str
    timestamp: str
