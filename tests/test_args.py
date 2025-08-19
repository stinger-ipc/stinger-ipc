import unittest
from stingeripc.components import Arg, ArgPrimitive, InvalidStingerStructure
from stingeripc.args import ArgPrimitiveType

class TestArgCreationFromSpec(unittest.TestCase):

    def setUp(self):
        self.spec_objs = [
            {"name": "one", "type": "integer", "python_type": "int", "value_type": ArgPrimitiveType.INTEGER},
            {"name": "two", "type": "float", "python_type": "float", "value_type": ArgPrimitiveType.FLOAT},
            {"name": "three", "type": "boolean", "python_type": "bool", "value_type": ArgPrimitiveType.BOOLEAN},
            {"name": "four", "type": "string", "python_type": "str", "value_type": ArgPrimitiveType.STRING},
        ]

    def test_arg(self):
        for obj in self.spec_objs:
            with self.subTest(obj):
                arg = Arg.new_arg_from_stinger(obj)
                self.assertEqual(arg.name, obj['name'])
                self.assertEqual(arg.python_type, obj['python_type'])
                self.assertEqual(arg.type, obj['value_type'])
                example = arg.get_random_example_value()
                real_python_type = eval(arg.python_type)
                self.assertIsInstance(example, real_python_type)


class TestInvalidArgCreation(unittest.TestCase):

    def test_not_an_arg_type_from_spec(self):
        with self.assertRaises(InvalidStingerStructure):
            ArgPrimitive.new_arg_primitive_from_stinger({"name": "one", "type": "double"})

    def test_not_an_arg_type(self):
        with self.assertRaises(InvalidStingerStructure):
            ArgPrimitiveType.from_string("unsigned int")

    def test_arg_primitive_name_missing(self):
        with self.assertRaises(InvalidStingerStructure):
            ArgPrimitive.new_arg_primitive_from_stinger({"type": "integer"})  

    def test_arg_name_missing(self):
        with self.assertRaises(InvalidStingerStructure):
            Arg.new_arg_primitive_from_stinger({"type": "integer"})  
    
    def test_arg_primitive_type_missing(self):
        with self.assertRaises(InvalidStingerStructure):
            ArgPrimitive.new_arg_primitive_from_stinger({"name": "foo"})  

    def test_arg_type_missing(self):
        with self.assertRaises(InvalidStingerStructure):
            Arg.new_arg_primitive_from_stinger({"name": "foo"})  

class TestPythonTypes(unittest.TestCase):

    def test_from_invalid_input(self):
        with self.assertRaises(InvalidStingerStructure):
            ArgPrimitiveType.to_python_type(-1)