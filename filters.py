from aiogram.filters import Filter
from aiogram.types import Message

def _is_digit(string: str) -> bool:
    if string == "-": return False
    if string[0] == '-': string = string[1:]
    return string.replace('.', '', 1).isdigit()


def _is_int(string: str) -> bool:
    if string == "-": return False
    if string[0] == '-': string = string[1:]
    return string.isdigit()

class is_digit(Filter):
    async def __call__(self, message: Message) -> bool:
        return _is_digit(message.text)


class is_int(Filter):
    async def __call__(self, message: Message) -> bool:
        return _is_int(message.text)

