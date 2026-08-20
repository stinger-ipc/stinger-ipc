import unittest
from stingeripc.ipc_method import IpcMethod
from stingeripc.components import StingerSpec, Arg
from stingeripc.config import StingerConfig
from stingeripc.exceptions import InvalidStingerStructure


def _make_stinger_spec():
    stinger = {
        "stingeripc": {"version": "0.3.0"},
        "interface": {"name": "test_iface", "version": "0.0.1"},
    }
    return StingerSpec.new_spec_from_stinger(stinger, StingerConfig())


class TestIpcMethodCreateManually(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.method = IpcMethod("myMethod", self.spec)

    def test_name(self):
        self.assertEqual(self.method.name, "myMethod")

    def test_version_defaults_to_none(self):
        self.assertIsNone(self.method.version)

    def test_initial_arg_list_empty(self):
        self.assertEqual(len(self.method.arg_list), 0)

    def test_initial_return_arg_list_empty(self):
        self.assertEqual(len(self.method.return_arg_list), 0)

    def test_initial_return_value_none(self):
        self.assertIsNone(self.method.return_value)

    def test_add_arg(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.method.add_arg(arg)
        self.assertEqual(len(self.method.arg_list), 1)
        self.assertEqual(self.method.arg_list[0].name, "x")

    def test_add_duplicate_arg_raises(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.method.add_arg(arg)
        with self.assertRaises(InvalidStingerStructure):
            self.method.add_arg(arg)

    def test_set_return_value(self):
        arg = Arg.new_arg_from_stinger({"name": "result", "type": "string"})
        self.method.set_return_value(arg)
        self.assertEqual(len(self.method.return_arg_list), 1)
        self.assertIs(self.method.return_value, arg)

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.method.documentation)


class TestIpcMethodFromStinger(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.method_spec = {
            "arguments": [
                {"name": "x", "type": "integer"},
                {"name": "y", "type": "float"},
            ],
            "returnValue": {"name": "result", "type": "string"},
        }
        self.method = IpcMethod.new_method_from_stinger("add", self.method_spec, self.spec)

    def test_name(self):
        self.assertEqual(self.method.name, "add")

    def test_version_defaults_to_none(self):
        self.assertIsNone(self.method.version)

    def test_arg_list_populated(self):
        self.assertEqual(len(self.method.arg_list), 2)

    def test_arg_names(self):
        self.assertEqual([a.name for a in self.method.arg_list], ["x", "y"])

    def test_return_arg_list_populated(self):
        self.assertEqual(len(self.method.return_arg_list), 1)

    def test_return_value_single(self):
        self.assertIsInstance(self.method.return_value, Arg)
        self.assertEqual(self.method.return_value.name, "result")

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.method.documentation)


class TestIpcMethodFromStingerWithVersion(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.method_spec = {
            "arguments": [
                {"name": "x", "type": "integer"},
            ],
            "version": "2.1.0",
        }
        self.method = IpcMethod.new_method_from_stinger("add", self.method_spec, self.spec)

    def test_version_set(self):
        self.assertEqual(self.method.version, "2.1.0")


class TestIpcMethodFromStingerWithDocumentation(unittest.TestCase):
    def test_documentation_set(self):
        spec = _make_stinger_spec()
        method_spec = {
            "documentation": "Adds two numbers.",
            "arguments": [{"name": "x", "type": "integer"}],
        }
        method = IpcMethod.new_method_from_stinger("add", method_spec, spec)
        self.assertEqual(method.documentation, "Adds two numbers.")

    def test_documentation_defaults_to_none(self):
        spec = _make_stinger_spec()
        method = IpcMethod.new_method_from_stinger("add", {"arguments": [{"name": "x", "type": "integer"}]}, spec)
        self.assertIsNone(method.documentation)


class TestIpcMethodFromStingerNoReturnValue(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.method = IpcMethod.new_method_from_stinger("noop", {"arguments": [{"name": "x", "type": "integer"}]}, self.spec)

    def test_no_return_value(self):
        self.assertIsNone(self.method.return_value)
        self.assertEqual(len(self.method.return_arg_list), 0)

    def test_return_value_type_false(self):
        self.assertFalse(self.method.return_value_type)


class TestIpcMethodFromStingerValidationErrors(unittest.TestCase):
    def test_missing_arguments_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcMethod.new_method_from_stinger("bad", {}, spec)

    def test_arguments_not_a_list_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcMethod.new_method_from_stinger("bad", {"arguments": "not_a_list"}, spec)

    def test_arg_missing_name_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcMethod.new_method_from_stinger("bad", {"arguments": [{"type": "integer"}]}, spec)

    def test_arg_missing_type_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcMethod.new_method_from_stinger("bad", {"arguments": [{"name": "x"}]}, spec)

    def test_return_value_not_a_mapping_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcMethod.new_method_from_stinger(
                "bad",
                {"arguments": [{"name": "x", "type": "integer"}], "returnValue": [{"name": "result", "type": "string"}]},
                spec,
            )

    def test_return_value_missing_name_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcMethod.new_method_from_stinger(
                "bad",
                {"arguments": [{"name": "x", "type": "integer"}], "returnValue": {"type": "string"}},
                spec,
            )

    def test_return_value_missing_type_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcMethod.new_method_from_stinger(
                "bad",
                {"arguments": [{"name": "x", "type": "integer"}], "returnValue": {"name": "result"}},
                spec,
            )

    def test_legacy_return_values_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcMethod.new_method_from_stinger(
                "bad",
                {"arguments": [{"name": "x", "type": "integer"}], "returnValues": [{"name": "result", "type": "string"}]},
                spec,
            )


class TestIpcMethodReturnValueProperties(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()

    def test_return_value_name_no_return(self):
        method = IpcMethod.new_method_from_stinger("noop", {"arguments": [{"name": "x", "type": "integer"}]}, self.spec)
        self.assertEqual(method.return_value_name, "noop return value")

    def test_return_value_name_single_return(self):
        method = IpcMethod.new_method_from_stinger("add", {"arguments": [{"name": "x", "type": "integer"}], "returnValue": {"name": "result", "type": "integer"}}, self.spec)
        self.assertEqual(method.return_value_name, "add return value")

    def test_return_value_property_name(self):
        method = IpcMethod.new_method_from_stinger("add", {"arguments": [{"name": "x", "type": "integer"}], "returnValue": {"name": "result", "type": "integer"}}, self.spec)
        self.assertEqual(method.return_value_property_name, "result")

    def test_return_value_property_name_no_return(self):
        method = IpcMethod.new_method_from_stinger("noop", {"arguments": [{"name": "x", "type": "integer"}]}, self.spec)
        self.assertEqual(method.return_value_property_name, "noop")

    def test_return_value_type_single(self):
        method = IpcMethod.new_method_from_stinger("add", {"arguments": [{"name": "x", "type": "integer"}], "returnValue": {"name": "result", "type": "string"}}, self.spec)
        self.assertEqual(method.return_value_type, "primitive")


class TestIpcMethodReturnValueRandomExample(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()

    def test_random_example_no_return(self):
        method = IpcMethod.new_method_from_stinger("noop", {"arguments": [{"name": "x", "type": "integer"}]}, self.spec)
        self.assertEqual(method.get_return_value_random_example_value("python"), "None")
        self.assertEqual(method.get_return_value_random_example_value("cpp"), "nullptr")

    def test_random_example_single_return(self):
        method = IpcMethod.new_method_from_stinger("add", {"arguments": [{"name": "x", "type": "integer"}], "returnValue": {"name": "result", "type": "integer"}}, self.spec)
        example = method.get_return_value_random_example_value("python")
        self.assertIsInstance(example, int)

    def test_random_example_unsupported_lang_raises(self):
        method = IpcMethod.new_method_from_stinger("noop", {"arguments": [{"name": "x", "type": "integer"}]}, self.spec)
        with self.assertRaises(RuntimeError):
            method.get_return_value_random_example_value("ruby")


class TestIpcMethodSecondReturnValue(unittest.TestCase):
    def test_setting_a_second_return_value_raises(self):
        spec = _make_stinger_spec()
        method = IpcMethod("test", spec)
        method.set_return_value(Arg.new_arg_from_stinger({"name": "sum", "type": "integer"}))
        with self.assertRaises(InvalidStingerStructure):
            method.set_return_value(Arg.new_arg_from_stinger({"name": "count", "type": "integer"}))
