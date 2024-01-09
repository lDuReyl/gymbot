from typing import List
from collections.abc import Callable
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from stategroups.stategroups import EditUserInfo
from keyboards.inline import  edit_user_info_keyboard, sex_keyboard, activity_keyboard, goal_keyboard
from keyboards.reply import default_keyboard
from db import set_user_field
from big_messages import choose_activity_text

router = Router()

states = {"change_age" :  EditUserInfo.age, "change_weight" : EditUserInfo.weight, "change_height" : EditUserInfo.height, "change_sex" : EditUserInfo.sex, "change_goal" : EditUserInfo.goal, "change_activity" : EditUserInfo.activity} 

state_to_russian = {EditUserInfo.age: "возраст", EditUserInfo.weight: "вес", EditUserInfo.height : "рост", EditUserInfo.sex : "пол"}

@router.callback_query(StateFilter(EditUserInfo.choose), F.data.in_(["change_age", "change_weight", "change_height", "change_goal", "change_activity", "change_sex"]))
async def edit_user_info(query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(states[query.data])
    if query.data == "change_sex":
        await bot.send_message(query.from_user.id, "Выберите пол", reply_markup=sex_keyboard)
    elif query.data == "change_activity":
        await bot.send_message(query.from_user.id, choose_activity_text, reply_markup=activity_keyboard)
    elif query.data == "change_goal":
        await bot.send_message(query.from_user.id, "Выберите цель", reply_markup=goal_keyboard)
    else:
        current_state = await state.get_state()
        await bot.send_message(query.from_user.id, f"Введите {state_to_russian[current_state]}:")
    await query.answer()


@router.callback_query(StateFilter(EditUserInfo.choose), F.data == "cancel_edit_user_info")
async def cancel_edit_user_info(query: CallbackQuery, state: FSMContext, bot : Bot):
    await state.clear()
    await bot.send_message(query.from_user.id, "Вы закончили вводить данные", reply_markup=default_keyboard)
    await query.answer()


def create_edit_user_field_callback(field: str, changer: Callable[[str], str], rus_field: str, accaptable_data : List[str]):
    state_filter = states["change_" + field]
    @router.callback_query(StateFilter(state_filter), F.data.in_(accaptable_data))
    async def edit_user_info(query: CallbackQuery, state: FSMContext, bot: Bot):
        value = changer(query.data)
        set_user_field(query.from_user.id, field, value)
        await bot.send_message(query.from_user.id, f"{rus_field} {'изменён' if rus_field == 'Пол' else 'изменена'}", reply_markup=edit_user_info_keyboard)
        await state.set_state(EditUserInfo.choose)
    return edit_user_info


edit_user_sex = create_edit_user_field_callback(
    "sex",
    lambda data: '1' if data == "male" else '0',
    "Пол",
    ["male", "female"]
)
edit_user_activity = create_edit_user_field_callback(
    "activity",
    lambda data: data[8:],
    "Активность",
    ["activity1.2", "activity1.375", "activity1.55", "activity1.725", "activity1.9"]
)
edit_user_goal = create_edit_user_field_callback(
    "goal",
    lambda data: data[-1],
    "Цель",
    ["goal1", "goal2", "goal3", "goal4"]
)

