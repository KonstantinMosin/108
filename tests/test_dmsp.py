from src.messageTools import DelimitedMessagesStreamParser
from proto.message_pb2 import WrapperMessage

import unittest

class DelimitedMessagesStreamParserTest(unittest.TestCase):
    def test_null_data(self):
        parser = DelimitedMessagesStreamParser(WrapperMessage)
        
        messages = parser.parse(b'')
        self.assertListEqual([], messages)
        """
        An empty list is created before parsing
        """

        messages = parser.parse("")
        self.assertIsNone(messages)
        """
        The function takes bytes
        """

        messages = parser.parse(None)
        self.assertIsNone(messages)
        """
        The function takes bytes
        """

    def test_wrong_data(self):
        parser = DelimitedMessagesStreamParser(WrapperMessage)
        
        messages = parser.parse(b'\x04TEST')
        self.assertListEqual([], messages)

        messages = parser.parse(b'\x0A\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01')
        self.assertListEqual([], messages)
    
    def test_corrupted_data(self):
        # TODO
        pass
        