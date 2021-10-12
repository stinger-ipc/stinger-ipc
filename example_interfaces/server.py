class ParamOnlyServer(object):

    def __init__(self, connection):
        self._conn = connection
        self._doubleParam = {'one': 1, 'two': 'two'}
        self._conn.subscribe("ParamOnly/doubleParam/value", self.set_doubleParam)
        self.changed_value_callback_for_doubleParam = None
        self._singleParam = {'foo': 'hello world'}
        self._conn.subscribe("ParamOnly/singleParam/value", self.set_singleParam)
        self.changed_value_callback_for_singleParam = None
        
    
    

    
    def set_doubleParam(self, one, two):
        changed = False
        if one != self._doubleParam['one']:
            changed = True
            self._doubleParam['one'] = one
        if two != self._doubleParam['two']:
            changed = True
            self._doubleParam['two'] = two
        if changed:
            topic = "ParamOnly/doubleParam/value"
            self._conn.publish(topic, self._doubleParam, 1, True)
            if self.changed_value_callback_for_doubleParam is not None:
                self.changed_value_callback_for_doubleParam(one, two)

    def get_doubleParam(self):
        return self._doubleParam
    
    def set_singleParam(self, foo):
        changed = False
        if foo != self._singleParam['foo']:
            changed = True
            self._singleParam['foo'] = foo
        if changed:
            topic = "ParamOnly/singleParam/value"
            self._conn.publish(topic, self._singleParam, 1, True)
            if self.changed_value_callback_for_singleParam is not None:
                self.changed_value_callback_for_singleParam(foo)

    def get_singleParam(self):
        return self._singleParam[args[0].name]
    