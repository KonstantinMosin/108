from utils.proto.message_pb2 import WrapperMessage
from src.helpers import parseDelimited

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

import unittest

class ParseDelimitedTest(unittest.TestCase):
    def test_null_data(self):
        message, bytesConsumed = parseDelimited(b'', WrapperMessage)
        self.assertIsNone(message)

        message, bytesConsumed = parseDelimited("", WrapperMessage)
        self.assertIsNone(message)

        message, bytesConsumed = parseDelimited(None, WrapperMessage)
        self.assertIsNone(message)

    def test_wrong_data(self):
        message, bytesConsumed = parseDelimited(b'Hello World', WrapperMessage)
        self.assertIsNone(message)
        
        message, bytesConsumed = parseDelimited(b'\x02\x04\x1A', WrapperMessage)
        self.assertIsNone(message)

    def test_bytes_consumed(self):
        message = WrapperMessage()
        message.request_for_fast_response.SetInParent()
        message = _VarintBytes(message.ByteSize()) + message.SerializeToString()

        length = len(message)

        message, bytesConsumed = parseDelimited(message, WrapperMessage)
        self.assertEqual(length, bytesConsumed)

        message, bytesConsumed = parseDelimited(b'', WrapperMessage)
        self.assertEqual(0, bytesConsumed)

        buffer = b'Hello world'
        message, bytesConsumed = parseDelimited(buffer, WrapperMessage)
        self.assertEqual(0, bytesConsumed)
        """
        Hexadecimal "H" is 0x48 (ASCII).
        The length of the 'ello world' message is 9 bytes,
        so the function is waiting for the rest of the message.
        """

        buffer = b'\x02\x04\x1A'
        message, bytesConsumed = parseDelimited(b'\x02\x04\x1A', WrapperMessage)
        self.assertEqual(len(buffer), bytesConsumed)
