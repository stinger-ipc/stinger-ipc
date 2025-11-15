
import unittest
import yaml
import yamlloader
import os.path
import jsonschema_rs


example_stinger_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../example_interfaces"))
schema_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../schemas/schema.yaml"))


class SchemaValidation:

    def test_validates(self):
        with open(schema_path) as fp:
            schema_obj = yaml.load(fp, Loader=yamlloader.ordereddict.Loader)
        validator = jsonschema_rs.validator_for(schema_obj)
        
        param_only_path = os.path.join(example_stinger_path, self.directory, self.stinger_name)
        with open(param_only_path) as fp:
            interface = yaml.load(fp, Loader=yamlloader.ordereddict.Loader)
        
        errors = list(validator.iter_errors(interface))
        if errors:
            for error in errors:
                print(f"Error: {error}")
                print(f"Location: {error.instance_path}")
            assert (len(errors), 0)

class TestParamOnlyValidatesAgainstSchema(unittest.TestCase, SchemaValidation):

    def setUp(self):
        self.directory = "signal_only"
        self.stinger_name = "signal_only.stingeripc"


class TestEnumOnlyValidatesAgainstSchema(unittest.TestCase, SchemaValidation):

    def setUp(self):
        self.directory = "enum_only"
        self.stinger_name = "enum_only.stingeripc"

