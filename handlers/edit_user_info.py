from aiogram import Bot, Router
from aiogram.types import Message
from keyboards.inline import edit_user_info_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from filters import _is_digit, _is_int
from stategroups.stategroups import EditUserInfo 
from db import set_user_field


router = Router()

state_to_russian = {EditUserInfo.age : "Возраст", EditUserInfo.weight : "Вес", EditUserInfo.height : "Рост"}

# Uzhas begin

@router.message(StateFilter(EditUserInfo))
async def edit_user_info(message: Message, state: FSMContext, bot: Bot):
    print("In edit_user_info handler")
    text = message.text.replace(',', '.', 1)
    current_state = await state.get_state()
    flag = 0
    if current_state == EditUserInfo.age and _is_int(text) and 5 < int(text) <= 100:
        flag = set_user_field(message.from_user.id, "age", text)
    elif current_state == EditUserInfo.weight and _is_digit(text) and 30 <= float(text) <= 250:
        flag = set_user_field(message.from_user.id, "weight", text)
    elif current_state == EditUserInfo.height and _is_digit(text) and 90 <= float(text) <= 250:
        flag = set_user_field(message.from_user.id, "height", text)
    if flag:
        await bot.send_message(message.from_user.id, f"{state_to_russian[current_state]} изменён")
        await state.set_state(EditUserInfo.choose)
        await bot.send_message(message.from_user.id, "Что вы хотите изменить?", reply_markup=edit_user_info_keyboard)
    else:
        
# Uzhas end

