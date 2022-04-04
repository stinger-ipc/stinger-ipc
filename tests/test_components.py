
from stingeripc.components import Signal
from stingeripc.topics import SignalTopicCreator

import unittest

class TestSignalCreateManually(unittest.TestCase):

    def setUp(self):
        stc = SignalTopicCreator("test_interface")
        self.sig = Signal(stc, "mySignal")

    def test_create_signal(self):
        self.assertEqual(self.sig.name, "mySignal")

    def test_topic(self):
        self.assertEqual(self.sig.emit_topic, "test_interface/signal/mySignal")

class TestSignalCreateFromStinger(unittest.TestCase):

    def setUp(self):
        stc = SignalTopicCreator("test_interface")
        stinger = {
            "args": {
                "one": {"type": "integer"},
                "two": {"type": "string", "description": "This is the second arg"},
            },
        }
        self.sig = Signal.new_from_stinger(stc, "mySignal", stinger)

    def test_create_signal(self):
        self.assertEqual(self.sig.name, "mySignal")

    def test_signal_args(self):
        self.assertEqual(len(self.sig.arg_list), 2)

    def test_topic(self):
        self.assertEqual(self.sig.emit_topic, "test_interface/signal/mySignal")