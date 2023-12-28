from aiogram import Bot, Router
from aiogram.types import Message
from keyboards.reply import *
from keyboards.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from filters import is_digit, is_int
from stategroups.stategroups import UserRegistration

router = Router()


@router.message(StateFilter(UserRegistration.age), is_int(), lambda msg: 5 < int(msg.text) <= 100)
async def process_age(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(age=message.text)
    await state.set_state(UserRegistration.weight)
    await bot.send_message(message.from_user.id, "Введите ваш вес: ")


@router.message(StateFilter(UserRegistration.age), is_int())
async def process_age_failed(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Возраст должен быть от 6 до 100")


@router.message(StateFilter(UserRegistration.weight), is_digit(), lambda msg: 30 <= float(msg.text) <= 250)
async def process_weight(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(weight=float(message.text))
    await state.set_state(UserRegistration.height)
    await bot.send_message(message.from_user.id, "Введите ваш рост:")


@router.message(StateFilter(UserRegistration.weight), is_digit()) 
async def process_weight_failed(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Вес должен быть от 30 до 250")


@router.message(StateFilter(UserRegistration.height), is_digit(), lambda msg: 90 <= float(msg.text) <= 250)
async def process_height(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(height=float(message.text))
    await bot.send_message(message.from_user.id, "Выберите пол", reply_markup=sex_keyboard)


@router.message(StateFilter(UserRegistration.height), is_digit())
async def process_height_failed(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Рост должен быть от 90 до 250 (см)")

