"""Topic templates declared by an interface.

The broker topics an interface's messages travel on are part of the interface
contract -- a client and a server only find each other if they agree on them --
so they are declared in the ``*.stinger.yaml`` file itself rather than in the
generator's configuration.  The YAML keys are camelCase like the rest of the
stinger format; the Python attributes are the snake_case equivalents.
"""

import re
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .topic_util import get_argument_position


class InterfaceTopics(BaseModel):
    """The topic templates an interface publishes and subscribes on."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    params: List[str] = Field(default_factory=list, description="List of parameters to include in topic templates")
    signals: str = Field(default="{interface_name}/{service_id}/signal/{signal_name}", description="Topic template for signals")
    property_values: str = Field(default="{interface_name}/{service_id}/property/{property_name}/value", alias="propertyValues", description="Topic template for property values")
    property_updates: str = Field(default="{interface_name}/{service_id}/property/{property_name}/update", alias="propertyUpdates", description="Topic template for property updates")
    property_update_responses: str = Field(
        default="client/{client_id}/{interface_name}/property/{property_name}/update/response",
        alias="propertyUpdateResponses",
        description="Topic template for property update responses",
    )
    commands: str = Field(default="{interface_name}/{service_id}/command/{command_name}", description="Topic template for commands")
    method_requests: str = Field(default="{interface_name}/{service_id}/method/{method_name}/request", alias="methodRequests", description="Topic template for method requests")
    method_responses: str = Field(default="client/{client_id}/{interface_name}/method/{method_name}/response", alias="methodResponses", description="Topic template for method responses")
    interface_discovery: str = Field(default="{interface_name}/{service_id}/interface", alias="interfaceDiscovery", description="Topic template for interface discovery")
    lwt: str = Field(default="client/{client_id}/online", description="Topic template for Last Will and Testament messages")

    @field_validator("property_values")
    @classmethod
    def validate_property_values(cls, v: str) -> str:
        if get_argument_position(v, "property_name") is None:
            raise ValueError('"propertyValues" topic template must contain {property_name} placeholder')
        if get_argument_position(v, "service_id") is None:
            raise ValueError('"propertyValues" topic template must contain {service_id} placeholder')
        return v

    @field_validator("commands")
    @classmethod
    def validate_commands(cls, v: str) -> str:
        if get_argument_position(v, "command_name") is None:
            raise ValueError('"commands" topic template must contain {command_name} placeholder')
        if get_argument_position(v, "service_id") is None:
            raise ValueError('"commands" topic template must contain {service_id} placeholder')
        return v

    @field_validator("property_update_responses")
    @classmethod
    def validate_property_update_responses(cls, v: str) -> str:
        if get_argument_position(v, "property_name") is None:
            raise ValueError('"propertyUpdateResponses" topic template must contain {property_name} placeholder')
        return v

    @field_validator("method_responses")
    @classmethod
    def validate_method_responses(cls, v: str) -> str:
        if get_argument_position(v, "method_name") is None:
            raise ValueError('"methodResponses" topic template must contain {method_name} placeholder')
        return v

    @field_validator("params")
    @classmethod
    def validate_params(cls, v: List[str]) -> List[str]:
        reserved_params = {"interface_name", "service_id", "signal_name", "property_name", "method_name", "command_name", "client_id", "instance_id"}
        for param in v:
            if param in reserved_params:
                raise ValueError(f"Custom topic parameters cannot use reserved names: {param}")
        for param in v:
            if not re.match(r"^[a-zA-Z0-9]+(_[a-zA-Z0-9]+)*$", param):
                raise ValueError(f"Custom topic parameters must be alphanumeric with optional underscores, but no consecutive underscores: {param}")
        return v

    @model_validator(mode="after")
    def validate_topic_values(self) -> "InterfaceTopics":
        if self.property_update_responses == self.method_responses:
            raise ValueError('"propertyUpdateResponses" and "methodResponses" topic templates must be different to avoid routing conflicts')
        return self
