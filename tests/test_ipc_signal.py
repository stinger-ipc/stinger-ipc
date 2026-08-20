import unittest
from stingeripc.ipc_signal import IpcSignal
from stingeripc.components import StingerSpec, Arg
from stingeripc.config import StingerConfig
from stingeripc.exceptions import InvalidStingerStructure


def _make_stinger_spec():
    stinger = {
        "stingeripc": {"version": "0.3.0"},
        "interface": {"name": "test_iface", "version": "0.0.1"},
    }
    return StingerSpec.new_spec_from_stinger(stinger, StingerConfig())


class TestIpcSignalCreateManually(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.signal = IpcSignal("mySignal", self.spec)

    def test_name(self):
        self.assertEqual(self.signal.name, "mySignal")

    def test_version_defaults_to_none(self):
        self.assertIsNone(self.signal.version)

    def test_initial_arg_list_empty(self):
        self.assertEqual(len(self.signal.arg_list), 0)

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.signal.documentation)

    def test_add_arg(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.signal.add_arg(arg)
        self.assertEqual(len(self.signal.arg_list), 1)
        self.assertEqual(self.signal.arg_list[0].name, "x")

    def test_add_duplicate_arg_raises(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.signal.add_arg(arg)
        with self.assertRaises(InvalidStingerStructure):
            self.signal.add_arg(arg)


class TestIpcSignalFromStinger(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.signal_spec = {
            "values": [
                {"name": "temperature", "type": "float"},
                {"name": "humidity", "type": "float"},
            ],
        }
        self.signal = IpcSignal.new_signal_from_stinger("reading", self.signal_spec, self.spec)

    def test_name(self):
        self.assertEqual(self.signal.name, "reading")

    def test_version_defaults_to_none(self):
        self.assertIsNone(self.signal.version)

    def test_arg_list_populated(self):
        self.assertEqual(len(self.signal.arg_list), 2)

    def test_arg_names(self):
        self.assertEqual([a.name for a in self.signal.arg_list], ["temperature", "humidity"])

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.signal.documentation)


class TestIpcSignalFromStingerWithVersion(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.signal = IpcSignal.new_signal_from_stinger(
            "reading",
            {"values": [{"name": "x", "type": "integer"}], "version": "1.0.0"},
            self.spec,
        )

    def test_version_set(self):
        self.assertEqual(self.signal.version, "1.0.0")


class TestIpcSignalFromStingerWithDocumentation(unittest.TestCase):
    def test_documentation_set(self):
        spec = _make_stinger_spec()
        signal = IpcSignal.new_signal_from_stinger(
            "reading",
            {"documentation": "A sensor reading.", "values": [{"name": "x", "type": "integer"}]},
            spec,
        )
        self.assertEqual(signal.documentation, "A sensor reading.")

    def test_documentation_defaults_to_none(self):
        spec = _make_stinger_spec()
        signal = IpcSignal.new_signal_from_stinger("reading", {"values": [{"name": "x", "type": "integer"}]}, spec)
        self.assertIsNone(signal.documentation)


class TestIpcSignalFromStingerValidationErrors(unittest.TestCase):
    def test_missing_values_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcSignal.new_signal_from_stinger("bad", {}, spec)

    def test_values_not_a_list_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcSignal.new_signal_from_stinger("bad", {"values": "not_a_list"}, spec)

    def test_arg_missing_name_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcSignal.new_signal_from_stinger("bad", {"values": [{"type": "integer"}]}, spec)

    def test_arg_missing_type_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcSignal.new_signal_from_stinger("bad", {"values": [{"name": "x"}]}, spec)
