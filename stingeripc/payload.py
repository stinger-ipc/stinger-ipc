def get_initial_value(initial_value, name):
    if initial_value is None:
        return None
    else:
        return initial_value[name]


def payload_parser(payload_obj, initialValue=None):
    if "schema" in payload_obj:
        return [
            {
                "cpptype": "Json",
                "value": payload_obj["initialValue"],
                "name": "json",
            }
        ]
    assert "args" in payload_obj
    args = []
    for ak, av in payload_obj["args"].items():
        args.append(
            {
                "cpptype": "void",
                "value": get_initial_value(initialValue, ak),
                "name": ak,
            }
        )
    return args
