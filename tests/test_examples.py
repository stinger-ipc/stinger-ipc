import unittest
import os.path
import jsonschema_rs
from ruamel.yaml import YAML

from stingeripc.loading import parse_yaml_file

example_stinger_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../example_interfaces"))
schema_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../schemas/0.2/schema.yaml"))


class SchemaValidation:

    def test_validates(self):
        # Load the schema with plain YAML so $ref/$defs are left intact for
        # jsonschema_rs to resolve (parse_yaml_file would expand the recursive
        # jsonSchema definition and recurse forever).
        with open(schema_path) as f:
            schema_obj = YAML(typ="safe").load(f)
        validator = jsonschema_rs.validator_for(schema_obj)

        param_only_path = os.path.join(example_stinger_path, self.directory, self.stinger_name)
        interface = parse_yaml_file(param_only_path)

        errors = list(validator.iter_errors(interface))
        if errors:
            for error in errors:
                print(f"Error: {error}")
                print(f"Location: {error.instance_path}")
            assert (len(errors), 0)


class TestParamOnlyValidatesAgainstSchema(unittest.TestCase, SchemaValidation):

    def setUp(self):
        self.directory = "signal_only"
        self.stinger_name = "signal_only.stinger.yaml"


class TestEnumOnlyValidatesAgainstSchema(unittest.TestCase, SchemaValidation):

    def setUp(self):
        self.directory = "full"
        self.stinger_name = "full.stinger.yaml"
