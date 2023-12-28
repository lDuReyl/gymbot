from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from stategroups.stategroups import UserRegistration
from keyboards.reply import default_keyboard
from users_db import add_user

router = Router()

@router.callback_query(StateFilter(UserRegistration.height), F.data.in_(["male", "female"]))
async def get_sex(query: CallbackQuery, state: FSMContext, bot: Bot):
    query.answer()
    state_data = await state.get_data()
    age = state_data.get("age")
    weight = state_data.get("weight")
    height = state_data.get("height")
    add_user(query.from_user.id, age, query.data=="male", weight, height)
    await bot.send_message(query.from_user.id, f"Вы успешно ввели данные.\nВозраст: {age},\nвес: {weight},\nрост: {height},\nПол: {'мужской' if query.data == 'male' else 'женский'}.\nПри необходимости их можно изменить нажав, на кнопку снизу\n", reply_markup=default_keyboard)
    await state.clear()

