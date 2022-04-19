import unittest
from stingeripc.components import Arg, ArgValueType

class TestArgCreationFromSpec(unittest.TestCase):

    def setUp(self):
        self.spec_objs = [
            {"name": "one", "type": "integer", "python_type": "int", "value_type": ArgValueType.INTEGER},
            {"name": "two", "type": "float", "python_type": "float", "value_type": ArgValueType.FLOAT},
            {"name": "three", "type": "boolean", "python_type": "bool", "value_type": ArgValueType.BOOLEAN},
            {"name": "four", "type": "string", "python_type": "str", "value_type": ArgValueType.STRING},
        ]

    def test_arg(self):
        for obj in self.spec_objs:
            with self.subTest(obj):
                arg = Arg.new_from_stinger(obj)
                self.assertEqual(arg.name, obj['name'])
                self.assertEqual(arg.python_type, obj['python_type'])
                self.assertEqual(arg.type, obj['value_type'])
