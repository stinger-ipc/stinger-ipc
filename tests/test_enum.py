from stingeripc.components import InterfaceEnum

import unittest

class TestEnumCreateManually(unittest.TestCase):
    def setUp(self):
        self.enum = InterfaceEnum("bread")
        self.enum.add_value("pumpernickel")
        self.enum.add_value("whole wheat")
        self.enum.add_value("french")

    def test_name(self):
        self.assertEqual(self.enum.name, "bread")
    
    def test_values(self):
        self.assertEqual(len(self.enum.values), 3)


class TestSignalCreateFromStinger(unittest.TestCase):
    def setUp(self):
        stinger = [
            {"name": "white"},
            {"name": "blue"},
            {"name": "red"},
        ]
        self.enum = InterfaceEnum.new_enum_from_stinger("color", stinger)

    def test_name(self):
        self.assertEqual(self.enum.name, "color")
    
    def test_values(self):
        self.assertEqual(len(self.enum.values), 3)

