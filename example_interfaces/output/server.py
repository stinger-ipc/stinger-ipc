import json
from connection import MqttConnection

class SignalOnlyServer(object):

    def __init__(self, connection: MqttConnection):
        self._conn = connection
        
    
    def emit_theSignal(self, ):
        payload = {
        }
        self._conn.publish("SignalOnly/signal/theSignal", json.dumps(payload), qos=1, retain=False)

    def emit_anotherSignal(self, one: float, two: bool, three: str):
        payload = {
            "one": one, 
            "two": two, 
            "three": three, 
        }
        self._conn.publish("SignalOnly/signal/anotherSignal", json.dumps(payload), qos=1, retain=False)

    

    

if __name__ == '__main__':
    from time import sleep

    conn = MqttConnection('localhost', 1883)
    server = SignalOnlyServer(conn)

    server.emit_theSignal()
    server.emit_anotherSignal(2.5, False, "apples")
    

    sleep(4)

    server.emit_theSignal()
    server.emit_anotherSignal(one=2.5, two=False, three="apples")

    sleep(2)
    