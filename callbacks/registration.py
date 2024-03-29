from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from stategroups.stategroups import UserRegistration
from keyboards.reply import default_keyboard
from keyboards.inline import activity_keyboard, goal_keyboard
from db import add_user, set_cpfh 
from big_messages import choose_activity_text

router = Router()

@router.callback_query(StateFilter(UserRegistration.sex), F.data.in_(["male", "female"]))
async def get_sex(query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(sex=("1" if query.data=="male" else "0"))
    await bot.send_message(query.from_user.id, choose_activity_text, reply_markup=activity_keyboard)
    await state.set_state(UserRegistration.activity) 
    await query.answer()


@router.callback_query(StateFilter(UserRegistration.activity), F.data[:8] == "activity")
async def get_activity(query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(activity=query.data[8:])
    await bot.send_message(query.from_user.id, "Выберите вашу цель:", reply_markup=goal_keyboard)
    await state.set_state(UserRegistration.goal)
    await query.answer()


@router.callback_query(StateFilter(UserRegistration.goal), F.data[:4] == "goal")
async def get_goal(query: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    age = state_data.get("age")
    weight = state_data.get("weight")
    height = state_data.get("height")
    activity = state_data.get("activity")
    sex = state_data.get("sex")
    goal = query.data[-1:] 
    add_user(query.from_user.id, age, sex, weight, height, activity, goal)
    set_cpfh(query.from_user.id)
    await bot.send_message(query.from_user.id, f"Вы успешно ввели данные.\nВозраст: {age},\nвес: {weight},\nрост: {height},\nпол: {'мужской' if sex == '1' else 'женский'}.\nПри необходимости их можно изменить нажав, на кнопку снизу\n", reply_markup=default_keyboard)
    await state.clear()
    await query.answer()

