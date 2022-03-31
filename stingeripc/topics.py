class TopicCreator(object):
    """Helper class for creating MQTT topics for various stinger elements."""

    def __init__(self, root: str = ""):
        self.root = root

    def _get_base(self, name: str, multi: bool) -> str:
        ext = ""
        if multi:
            ext = "%s/"
        b = f"{self.root}{name}/{ext}"
        return b

    def _get_param_base(self, interface_name: str, multi: bool, param_name: str, objects=None) -> str:
        if objects is None:
            objects = []
        t = self._get_base(interface_name, multi)
        t += "/".join(objects)
        t += f"{param_name}/"
        return t

    def get_param_set(self, interface_name: str, multi: bool, param_name: str, objects=None) -> str:
        t = self._get_param_base(interface_name, multi, param_name, objects)
        t += "set"
        return t

    def get_param_value(self, interface_name: str, multi: bool, param_name: str, objects=None) -> str:
        t = self._get_param_base(interface_name, multi, param_name, objects)
        t += "value"
        return t
