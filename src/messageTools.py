from typing import TypeVar, Any, Type
from google.protobuf.internal.decoder import _DecodeVarint32

T = TypeVar('T')

def parseDelimited(data: Any, message_type: Type[T]) -> Type[T]:
    if data is None or len(data) == 0:
        return None, 0
    
    length, pos = _DecodeVarint32(data, 0)

    if (length > len(data[pos:])):
        return None, 0

    buffer = data[pos:pos + length]
    
    message = message_type()
    try:
        message.ParseFromString(buffer)
    except:
        return None, pos + length
    
    return message, pos + length

class DelimitedMessagesStreamParser:
    def __init__(self, type: Type[T]) -> None:
        self.type = type
        self.buffer: bytes = b''

    def parse(self, data: Any) -> list[Type[T]]:
        try:
            self.buffer += data
        except:
            return None

        messages: list[Type[T]] = []
        while (len(self.buffer)):
            message, bytesConsumed = parseDelimited(self.buffer, self.type)
            if message:
                messages.append(message)
            self.buffer = self.buffer[bytesConsumed:]
        
        return messages
