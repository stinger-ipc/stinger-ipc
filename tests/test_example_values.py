"""Tests that generated example values respect an argument's ``schema`` constraint.

Example values feed the generated demos, tests, and documentation, so a value that does
not satisfy its argument's constraint would make the generated code reject its own
examples.
"""

import random
import unittest

import jsonschema_rs

from stingeripc.components import Arg, StingerSpec
from stingeripc.config import StingerConfig
from stingeripc.exceptions import InvalidStingerStructure

SEEDS = range(1, 12)


def _root():
    stinger = {
        "stingeripc": {"version": "0.3.0"},
        "interface": {"name": "test_iface", "version": "0.0.1"},
        "enums": {
            "Numbers": {
                "values": [
                    {"name": "one", "value": 1},
                    {"name": "two", "value": 2},
                    {"name": "three", "value": 3},
                ]
            }
        },
    }
    return StingerSpec.new_spec_from_stinger(stinger, StingerConfig())


def _unquote(value):
    """Turn a rendered Python example back into the JSON value it stands for."""
    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


class TestUnconstrainedExamplesAreUnchanged(unittest.TestCase):
    """An argument with no constraint keeps the example value it always had."""

    def test_known_values_per_type(self):
        expected = {
            "integer": 42,
            "float": 3.14,
            "string": '"apples"',
            "boolean": True,
        }
        for arg_type, want in expected.items():
            with self.subTest(arg_type):
                arg = Arg.new_arg_from_stinger({"name": "x", "type": arg_type})
                self.assertEqual(arg.get_random_example_value("python", seed=2), want)

    def test_values_still_vary_by_seed(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        values = {arg.get_random_example_value("python", seed=seed) for seed in SEEDS}
        self.assertGreater(len(values), 1)


class TestConstrainedPrimitiveExamples(unittest.TestCase):
    """Every example value satisfies the argument's constraint, for every seed."""

    CASES = [
        ("integer_tight_max", "integer", {"minimum": 1, "maximum": 12}),
        ("integer_range", "integer", {"minimum": 0, "maximum": 100}),
        ("integer_exclusive_max", "integer", {"minimum": 0, "maximum": 10, "exclusiveMaximum": True}),
        ("integer_exclusive_min", "integer", {"minimum": 5, "exclusiveMinimum": True, "maximum": 9}),
        ("integer_multiple_of", "integer", {"minimum": 1, "maximum": 50, "multipleOf": 7}),
        ("integer_enum", "integer", {"enum": [7, 8, 9]}),
        ("integer_min_only", "integer", {"minimum": 100000}),
        ("integer_max_only", "integer", {"maximum": -5}),
        ("float_unit_range", "float", {"minimum": 0.0, "maximum": 1.0}),
        ("float_min_only", "float", {"minimum": 1000.5}),
        ("string_short", "string", {"minLength": 1, "maxLength": 4}),
        ("string_long", "string", {"minLength": 40}),
        ("string_exact", "string", {"minLength": 6, "maxLength": 6}),
        ("string_enum", "string", {"enum": ["alpha", "beta"]}),
    ]

    def test_examples_conform(self):
        for label, arg_type, schema in self.CASES:
            arg = Arg.new_arg_from_stinger({"name": "x", "type": arg_type, "schema": schema})
            validator = jsonschema_rs.Draft4Validator(schema)
            for seed in SEEDS:
                with self.subTest(label=label, seed=seed):
                    example = _unquote(arg.get_random_example_value("python", seed=seed))
                    self.assertTrue(validator.is_valid(example), f"{example!r} violates {schema}")

    def test_examples_conform_in_every_language(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer", "schema": {"minimum": 1, "maximum": 12}})
        for lang in ("python", "rust", "c++", "json"):
            with self.subTest(lang):
                self.assertIn(arg.get_random_example_value(lang, seed=2), (5, "5"))


class TestConstrainedEnumExamples(unittest.TestCase):
    """An enum argument travels as its integer, so a constraint narrows its members."""

    def test_constraint_selects_the_allowed_member(self):
        arg = Arg.new_arg_from_stinger({"name": "e", "type": "enum", "enumName": "Numbers", "schema": {"enum": [3]}}, _root())
        for seed in SEEDS:
            with self.subTest(seed=seed):
                self.assertEqual(arg.get_random_example_value("python", seed=seed), "Numbers.THREE")

    def test_unsatisfiable_constraint_raises(self):
        arg = Arg.new_arg_from_stinger({"name": "e", "type": "enum", "enumName": "Numbers", "schema": {"minimum": 99}}, _root())
        with self.assertRaises(InvalidStingerStructure):
            arg.get_random_example_value("python", seed=2)


class TestConstrainedArrayExamples(unittest.TestCase):
    """``minItems``/``maxItems`` decide how many elements an example array carries."""

    def _array(self, schema=None):
        spec = {"name": "a", "type": "array", "itemType": {"type": "integer"}}
        if schema is not None:
            spec["schema"] = schema
        return Arg.new_arg_from_stinger(spec, _root())

    def test_min_items_is_respected(self):
        rendered = self._array({"minItems": 4}).get_random_example_value("python", seed=2)
        self.assertEqual(rendered.count(",") + 1, 4)

    def test_max_items_is_respected(self):
        rendered = self._array({"maxItems": 1}).get_random_example_value("python", seed=2)
        self.assertEqual(rendered.count(","), 0)

    def test_default_element_count_unchanged(self):
        self.assertEqual(self._array().get_random_example_value("python", seed=2).count(",") + 1, 2)

    def test_json_never_emits_an_empty_array_when_min_items_forbids_it(self):
        arg = self._array({"minItems": 2})
        for seed in SEEDS:
            with self.subTest(seed=seed):
                self.assertNotEqual(arg.get_random_example_value("json", seed=seed), "[]")

    def test_element_constraint_is_respected(self):
        arg = Arg.new_arg_from_stinger(
            {"name": "a", "type": "array", "itemType": {"type": "integer", "schema": {"minimum": 1, "maximum": 12}}},
            _root(),
        )
        rendered = arg.get_random_example_value("python", seed=2)
        for element in rendered.strip("[]").split(","):
            self.assertLessEqual(int(element.strip()), 12)


class TestUnsatisfiableConstraints(unittest.TestCase):
    """A constraint no example can satisfy is reported, not silently violated."""

    def test_pattern_raises(self):
        arg = Arg.new_arg_from_stinger({"name": "s", "type": "string", "schema": {"pattern": "^ZZZ-[0-9]{4}$"}})
        with self.assertRaises(InvalidStingerStructure) as ctx:
            arg.get_random_example_value("python", seed=2)
        self.assertIn("'s'", str(ctx.exception))

    def test_empty_numeric_range_raises(self):
        arg = Arg.new_arg_from_stinger({"name": "i", "type": "integer", "schema": {"minimum": 10, "maximum": 5}})
        with self.assertRaises(InvalidStingerStructure):
            arg.get_random_example_value("python", seed=2)

    def test_ambient_random_state_survives_a_raise(self):
        arg = Arg.new_arg_from_stinger({"name": "s", "type": "string", "schema": {"pattern": "^ZZZ$"}})
        random.seed(1234)
        expected = random.random()
        random.seed(1234)
        with self.assertRaises(InvalidStingerStructure):
            arg.get_random_example_value("python", seed=9)
        self.assertEqual(random.random(), expected)


class TestSchemaAllows(unittest.TestCase):

    def test_no_constraint_allows_anything(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer"})
        self.assertTrue(arg.schema_allows(999999))
        self.assertTrue(arg.schema_allows(None))

    def test_constraint_is_enforced(self):
        arg = Arg.new_arg_from_stinger({"name": "x", "type": "integer", "schema": {"maximum": 10}})
        self.assertTrue(arg.schema_allows(3))
        self.assertFalse(arg.schema_allows(11))
