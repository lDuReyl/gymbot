from aiogram import Bot, Router
from aiogram.types import Message
from keyboards.inline import edit_user_info_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from filters import is_digit
from stategroups.stategroups import EditUserInfo 
from db import set_user_field


router = Router()


@router.message(StateFilter(EditUserInfo.weight), is_digit())
async def edit_user_weight(message: Message, state: FSMContext, bot: Bot):
    value = message.text
    if 30 <= int(value) <= 250:
        set_user_field(message.from_user.id, "weight", value)
        await bot.send_message(message.from_user.id, f"Вес изменён", reply_markup=edit_user_info_keyboard)
        await state.set_state(EditUserInfo.choose)
    else:
        await bot.send_message(message.from_user.id, f"Вес должен быть от 30 до 250")

