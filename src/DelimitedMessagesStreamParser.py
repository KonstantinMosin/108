from src.helpers import parseDelimited
from typing import TypeVar, Any, Type

T = TypeVar('T')

class DelimitedMessagesStreamParser:
    def __init__(self, type: Type[T]) -> None:
        self.type = type
        self.buffer: bytes = b''

    def parse(self, data: bytes) -> list[Type[T]]:
        try:
            self.buffer += data
        except TypeError:
            return []

        messages: list[Type[T]] = []
        while (len(self.buffer)):
            message, bytesConsumed = parseDelimited(self.buffer, self.type)
            if message:
                messages.append(message)
            self.buffer = self.buffer[bytesConsumed:]
            if bytesConsumed == 0:
                break
        
        return messages
