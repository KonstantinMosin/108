from src.messageTools import parseDelimited
from proto.message_pb2 import WrapperMessage

import unittest

class ParseDelimitedTest(unittest.TestCase):
    def test_null_data(self):
        self.assertIsNone(parseDelimited(None, WrapperMessage))
        self.assertIsNone(parseDelimited("", WrapperMessage))
