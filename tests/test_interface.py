from stingeripc.components import StingerSpec, Signal
from stingeripc.topic import InterfaceTopicCreator

import unittest

class TestSpecCreateManually(unittest.TestCase):
    def setUp(self):
        self.interface = {
            "name": "test_interface",
            "version": "1.2.3",
        }
        itc = InterfaceTopicCreator(self.interface['name'])
        self.spec = StingerSpec(itc, self.interface)
        signal = Signal(itc.signal_topic_creator(), "mySignal")
        self.spec.add_signal(signal)

    def test_create_spec(self):
        self.assertEqual(self.spec.name, self.interface['name'])

    def test_has_signals(self):
        self.assertEqual(len(self.spec.signals), 1)
        self.assertIn("mySignal", self.spec.signals)

class TestSpecCreateFromStructure(unittest.TestCase):
    def setUp(self):
        self.stinger = {
            "stingeripc": {
                "version": "0.0.7"
            },
            "interface": {
                "name": "test_interface",
                "version": "0.0.1",
            },
            "signals": {
                "mySignal": {
                    "payload": [
                        {"name": "one", "type": "integer"},
                        {"name": "two", "type": "string"},
                    ]
                }
            },
            "enums": {
                "milk": [
                    {"name": "one percent"},
                    {"name": "two percent"},
                ]
            }
        }
        itc = InterfaceTopicCreator(self.stinger['interface']['name'])
        self.spec = StingerSpec.new_spec_from_stinger(itc, self.stinger)

    def test_create_spec(self):
        self.assertIsNotNone(self.spec)
        self.assertEqual(self.spec.name, self.stinger['interface']['name'])

    def test_has_signals(self):
        self.assertEqual(len(self.spec.signals), 1)
        self.assertIn("mySignal", self.spec.signals)

    def test_has_enums(self):
        self.assertEqual(len(self.spec.enums), 1)
        self.assertIn("milk", self.spec.enums)