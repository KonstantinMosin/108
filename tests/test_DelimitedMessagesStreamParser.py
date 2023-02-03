from utils.proto.message_pb2 import WrapperMessage
from src.DelimitedMessagesStreamParser import DelimitedMessagesStreamParser

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
        self.assertListEqual([], messages)
        """
        The function takes bytes
        """

        messages = parser.parse(None)
        self.assertListEqual([], messages)
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
        message = WrapperMessage()
        message.fast_response.current_date_time = '1'
        message = _VarintBytes(message.ByteSize()) + message.SerializeToString() # \x05\n\x03\n\x011
        
        stream = message * 3 # \x05\n\x03\n\x011\x05\n\x03\n\x011\x05\n\x03\n\x011
        """
        ----------------- ----------------- -----------------
        \x05\n\x03\n\x011 \x05\n\x03\n\x011 \x05\n\x03\n\x011
        """
        parser = DelimitedMessagesStreamParser(WrapperMessage)
        messages = parser.parse(stream)

        self.assertEqual(3, len(messages))
        for m in messages:
            self.assertTrue(m.HasField('fast_response'))

        stream_corrupted = stream[:len(message)]
        stream_corrupted += b'\x03'
        stream_corrupted += stream[len(message) + 1:]
        """
        ----------------- ----------------- -----------------
        \x05\n\x03\n\x011 \x05\n\x03\n\x011 \x05\n\x03\n\x011
                          ^
                          \x03
        ----------------- ------------ ----- -----------------                  
        \x05\n\x03\n\x011 \x03\n\x03\n \x011 \x05\n\x03\n\x011
        """

        messages = parser.parse(stream_corrupted)
        
        self.assertEqual(2, len(messages))
        for m in messages:
            self.assertTrue(m.HasField('fast_response'))
        
        stream_corrupted = b'\x02\x01\x05\x02\x01\x01\x01'
        stream_corrupted += stream

        # print(stream_corrupted)
        
        messages = parser.parse(stream_corrupted)
        """
        ------------ ------------ -------- ------------------------------ -----------------
        \x02\x01\x05 \x02\x01\x01 \x01\x05 \n\x03\n\x011\x05\n\x03\n\x011 \x05\n\x03\n\x011
        """
        
        self.assertEqual(1, len(messages))
        for m in messages:
            self.assertTrue(m.HasField('fast_response'))
