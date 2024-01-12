from aiogram import Bot, Router
from aiogram.types import Message
from keyboards.inline import sex_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from filters import is_digit
from stategroups.stategroups import UserRegistration

router = Router()


@router.message(StateFilter(UserRegistration.weight), is_digit(), lambda msg: 30 <= float(msg.text) <= 250)
async def process_weight(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(weight=float(message.text))
    await state.set_state(UserRegistration.sex)
    await bot.send_message(message.from_user.id, "Выберите пол: ", reply_markup=sex_keyboard)


@router.message(StateFilter(UserRegistration.weight), is_digit()) 
async def process_weight_failed(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Вес должен быть от 30 до 250")
