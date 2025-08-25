from abc import ABC, abstractmethod


class AbstractConnection(ABC):

    @abstractmethod
    def publish(self, topic: str, payload: str, qos: int, retain: bool = False):
        pass
