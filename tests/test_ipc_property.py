import unittest
from stingeripc.ipc_property import IpcProperty
from stingeripc.components import StingerSpec, Arg
from stingeripc.config import StingerConfig
from stingeripc.exceptions import InvalidStingerStructure


def _make_stinger_spec():
    stinger = {
        "stingeripc": {"version": "0.3.0"},
        "interface": {"name": "test_iface", "version": "0.0.1"},
    }
    return StingerSpec.new_spec_from_stinger(stinger, StingerConfig())


class TestIpcPropertyCreateManually(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.prop = IpcProperty("myProp", self.spec)

    def test_name(self):
        self.assertEqual(self.prop.name, "myProp")

    def test_version_defaults_to_none(self):
        self.assertIsNone(self.prop.version)

    def test_read_only_defaults_to_false(self):
        self.assertFalse(self.prop.read_only)

    def test_value_before_set_raises(self):
        with self.assertRaises(InvalidStingerStructure):
            self.prop.value

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.prop.documentation)

    def test_set_value(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.prop.set_value(arg)
        self.assertIs(self.prop.value, arg)
        self.assertEqual(len(self.prop.arg_list), 1)
        self.assertEqual(self.prop.arg_list[0].name, "x")

    def test_set_second_value_raises(self):
        self.prop.set_value(Arg.new_arg_from_stinger({"name": "x", "type": "integer"}))
        with self.assertRaises(InvalidStingerStructure):
            self.prop.set_value(Arg.new_arg_from_stinger({"name": "y", "type": "integer"}))


class TestIpcPropertyFromStinger(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.prop_spec = {
            "value": {"name": "temperature", "type": "float"},
        }
        self.prop = IpcProperty.new_property_from_stinger("sensor", self.prop_spec, self.spec)

    def test_name(self):
        self.assertEqual(self.prop.name, "sensor")

    def test_version_defaults_to_none(self):
        self.assertIsNone(self.prop.version)

    def test_read_only_defaults_to_false(self):
        self.assertFalse(self.prop.read_only)

    def test_value_populated(self):
        self.assertEqual(self.prop.value.name, "temperature")

    def test_arg_list_holds_the_single_value(self):
        self.assertEqual([a.name for a in self.prop.arg_list], ["temperature"])

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.prop.documentation)


class TestIpcPropertyFromStingerWithVersion(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.prop = IpcProperty.new_property_from_stinger(
            "sensor",
            {"value": {"name": "x", "type": "integer"}, "version": "2.0.0"},
            self.spec,
        )

    def test_version_set(self):
        self.assertEqual(self.prop.version, "2.0.0")


class TestIpcPropertyFromStingerReadOnly(unittest.TestCase):
    def test_read_only_true(self):
        spec = _make_stinger_spec()
        prop = IpcProperty.new_property_from_stinger(
            "constant",
            {"value": {"name": "x", "type": "integer"}, "readOnly": True},
            spec,
        )
        self.assertTrue(prop.read_only)

    def test_read_only_non_bool_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger(
                "bad",
                {"value": {"name": "x", "type": "integer"}, "readOnly": "yes"},
                spec,
            )


class TestIpcPropertyFromStingerWithDocumentation(unittest.TestCase):
    def test_documentation_set(self):
        spec = _make_stinger_spec()
        prop = IpcProperty.new_property_from_stinger(
            "sensor",
            {"documentation": "Current sensor reading.", "value": {"name": "x", "type": "integer"}},
            spec,
        )
        self.assertEqual(prop.documentation, "Current sensor reading.")

    def test_documentation_defaults_to_none(self):
        spec = _make_stinger_spec()
        prop = IpcProperty.new_property_from_stinger("sensor", {"value": {"name": "x", "type": "integer"}}, spec)
        self.assertIsNone(prop.documentation)


class TestIpcPropertyFromStingerValidationErrors(unittest.TestCase):
    def test_missing_value_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger("bad", {}, spec)

    def test_legacy_values_list_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger("bad", {"values": [{"name": "x", "type": "integer"}]}, spec)

    def test_value_not_a_mapping_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger("bad", {"value": "not_a_mapping"}, spec)

    def test_value_missing_name_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger("bad", {"value": {"type": "integer"}}, spec)

    def test_value_missing_type_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger("bad", {"value": {"name": "x"}}, spec)
