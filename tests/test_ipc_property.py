import unittest
from stingeripc.ipc_property import IpcProperty
from stingeripc.components import StingerSpec, Arg
from stingeripc.config import StingerConfig
from stingeripc.exceptions import InvalidStingerStructure


def _make_stinger_spec():
    stinger = {
        "stingeripc": {"version": "0.0.7"},
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

    def test_initial_arg_list_empty(self):
        self.assertEqual(len(self.prop.arg_list), 0)

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.prop.documentation)

    def test_add_arg(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.prop.add_arg(arg)
        self.assertEqual(len(self.prop.arg_list), 1)
        self.assertEqual(self.prop.arg_list[0].name, "x")

    def test_add_duplicate_arg_raises(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.prop.add_arg(arg)
        with self.assertRaises(InvalidStingerStructure):
            self.prop.add_arg(arg)


class TestIpcPropertyFromStinger(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.prop_spec = {
            "values": [
                {"name": "temperature", "type": "float"},
                {"name": "unit", "type": "string"},
            ],
        }
        self.prop = IpcProperty.new_property_from_stinger("sensor", self.prop_spec, self.spec)

    def test_name(self):
        self.assertEqual(self.prop.name, "sensor")

    def test_version_defaults_to_none(self):
        self.assertIsNone(self.prop.version)

    def test_read_only_defaults_to_false(self):
        self.assertFalse(self.prop.read_only)

    def test_arg_list_populated(self):
        self.assertEqual(len(self.prop.arg_list), 2)

    def test_arg_names(self):
        self.assertEqual([a.name for a in self.prop.arg_list], ["temperature", "unit"])

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.prop.documentation)


class TestIpcPropertyFromStingerWithVersion(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.prop = IpcProperty.new_property_from_stinger(
            "sensor",
            {"values": [{"name": "x", "type": "integer"}], "version": "2.0.0"},
            self.spec,
        )

    def test_version_set(self):
        self.assertEqual(self.prop.version, "2.0.0")


class TestIpcPropertyFromStingerReadOnly(unittest.TestCase):
    def test_read_only_true(self):
        spec = _make_stinger_spec()
        prop = IpcProperty.new_property_from_stinger(
            "constant",
            {"values": [{"name": "x", "type": "integer"}], "readOnly": True},
            spec,
        )
        self.assertTrue(prop.read_only)

    def test_read_only_non_bool_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger(
                "bad",
                {"values": [{"name": "x", "type": "integer"}], "readOnly": "yes"},
                spec,
            )


class TestIpcPropertyFromStingerWithDocumentation(unittest.TestCase):
    def test_documentation_set(self):
        spec = _make_stinger_spec()
        prop = IpcProperty.new_property_from_stinger(
            "sensor",
            {"documentation": "Current sensor reading.", "values": [{"name": "x", "type": "integer"}]},
            spec,
        )
        self.assertEqual(prop.documentation, "Current sensor reading.")

    def test_documentation_defaults_to_none(self):
        spec = _make_stinger_spec()
        prop = IpcProperty.new_property_from_stinger("sensor", {"values": [{"name": "x", "type": "integer"}]}, spec)
        self.assertIsNone(prop.documentation)


class TestIpcPropertyFromStingerValidationErrors(unittest.TestCase):
    def test_missing_values_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger("bad", {}, spec)

    def test_values_not_a_list_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger("bad", {"values": "not_a_list"}, spec)

    def test_arg_missing_name_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger("bad", {"values": [{"type": "integer"}]}, spec)

    def test_arg_missing_type_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcProperty.new_property_from_stinger("bad", {"values": [{"name": "x"}]}, spec)
