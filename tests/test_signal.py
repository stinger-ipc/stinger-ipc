from stingeripc.components import Signal, InvalidStingerStructure
from stingeripc.topic import SignalTopicCreator

import unittest


class TestSignalCreateManually(unittest.TestCase):
    def setUp(self):
        stc = SignalTopicCreator("test_interface")
        self.sig = Signal(stc, "mySignal")

    def test_create_signal(self):
        self.assertEqual(self.sig.name, "mySignal")

    def test_topic(self):
        self.assertEqual(self.sig.topic, "test_interface/signal/mySignal")


class TestSignalCreateFromStinger(unittest.TestCase):
    def setUp(self):
        stc = SignalTopicCreator("test_interface")
        stinger = {
            "payload": [
                {"name": "one", "type": "integer"},
                {"name": "two", "type": "string", "description": "This is the second arg"},
            ]
        }
        self.sig = Signal.new_signal_from_stinger(stc, "mySignal", stinger)

    def test_create_signal(self):
        self.assertEqual(self.sig.name, "mySignal")

    def test_signal_args(self):
        self.assertEqual(len(self.sig.arg_list), 2)

    def test_topic(self):
        self.assertEqual(self.sig.topic, "test_interface/signal/mySignal")


class TestSignalRejectsArgsWithSameName(unittest.TestCase):

    def setUp(self):
        self.topic_creator = SignalTopicCreator("test_interface")

    def test_two_args_with_same_name(self):
        signal_spec = {
            "payload": [
                {"name": "one", "type": "integer"},
                {"name": "one", "type": "string", "description": "This is the second arg"},
            ]
        }

        with self.assertRaises(InvalidStingerStructure):
            Signal.new_signal_from_stinger(self.topic_creator, "badSignal", signal_spec)