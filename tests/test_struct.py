import unittest
from stingeripc.arg_datatypes import InterfaceStruct
from stingeripc.arg_models import Arg
from stingeripc.components import StingerSpec
from stingeripc.config import StingerConfig
from stingeripc.exceptions import InvalidStingerStructure


def _make_stinger_spec(extra_structs=None, extra_enums=None):
    """Helper: build a minimal StingerSpec, optionally with structs/enums."""
    stinger = {
        "stingeripc": {"version": "0.3.0"},
        "interface": {"name": "test_iface", "version": "0.0.1"},
    }
    if extra_structs:
        stinger["structs"] = extra_structs
    if extra_enums:
        stinger["enums"] = extra_enums
    return StingerSpec.new_spec_from_stinger(stinger, StingerConfig())


class TestInterfaceStructCreateManually(unittest.TestCase):
    def setUp(self):
        self.struct = InterfaceStruct(name="point")

    def test_name(self):
        self.assertEqual(self.struct.name, "point")

    def test_initial_values_empty(self):
        self.assertEqual(len(self.struct.values), 0)

    def test_class_name(self):
        self.assertEqual(self.struct.class_name, "Point")

    def test_class_name_snake_case(self):
        struct = InterfaceStruct(name="my_data_type")
        self.assertEqual(struct.class_name, "MyDataType")

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.struct.documentation)

    def test_add_value(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "float"})
        self.struct.add_value(arg)
        self.assertEqual(len(self.struct.values), 1)
        self.assertEqual(self.struct.values[0].name, "x")

    def test_multiple_values(self):
        for name, typ in [("x", "float"), ("y", "float"), ("label", "string")]:
            self.struct.add_value(Arg.new_arg_from_stinger({"name": name, "type": typ}))
        self.assertEqual(len(self.struct.values), 3)
        self.assertEqual([v.name for v in self.struct.values], ["x", "y", "label"])


class TestInterfaceStructFromStinger(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.stinger_spec = {
            "values": [
                {"name": "x", "type": "float"},
                {"name": "y", "type": "float"},
            ]
        }
        self.struct = InterfaceStruct.new_struct_from_stinger("point", self.stinger_spec, self.spec)

    def test_name(self):
        self.assertEqual(self.struct.name, "point")

    def test_value_count(self):
        self.assertEqual(len(self.struct.values), 2)

    def test_value_names(self):
        self.assertEqual([v.name for v in self.struct.values], ["x", "y"])


class TestInterfaceStructFromStingerWithDocumentation(unittest.TestCase):
    def test_documentation_set(self):
        spec = _make_stinger_spec()
        stinger_spec = {
            "documentation": "A 2D point.",
            "values": [{"name": "x", "type": "float"}],
        }
        struct = InterfaceStruct.new_struct_from_stinger("point", stinger_spec, spec)
        self.assertEqual(struct.documentation, "A 2D point.")

    def test_documentation_defaults_to_none(self):
        spec = _make_stinger_spec()
        struct = InterfaceStruct.new_struct_from_stinger("point", {"values": [{"name": "x", "type": "float"}]}, spec)
        self.assertIsNone(struct.documentation)


class TestInterfaceStructFromStingerNoValues(unittest.TestCase):
    def test_no_values_key(self):
        spec = _make_stinger_spec()
        struct = InterfaceStruct.new_struct_from_stinger("empty", {}, spec)
        self.assertEqual(len(struct.values), 0)

    def test_empty_values_list(self):
        spec = _make_stinger_spec()
        struct = InterfaceStruct.new_struct_from_stinger("empty", {"values": []}, spec)
        self.assertEqual(len(struct.values), 0)


class TestInterfaceStructFromStingerValidationErrors(unittest.TestCase):
    def test_non_dict_value_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            InterfaceStruct.new_struct_from_stinger("bad", {"values": ["not_a_dict"]}, spec)

    def test_value_missing_type_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            InterfaceStruct.new_struct_from_stinger("bad", {"values": [{"name": "x"}]}, spec)

    def test_non_string_documentation_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            InterfaceStruct.new_struct_from_stinger("bad", {"documentation": 42, "values": []}, spec)
