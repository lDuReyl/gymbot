from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from stategroups.stategroups import UserRegistration
from keyboards.reply import default_keyboard
from keyboards.inline import activity_keyboard, goal_keyboard
from db import add_user, set_cpfh 

router = Router()

@router.callback_query(StateFilter(UserRegistration.sex), F.data.in_(["male", "female"]))
async def get_sex(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await state.update_data(sex=query.data)
    await bot.send_message(query.from_user.id, "Выберите свою активность:\n1️⃣ Нет нагрузок и сидячая работа\n2️⃣ Небольшие пробежки или лёгкая гимнастика 1-3 раза в неделю\n3️⃣ Занятия спортом со средними нагрузками 5-7 раз в неделю\n4️⃣ Полноценные тренировки 6-7 раз в неделю\n5️⃣ Ваша работа связана с физическим трудом, вы тренируетесь 2 раза в день, вклчая в программу тренировок силовые упражнения", reply_markup=activity_keyboard)
    await state.set_state(UserRegistration.activity) 


@router.callback_query(StateFilter(UserRegistration.activity),
                       F.data.in_(["low_activity", "mid_activity",
                                  "high_activity", "higher_activity",
                                  "highest_activity"]))
async def get_activity(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await state.update_data(activity=query.message.text)
    await bot.send_message(query.from_user.id, "Выберите вашу цель:", reply_markup=goal_keyboard)
    await state.set_state(UserRegistration.goal)


@router.callback_query(StateFilter(UserRegistration.goal), F.data.in_(["goal1", "goal2", "goal3"]))
async def get_goal(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    state_data = await state.get_data()
    age = state_data.get("age")
    weight = state_data.get("weight")
    height = state_data.get("height")
    activity = state_data.get("activity")
    goal = query.data[-1:] 
    add_user(query.from_user.id, age, query.data=="male", weight, height, activity, goal)
    set_cpfh(query.from_user.id)
    await bot.send_message(query.from_user.id, f"Вы успешно ввели данные.\nВозраст: {age},\nвес: {weight},\nрост: {height},\nпол: {'мужской' if query.data == 'male' else 'женский'}.\nПри необходимости их можно изменить нажав, на кнопку снизу\n", reply_markup=default_keyboard)
    await state.clear()

