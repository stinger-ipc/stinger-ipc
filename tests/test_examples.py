
import unittest
import yaml
import os.path
from jacobsjsonschema.draft7 import Validator


example_stinger_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../example_interfaces"))
schema_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../schemas/schema.yaml"))


class SchemaValidation:

    def test_validates(self):
        with open(schema_path) as fp:
            validator = Validator(yaml.load(fp, Loader=yaml.CSafeLoader), lazy_error_reporting=True)
        
        param_only_path = os.path.join(example_stinger_path, self.directory, self.stinger_name)
        with open(param_only_path) as fp:
            interface = yaml.load(fp, Loader=yaml.CSafeLoader)
        is_valid = validator.validate(interface)
        if not is_valid:
            for err in validator.get_errors():
                print(err)
            self.assertEqual(len(validator.get_errors()), 0)
        self.assertTrue(is_valid)


class TestParamOnlyValidatesAgainstSchema(unittest.TestCase, SchemaValidation):

    def setUp(self):
        self.directory = "signal_only"
        self.stinger_name = "signal_only.stingeripc"


class TestEnumOnlyValidatesAgainstSchema(unittest.TestCase, SchemaValidation):

    def setUp(self):
        self.directory = "enum_only"
        self.stinger_name = "enum_only.stingeripc"

