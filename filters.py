from aiogram.filters import BaseFilter
from aiogram.types import Message

def _is_digit(string: str) -> bool:
    return string.lstrip('-').replace('.', '', 1).isdigit()


def _is_int(string: str) -> bool:
    return string.lstrip('-').isdigit()

class is_digit(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return _is_digit(message.text)


class is_int(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return _is_int(message.text)

