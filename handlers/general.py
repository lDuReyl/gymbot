from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from keyboards.reply import register_keyboard
from keyboards.inline import edit_user_info_keyboard
from stategroups.stategroups import UserRegistration, EditUserInfo
from db import get_nutrients

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, f"Нажмите на кнопку \"Ввести данные\".\nНужно будет ввести возраст, вес, рост и выбрать пол.", reply_markup=register_keyboard)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


@router.message(F.text == "Ввести данные")
async def set_age(message: Message, state: FSMContext, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, f"Введите ваш вес:") 
    await state.set_state(UserRegistration.weight)


@router.message(F.text == "Изменить данные")
async def edit_user_info(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(EditUserInfo.choose)
    await bot.send_message(message.from_user.id, "Что вы хотите изменить?", reply_markup=edit_user_info_keyboard)


@router.message(F.text == "Проверить норму")
async def get_daily_PFH_norm(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, "Осталось:\nБелки: {0}\nЖиры: {1}\nУглеводы: {2}".format(*get_nutrients(message.from_user.id)))


@router.message(Command("help"))
async def help(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "help text")
    await message.delete()

