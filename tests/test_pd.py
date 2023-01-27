from proto import message_pb2
from src.messageTools import parseDelimited

import unittest

class ParseDelimitedTest(unittest.TestCase):
    def setUp(self):
        self.message = message_pb2.WrapperMessage()

    def test_nulldata(self):
        self.assertIsNone(parseDelimited(None))
        self.assertIsNone(parseDelimited(""))
