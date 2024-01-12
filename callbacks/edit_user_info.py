from typing import List
from collections.abc import Callable
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from stategroups.stategroups import EditUserInfo
from keyboards.inline import  edit_user_info_keyboard, sex_keyboard, goal_keyboard
from keyboards.reply import default_keyboard
from db import set_user_field

router = Router()

states = {"change_weight" : EditUserInfo.weight, "change_sex" : EditUserInfo.sex, "change_goal" : EditUserInfo.goal} 

state_translation = {EditUserInfo.weight: "вес", EditUserInfo.sex : "пол", EditUserInfo.goal : "цель"}

@router.callback_query(StateFilter(EditUserInfo.choose), F.data.in_(["change_weight", "change_goal",  "change_sex"]))
async def edit_user_info(query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(states[query.data])
    if query.data == "change_sex":
        await bot.send_message(query.from_user.id, "Выберите пол", reply_markup=sex_keyboard)
    elif query.data == "change_goal":
        await bot.send_message(query.from_user.id, "Выберите цель", reply_markup=goal_keyboard)
    else:
        current_state = await state.get_state()
        await bot.send_message(query.from_user.id, f"Введите {state_translation[current_state]}:")
    await query.answer()


@router.callback_query(StateFilter(EditUserInfo.choose), F.data == "cancel_edit_user_info")
async def cancel_edit_user_info(query: CallbackQuery, state: FSMContext, bot : Bot):
    await state.clear()
    await bot.send_message(query.from_user.id, "Вы закончили вводить данные", reply_markup=default_keyboard)
    await query.answer()


def create_edit_user_field_callback(field: str, changer: Callable[[str], str], translated_field: str, accaptable_data : List[str]):
    """Creates callback query handlers.
    Field is field in db
    changer is function that changes query data
    translated_field is translation for "field"
    accaptable_data is data which function will handle
    """
    state_filter = states["change_" + field]
    @router.callback_query(StateFilter(state_filter), F.data.in_(accaptable_data))
    async def edit_user_info(query: CallbackQuery, state: FSMContext, bot: Bot):
        value = changer(query.data)
        set_user_field(query.from_user.id, field, value)
        await bot.send_message(query.from_user.id, f"{translated_field} {'изменён' if translated_field == 'Пол' else 'изменена'}", reply_markup=edit_user_info_keyboard)
        await state.set_state(EditUserInfo.choose)
    return edit_user_info


edit_user_sex = create_edit_user_field_callback(
    "sex",
    lambda data: '1' if data == "male" else '0',
    state_translation[states["change_sex"]].title(),
    ["male", "female"]
)
edit_user_goal = create_edit_user_field_callback(
    "goal",
    lambda data: data[-1],
    state_translation[states["change_goal"]].title(),
    ["goal1", "goal2", "goal3", "goal4"]
)

