class SignalOnlyServer(object):

    def __init__(self, connection):
        self._conn = connection
        
    
    def emit_theSignal():
        self._conn.publish("SignalOnly/signal/theSignal")

    def emit_anotherSignal(one, two, three, ):
        self._conn.publish("SignalOnly/signal/anotherSignal")

    

    