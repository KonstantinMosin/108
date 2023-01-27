from proto import message_pb2
from google.protobuf.internal.decoder import _DecodeVarint32

def parseDelimited(data):
    if data is None or len(data) == 0:
        return None
    
    
    n = 0
    while n < len(data):
        length, pos = _DecodeVarint32(data, n)
        n = pos

        buffer = data[n:n + length]
        n += length

        message = message_pb2.WrapperMessage()
        message.ParseFromString(buffer)

    return message, length + pos

class DelimitedMessagesStreamParser:
    def __init__(self) -> None:
        self.buffer = []

    def parse(self, data):
        self.buffer.append(data)

        messages = []
        while (len(self.buffer)):
            message, bytesConsumed = parseDelimited(self.buffer, len(self.buffer))
            if message:
                messages.append(message)
            self.buffer = self.buffer[bytesConsumed:]
        
        return messages
