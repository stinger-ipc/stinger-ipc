
class TopicCreator(object):

    def __init__(self, root=''):
        self.root = root
    
    def _get_base(self, name, multi):
        ext = ""
        if multi:
            ext = "%s/"
        b = f"{self.root}{name}/{ext}"
        return b

    def _get_param_base(self, interface_name, multi, paramName, objects=None):
        if objects is None:
            objects = []
        t = self._get_base(interface_name, multi)
        t += "/".join(objects)
        t += f"{paramName}/"
        return t

    def get_param_set(self, interface_name, multi, paramName, objects=None):
        t = self._get_param_base(interface_name, multi, paramName, objects)
        t += "set"
        return t

    def get_param_value(self, interface_name, multi, paramName, objects=None):
        t = self._get_param_base(interface_name, multi, paramName, objects)
        t += "value"
        return t