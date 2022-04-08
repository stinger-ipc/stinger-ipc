from stinger.connection import AbstractConnection

class MockConnection(AbstractConnection):

    def __init__(self):
        self.last_published = (None, None, None, None)
    
    def publish(topic: str, payload: str, qos: int, retain:bool=False):
        self.last_published = (topic, payload, qos, retain)
