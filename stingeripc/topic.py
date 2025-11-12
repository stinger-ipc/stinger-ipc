from typing import Optional
from jacobsjinjatoo import stringmanip

class TopicCreatorBase:
    def __init__(self, placeholder: str, root: Optional[str] = None):
        self._placeholder = placeholder
        if root is None:
            self._base_topic = None
        else:
            self._base_topic = root.strip("/")

    def slash(self, *args) -> str:
        if self._base_topic is None:
            return "/".join(args)
        else:
            return f"{self._base_topic}/{'/'.join(args)}"


class SignalTopicCreator(TopicCreatorBase):
    def __init__(self, placeholder: str, root: str):
        super().__init__(placeholder, root)

    def signal_topic(self, signal_name: str) -> str:
        return self.slash("signal", stringmanip.lower_camel_case(signal_name))


class MethodTopicCreator(TopicCreatorBase):
    def __init__(self, placeholder: str, root: str):
        super().__init__(placeholder, root)

    def method_topic(self, method_name: str) -> str:
        return self.slash("method", stringmanip.lower_camel_case(method_name))

    def method_response_topic(self, method_name: str, namespace: str, client_id: str) -> str:
        return f"client/{client_id}/{namespace}/methodResponse"


class PropertyTopicCreator(TopicCreatorBase):
    def __init__(self, placeholder: str, root: str):
        super().__init__(placeholder, root)

    def property_value_topic(self, property_name: str) -> str:
        return self.slash("property", stringmanip.lower_camel_case(property_name), "value")

    def property_update_topic(self, property_name: str) -> str:
        return self.slash("property", stringmanip.lower_camel_case(property_name), "setValue")

    def property_response_topic(self, property_name: str, namespace: str, client_id: str) -> str:
        return f"client/{client_id}/{namespace}/propertyUpdateResponse"

class InterfaceTopicCreator(TopicCreatorBase):
    """Helper class for creating MQTT topics for various stinger elements."""

    def __init__(self, interface_name: str, placeholder: str, root: Optional[str] = None):
        super().__init__(placeholder, root)
        self._interface_name = stringmanip.lower_camel_case(interface_name)

    @property
    def _topic_prefix(self) -> str:
        return self.slash(self._interface_name, self._placeholder)

    def interface_info_topic(self) -> str:
        return f"{self._topic_prefix}/interface"

    def signal_topic_creator(self) -> SignalTopicCreator:
        return SignalTopicCreator(self._placeholder, self._topic_prefix)

    def method_topic_creator(self) -> MethodTopicCreator:
        return MethodTopicCreator(self._placeholder, self._topic_prefix)

    def property_topic_creator(self) -> PropertyTopicCreator:
        return PropertyTopicCreator(self._placeholder, self._topic_prefix)
