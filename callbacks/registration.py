from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from stategroups.stategroups import UserRegistration
from keyboards.reply import default_keyboard
from keyboards.inline import goal_keyboard
from db import add_user, set_nutrients_by_user_id

router = Router()

@router.callback_query(StateFilter(UserRegistration.sex), F.data.in_(["male", "female"]))
async def get_sex(query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(query.from_user.id, "Выберите цель", reply_markup=goal_keyboard)
    await state.set_state(UserRegistration.goal)


@router.callback_query(StateFilter(UserRegistration.goal), F.data[:4] == "goal")
async def get_goal(query: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    sex = "1" if query.data=="male" else "0"
    weight = state_data.get("weight")
    goal = query.data[4]
    add_user(query.from_user.id, sex, weight, goal)
    set_nutrients_by_user_id(query.from_user.id)
    await bot.send_message(query.from_user.id, f"Вы успешно ввели данные.\nВес: {weight},\nпол: {'мужской' if sex == '1' else 'женский'}.\nПри необходимости их можно изменить нажав, на кнопку снизу\n", reply_markup=default_keyboard)
    await state.clear()
    await query.answer()

