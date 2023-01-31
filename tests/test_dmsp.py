from src.messageTools import DelimitedMessagesStreamParser
from proto.message_pb2 import WrapperMessage

import unittest

class DelimitedMessagesStreamParserTest(unittest.TestCase):
    def test_null_data(self):
        parser = DelimitedMessagesStreamParser(WrapperMessage)
        parser.parse(b'')