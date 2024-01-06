from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from keyboards.reply import register_keyboard
from keyboards.inline import edit_user_info_keyboard
from stategroups.stategroups import UserRegistration, EditUserInfo
from db import get_nutrients

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, f"Бот спортзала X\nДля того, чтобы начать, нажмите на кнопку \"Ввести данные\". Вам потребуется ввести возраст, вес, рост и выбрать пол.", reply_markup=register_keyboard)


@router.message(F.text == "Ввести данные")
async def set_age(message: Message, state: FSMContext, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, f"Введите ваш возраст:") 
    await state.set_state(UserRegistration.age)


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

@router.message(Command("cancel"), ~StateFilter(default_state))
async def cancel_in_state(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    await bot.send_message(message.from_user.id, "Операция отменена")


@router.message(Command("cancel"))
async def cancel(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Нечего отменять")


@router.message(~StateFilter(default_state))
async def wrong_data_sent(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Данные введены неправильно.\n Вы можете использовать команду /cancel или ввести данные ещё раз:")

