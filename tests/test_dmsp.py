from src.messageTools import DelimitedMessagesStreamParser
from proto.message_pb2 import WrapperMessage

from google.protobuf.internal.encoder import _VarintBytes

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
        message = WrapperMessage()
        message.fast_response.current_date_time = "1"
        message = _VarintBytes(message.ByteSize()) + message.SerializeToString() # \x05\n\x03\n\x011
        
        pass
        