from stingeripc.components import InterfaceEnum

import unittest

class TestEnumCreateManually(unittest.TestCase):
    def setUp(self):
        self.enum = InterfaceEnum("bread")
        self.enum.add_item("pumpernickel")
        self.enum.add_item("whole wheat")
        self.enum.add_item("french")

    def test_name(self):
        self.assertEqual(self.enum.name, "bread")
    
    def test_values(self):
        self.assertEqual(len(self.enum.items), 3)


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

