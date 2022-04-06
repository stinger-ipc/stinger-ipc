from stingeripc.topic import InterfaceTopicCreator

import unittest


class TestTopics(unittest.TestCase):
    def test_signal_topic(self):
        itc = InterfaceTopicCreator("test_interface")
        stc = itc.signal_topic_creator()
        self.assertEqual(stc.signal_topic("alert"), "test_interface/signal/alert")
