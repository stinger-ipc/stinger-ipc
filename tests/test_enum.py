from stingeripc.components import InterfaceEnum
from stingeripc.exceptions import InvalidStingerStructure

import unittest


class TestEnumCreateManually(unittest.TestCase):
    def setUp(self):
        self.enum = InterfaceEnum(name="bread")
        self.enum.add_item("pumpernickel")
        self.enum.add_item("whole wheat")
        self.enum.add_item("french")

    def test_name(self):
        self.assertEqual(self.enum.name, "bread")

    def test_values(self):
        self.assertEqual(len(self.enum.items), 3)

    def test_auto_assigned_integers_start_at_1(self):
        integers = [item.integer for item in self.enum.items]
        self.assertEqual(integers, [1, 2, 3])

    def test_class_name(self):
        self.assertEqual(self.enum.class_name, "Bread")


class TestEnumCreateManuallyWithExplicitIntegers(unittest.TestCase):
    def setUp(self):
        self.enum = InterfaceEnum(name="size")
        self.enum.add_item("small", integer=10)
        self.enum.add_item("medium", integer=20)
        self.enum.add_item("large", integer=30)

    def test_explicit_integers_preserved(self):
        integers = [item.integer for item in self.enum.items]
        self.assertEqual(integers, [10, 20, 30])

    def test_has_value(self):
        self.assertTrue(self.enum.has_value(10))
        self.assertFalse(self.enum.has_value(99))

    def test_auto_integer_continues_from_max(self):
        self.enum.add_item("extra-large")
        self.assertEqual(self.enum.items[-1].integer, 31)


class TestEnumZeroValueReordering(unittest.TestCase):
    def test_zero_value_moved_to_front(self):
        enum = InterfaceEnum(name="state")
        enum.add_item("active", integer=1)
        enum.add_item("unknown", integer=0)
        enum.add_item("inactive", integer=2)
        items = enum.items
        self.assertEqual(items[0].integer, 0)
        self.assertEqual(items[0].name, "unknown")

    def test_zero_already_first_not_reordered(self):
        enum = InterfaceEnum(name="state")
        enum.add_item("unknown", integer=0)
        enum.add_item("active", integer=1)
        items = enum.items
        self.assertEqual(items[0].integer, 0)


class TestSignalCreateFromStinger(unittest.TestCase):
    def setUp(self):
        stinger = {
            "values": [
                {"name": "white"},
                {"name": "blue"},
                {"name": "red"},
            ]
        }
        self.enum = InterfaceEnum.new_enum_from_stinger("color", stinger)

    def test_name(self):
        self.assertEqual(self.enum.name, "color")

    def test_values(self):
        self.assertEqual(len(self.enum.items), 3)

    def test_item_names(self):
        names = [item.name for item in self.enum.items]
        self.assertEqual(names, ["white", "blue", "red"])


class TestEnumFromStingerWithExplicitValues(unittest.TestCase):
    def setUp(self):
        stinger = {
            "values": [
                {"name": "low", "value": 10},
                {"name": "medium", "value": 20},
                {"name": "high", "value": 30},
            ]
        }
        self.enum = InterfaceEnum.new_enum_from_stinger("priority", stinger)

    def test_explicit_values_preserved(self):
        integers = [item.integer for item in self.enum.items]
        self.assertEqual(integers, [10, 20, 30])


class TestEnumFromStingerWithDocumentation(unittest.TestCase):
    def test_documentation_set(self):
        stinger = {
            "documentation": "The type of milk.",
            "values": [{"name": "whole"}, {"name": "skim"}],
        }
        enum = InterfaceEnum.new_enum_from_stinger("milk", stinger)
        self.assertEqual(enum.documentation, "The type of milk.")

    def test_documentation_defaults_to_none(self):
        stinger = {"values": [{"name": "on"}, {"name": "off"}]}
        enum = InterfaceEnum.new_enum_from_stinger("switch", stinger)
        self.assertIsNone(enum.documentation)


class TestEnumFromStingerWithDescriptions(unittest.TestCase):
    def test_item_descriptions(self):
        stinger = {
            "values": [
                {"name": "on", "description": "Powered on"},
                {"name": "off", "description": "Powered off"},
            ]
        }
        enum = InterfaceEnum.new_enum_from_stinger("power", stinger)
        self.assertEqual(enum.items[0].description, "Powered on")
        self.assertEqual(enum.items[1].description, "Powered off")


class TestEnumFromStingerValidationErrors(unittest.TestCase):
    def test_duplicate_integer_values_raises(self):
        stinger = {
            "values": [
                {"name": "a", "value": 1},
                {"name": "b", "value": 1},
            ]
        }
        with self.assertRaises(InvalidStingerStructure):
            InterfaceEnum.new_enum_from_stinger("dupe", stinger)

    def test_empty_values_raises(self):
        with self.assertRaises(InvalidStingerStructure):
            InterfaceEnum.new_enum_from_stinger("empty", {"values": []})

    def test_missing_values_raises(self):
        with self.assertRaises(InvalidStingerStructure):
            InterfaceEnum.new_enum_from_stinger("missing", {})

    def test_invalid_name_pattern_raises(self):
        stinger = {"values": [{"name": "bad!name"}]}
        with self.assertRaises(InvalidStingerStructure):
            InterfaceEnum.new_enum_from_stinger("bad", stinger)

    def test_invalid_version_raises(self):
        stinger = {"values": [{"name": "a"}], "version": "not-a-version"}
        with self.assertRaises(InvalidStingerStructure):
            InterfaceEnum.new_enum_from_stinger("bad", stinger)

