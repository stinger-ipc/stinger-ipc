
import unittest
import yaml
import os.path
from jacobsjsonschema.draft7 import Validator


example_stinger_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../example_interfaces"))
schema_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../schemas/schema.yaml"))


class TestParamOnlyValidatesAgainstSchema(unittest.TestCase):

    def test_validates(self):
        with open(schema_path) as fp:
            validator = Validator(yaml.load(fp, Loader=yaml.CSafeLoader), lazy_error_reporting=True)
        
        param_only_path = os.path.join(example_stinger_path, "signal_only.stingeripc")
        with open(param_only_path) as fp:
            interface = yaml.load(fp, Loader=yaml.CSafeLoader)
        is_valid = validator.validate(interface)
        if not is_valid:
            for err in validator.get_errors():
                print(err)
            self.assertEqual(len(validator.get_erros()), 0)
        self.assertTrue(is_valid)
