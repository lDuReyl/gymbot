from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from keyboards.reply import register_keyboard
from stategroups.stategroups import UserRegistration
from db import get_field

router = Router()

@router.message(F.text.in_(["Ввести данные", "Изменить данные"]))
async def set_age(message: Message, state: FSMContext, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, f"Введите ваш возраст:") 
    await state.set_state(UserRegistration.age)


@router.message(F.text == "Проверить норму")
async def get_daily_PFH_norm(message: Message):
    await bot.send_message(message.from_user.id, get_field(message.from_user.id, "deily_calories"))

@router.message(StateFilter(default_state), Command("start"))
async def start_command(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, f"Бот спортзала X\nДля того, чтобы начать, нажмите на кнопку \"Ввести данные\". Вам потребуется ввести возраст, вес, рост и выбрать пол.", reply_markup=register_keyboard)


@router.message(Command("help"))
async def help(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "help text")
    await message.delete()

@router.message(Command("cancel"), ~StateFilter(default_state))
async def cancel_in_state(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    await bot.send_message(message.from_user.id, "Operation canceled")


@router.message(Command("cancel"))
async def cancel(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Nothing to cancel")


@router.message(~StateFilter(default_state))
async def wrong_data_sent(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Wrong data you can use /cancel to cancel operation or type data again:")

