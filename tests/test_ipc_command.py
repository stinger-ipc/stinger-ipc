import unittest
from stingeripc.ipc_command import IpcCommand
from stingeripc.components import StingerSpec, Arg
from stingeripc.config import StingerConfig
from stingeripc.exceptions import InvalidStingerStructure


def _make_stinger_spec():
    stinger = {
        "stingeripc": {"version": "0.3.0"},
        "interface": {"name": "test_iface", "version": "0.0.1"},
    }
    return StingerSpec.new_spec_from_stinger(stinger, StingerConfig())


class TestIpcCommandCreateManually(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.command = IpcCommand("myCommand", self.spec)

    def test_name(self):
        self.assertEqual(self.command.name, "myCommand")

    def test_version_defaults_to_none(self):
        self.assertIsNone(self.command.version)

    def test_initial_arg_list_empty(self):
        self.assertEqual(len(self.command.arg_list), 0)

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.command.documentation)

    def test_add_arg(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.command.add_arg(arg)
        self.assertEqual(len(self.command.arg_list), 1)
        self.assertEqual(self.command.arg_list[0].name, "x")

    def test_add_duplicate_arg_raises(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.command.add_arg(arg)
        with self.assertRaises(InvalidStingerStructure):
            self.command.add_arg(arg)


class TestIpcCommandFromStinger(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.command_spec = {
            "arguments": [
                {"name": "temperature", "type": "float"},
                {"name": "humidity", "type": "float"},
            ],
        }
        self.command = IpcCommand.new_command_from_stinger("set_climate", self.command_spec, self.spec)

    def test_name(self):
        self.assertEqual(self.command.name, "set_climate")

    def test_version_defaults_to_none(self):
        self.assertIsNone(self.command.version)

    def test_arg_list_populated(self):
        self.assertEqual(len(self.command.arg_list), 2)

    def test_arg_names(self):
        self.assertEqual([a.name for a in self.command.arg_list], ["temperature", "humidity"])

    def test_documentation_defaults_to_none(self):
        self.assertIsNone(self.command.documentation)

    def test_no_arguments_is_allowed(self):
        command = IpcCommand.new_command_from_stinger("ping", {"arguments": []}, self.spec)
        self.assertEqual(len(command.arg_list), 0)


class TestIpcCommandTopic(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.command = IpcCommand.new_command_from_stinger("set_climate", {"arguments": []}, self.spec)

    def test_topic_fills_in_interface_and_command_name(self):
        self.assertEqual(self.command.topic(), "test_iface/{service_id}/command/set_climate")

    def test_all_commands_topic_uses_wildcard(self):
        self.assertEqual(self.spec.all_commands_topic(), "test_iface/{service_id}/command/+")


class TestIpcCommandFromStingerWithVersion(unittest.TestCase):
    def setUp(self):
        self.spec = _make_stinger_spec()
        self.command = IpcCommand.new_command_from_stinger(
            "set_climate",
            {"arguments": [{"name": "x", "type": "integer"}], "version": "1.0.0"},
            self.spec,
        )

    def test_version_set(self):
        self.assertEqual(self.command.version, "1.0.0")


class TestIpcCommandFromStingerWithDocumentation(unittest.TestCase):
    def test_documentation_set(self):
        spec = _make_stinger_spec()
        command = IpcCommand.new_command_from_stinger(
            "set_climate",
            {"documentation": "Change the climate.", "arguments": [{"name": "x", "type": "integer"}]},
            spec,
        )
        self.assertEqual(command.documentation, "Change the climate.")

    def test_documentation_defaults_to_none(self):
        spec = _make_stinger_spec()
        command = IpcCommand.new_command_from_stinger("set_climate", {"arguments": [{"name": "x", "type": "integer"}]}, spec)
        self.assertIsNone(command.documentation)


class TestIpcCommandFromStingerValidationErrors(unittest.TestCase):
    def test_missing_arguments_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcCommand.new_command_from_stinger("bad", {}, spec)

    def test_arguments_not_a_list_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcCommand.new_command_from_stinger("bad", {"arguments": "not_a_list"}, spec)

    def test_arg_missing_name_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcCommand.new_command_from_stinger("bad", {"arguments": [{"type": "integer"}]}, spec)

    def test_arg_missing_type_raises(self):
        spec = _make_stinger_spec()
        with self.assertRaises(InvalidStingerStructure):
            IpcCommand.new_command_from_stinger("bad", {"arguments": [{"name": "x"}]}, spec)


class TestStingerSpecCommands(unittest.TestCase):
    def setUp(self):
        stinger = {
            "stingeripc": {"version": "0.3.0"},
            "interface": {"name": "test_iface", "version": "0.0.1"},
            "commands": {
                "set_climate": {"arguments": [{"name": "temperature", "type": "float"}]},
                "ping": {"arguments": []},
            },
        }
        self.spec = StingerSpec.new_spec_from_stinger(stinger, StingerConfig())

    def test_commands_are_registered(self):
        self.assertEqual(sorted(self.spec.commands.keys()), ["ping", "set_climate"])

    def test_command_args_are_parsed(self):
        self.assertEqual([a.name for a in self.spec.commands["set_climate"].arg_list], ["temperature"])

    def test_no_commands_yields_empty_dict(self):
        stinger = {
            "stingeripc": {"version": "0.3.0"},
            "interface": {"name": "test_iface", "version": "0.0.1"},
        }
        spec = StingerSpec.new_spec_from_stinger(stinger, StingerConfig())
        self.assertEqual(spec.commands, {})

    def test_command_args_are_collected_for_schema_detection(self):
        stinger = {
            "stingeripc": {"version": "0.3.0"},
            "interface": {"name": "test_iface", "version": "0.0.1"},
            "commands": {
                "set_climate": {"arguments": [{"name": "temperature", "type": "integer", "schema": {"minimum": 0}}]},
            },
        }
        spec = StingerSpec.new_spec_from_stinger(stinger, StingerConfig())
        self.assertTrue(spec.uses_schemas())
