from aiogram import Bot, Router
from aiogram.types import Message
from keyboards.inline import edit_user_info_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.filters import StateFilter
from filters import is_int, is_digit
from stategroups.stategroups import EditUserInfo 
from db import set_user_field


router = Router()


def create_edit_user_field_handler(field: str, min_value: int, max_value: int, rus_field: str, state_filter : State, filter):
    @router.message(StateFilter(state_filter), filter())
    async def edit_user_info(message: Message, state: FSMContext, bot: Bot):
        value = message.text
        if min_value < int(value) <= max_value:
            set_user_field(message.from_user.id, field, value)
            await bot.send_message(message.from_user.id, f"{rus_field} изменён", reply_markup=edit_user_info_keyboard)
            await state.set_state(EditUserInfo.choose)
        else:
            await bot.send_message(message.from_user.id, f"{rus_field} должен быть от {min_value} до {max_value}")

    return edit_user_info


edit_user_age = create_edit_user_field_handler(
    "age",
    5,
    100,
    "Возраст",
    EditUserInfo.age,
    is_int
)
edit_user_weight = create_edit_user_field_handler(
    "weight",
    30,
    250,
    "Вес",
    EditUserInfo.weight,
    is_digit
)
edit_user_height= create_edit_user_field_handler(
    "weight",
    90,
    250,
    "Рост",
    EditUserInfo.height,
    is_digit
)


