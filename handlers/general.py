from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command, invert_f 
from aiogram.fsm.state import default_state 
from keyboards.reply import register_keyboard
from keyboards.inline import edit_user_info_keyboard
from stategroups.stategroups import UserRegistration, EditUserInfo
from db import get_nutrients

router = Router()


@router.message(StateFilter(default_state), Command("start"))
async def start_command(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, f"Нажмите на кнопку \"Ввести данные\".\nНужно будет ввести вес, выбрать пол.", reply_markup=register_keyboard)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


@router.message(StateFilter(default_state), F.text == "Ввести данные")
async def set_age(message: Message, state: FSMContext, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, f"Введите ваш вес:") 
    await state.set_state(UserRegistration.weight)


@router.message(StateFilter(default_state), F.text == "Изменить данные")
async def edit_user_info(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(EditUserInfo.choose)
    await bot.send_message(message.from_user.id, "Что вы хотите изменить?", reply_markup=edit_user_info_keyboard)


@router.message(StateFilter(default_state), F.text == "Проверить норму")
async def get_daily_PFH_norm(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, "Осталось:\nБелки: {0}\nЖиры: {1}\nУглеводы: {2}".format(*get_nutrients(message.from_user.id)))


@router.message(~StateFilter(default_state), invert_f(F.text[0]=='/'))
async def wrong_data(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, "Данные введены неправильно")

