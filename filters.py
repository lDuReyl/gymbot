from aiogram.filters import BaseFilter
from aiogram.types import Message

class is_digit(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.lstrip('-').replace('.', '', 1).isdigit()


class is_int(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.lstrip('-').isdigit()

