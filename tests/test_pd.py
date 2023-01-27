from src.messageTools import parseDelimited
from proto import message_pb2

import unittest

class ParseDelimitedTest(unittest.TestCase):
    def test_null_data(self):
        self.assertIsNone(parseDelimited(None, message_pb2.WrapperMessage()))
        self.assertIsNone(parseDelimited("", message_pb2.WrapperMessage()))
