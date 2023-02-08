from typing import TypeVar, Any, Type
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.message import DecodeError

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
    except AttributeError or DecodeError:
        return None, pos + length
    
    return message, pos + length