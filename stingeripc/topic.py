from typing import Optional


class TopicCreatorBase:
    def __init__(self, root: Optional[str] = None):
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
    def __init__(self, root: str):
        super().__init__(root)

    def signal_topic(self, signal_name: str) -> str:
        return self.slash("signal", signal_name)

class MethodTopicCreator(TopicCreatorBase):
    def __init__(self, root: str):
        super().__init__(root)

    def method_topic(self, method_name: str) -> str:
        return self.slash("method", method_name)

    def method_response_topic(self, method_name: str, client_id: str) -> str:
        method_topic = self.method_topic(method_name)
        return f"client/{client_id}/{method_topic}/response"

class InterfaceTopicCreator(TopicCreatorBase):
    """Helper class for creating MQTT topics for various stinger elements."""

    def __init__(self, interface_name: str, root: Optional[str] = None):
        super().__init__(root)
        self._interface_name = interface_name

    @property
    def _topic_prefix(self) -> str:
        return self.slash(self._interface_name)

    def interface_info_topic(self) -> str:
        return f"{self._topic_prefix}/interface"

    def signal_topic_creator(self) -> SignalTopicCreator:
        return SignalTopicCreator(self._topic_prefix)

    def method_topic_creator(self) -> MethodTopicCreator:
        return MethodTopicCreator(self._topic_prefix)
