import json

class SignalOnlyServer(object):

    def __init__(self, connection):
        self._conn = connection
        
    
    def emit_theSignal():
        payload = {
        }
        self._conn.publish("SignalOnly/signal/theSignal", json.dumps(payload), qos=1, retain=False)

    def emit_anotherSignal(one: float, two: bool, three: str):
        payload = {
            "one": one, 
            "two": two, 
            "three": three, 
        }
        self._conn.publish("SignalOnly/signal/anotherSignal", json.dumps(payload), qos=1, retain=False)

    

    