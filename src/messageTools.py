from typing import TypeVar, Any, Type
from google.protobuf.internal.decoder import _DecodeVarint32

T = TypeVar('T')

def parseDelimited(data: Any, message_type: Type[T]) -> Type[T]:
    if data is None or len(data) == 0:
        return None

    length, pos = _DecodeVarint32(data, 0)
    buffer = data[pos:pos + length]
    
    message = message_type()
    message.ParseFromString(buffer)
    
    return message, pos + length

class DelimitedMessagesStreamParser:
    def __init__(self, type: Type[T]) -> None:
        self.type = type
        self.buffer = b''

    def parse(self, data):
        self.buffer += data

        messages = []
        while (len(self.buffer)):
            message, bytesConsumed = parseDelimited(self.buffer, self.type)
            if message:
                messages.append(message)
            self.buffer = self.buffer[bytesConsumed:]
        
        return messages
