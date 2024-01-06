from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from stategroups.stategroups import EditUserInfo
from keyboards.inline import  edit_user_info_keyboard, sex_keyboard, activity_keyboard, goal_keyboard
from keyboards.reply import default_keyboard
from db import set_user_field

from handlers.edit_user_info import state_to_russian

router = Router()

states = {"change_age" :  EditUserInfo.age, "change_weight" : EditUserInfo.weight, "change_height" : EditUserInfo.height, "change_goal" : EditUserInfo.goal, "change_activity" : EditUserInfo.activity} 

@router.callback_query(StateFilter(EditUserInfo.choose), F.data.in_(["change_age", "change_weight", "change_height", "change_goal", "change_activity"]))
async def edit_user_info(query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(states[query.data])
    if query.data == "change_sex":
        await bot.send_message(query.from_user.id, "Выберите пол", reply_markup=sex_keyboard)
    elif query.data == "change_activity":
        await bot.send_message(query.from_user.id, "Выберите свою активность", reply_markup=activity_keyboard)
    elif query.data == "change_goal":
        await bot.send_message(query.from_user.id, "Выберите цель", reply_markup=goal_keyboard)
    else:
        current_state = await state.get_state()
        await bot.send_message(query.from_user.id, f"Введите {state_to_russian[current_state].lower()}:")
    await query.answer()
    print("edit_user_info end")


@router.callback_query(StateFilter(EditUserInfo.sex), F.data.in_(["male", "female"]))
async def process_sex(query: CallbackQuery, state: FSMContext, bot: Bot):
    set_user_field(query.from_user.id, "sex", 1 if query.data == "male" else 0)
    await bot.send_message(query.from_user.id, "Пол изменён", reply_markup=edit_user_info_keyboard)
    await state.set_state(EditUserInfo.choose)
    await query.answer()


@router.callback_query(StateFilter(EditUserInfo.activity), F.data[:8] == "activity")
async def process_activity(query: CallbackQuery, state: FSMContext, bot : Bot):
    print(f"{query.from_user.id}, activity, {query.data[8:]}")
    set_user_field(query.from_user.id, "activity1", query.data[8:])
    await bot.send_message(query.from_user.id, "Активность изменена", reply_markup=edit_user_info_keyboard)
    await state.set_state(EditUserInfo.choose)
    await query.answer()


@router.callback_query(StateFilter(EditUserInfo.goal), F.data[:4] == "goal")
async def process_goal(query: CallbackQuery, state: FSMContext, bot: Bot):
    set_user_field(query.from_user.id, "goal", query.data[-1])
    await bot.send_message(query.from_user.id, "Цель изменена", reply_markup=edit_user_info_keyboard)
    await state.set_state(EditUserInfo.choose)
    await query.answer()


@router.callback_query(StateFilter(EditUserInfo.choose), F.data == "cancel_edit_user_info")
async def cancel_edit_user_info(query: CallbackQuery, state: FSMContext, bot : Bot):
    await state.clear()
    await bot.send_message(query.from_user.id, "Вы закончили вводить данные", reply_markup=default_keyboard)
    await query.answer()
