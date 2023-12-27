import asyncio
from aiogram import Bot, Dispatcher, F, types
from keyboards.default import default_keyboard
from aiogram.types import ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv
from dotenv import load_dotenv

from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from users_db import add_user#, get_age 

load_dotenv()
API_TOKEN = getenv("API_TOKEN")
dp = Dispatcher()
storage = MemoryStorage()
all_commands_text = """
/help - help menu
"""

async def startup():
    print("Бот запущен")

class UserRegistration(StatesGroup):
    age = State()
    weight = State()
    height = State(q)

@dp.message(StateFilter(UserRegistration.age), lambda msg: msg.text.isdigit() and 5 < int(msg.text) < 101)
async def process_age(message: types.Message, state: FSMContext) -> None:
    state_data = await state.update_data(age=message.text)
    print("proces_age-do")
    add_user(message.from_user.id, int(state_data['age']))
    await state.clear()
    await message.answer("Возраст успешно установлен", reply_markup=default_keyboard)



@dp.message(StateFilter(UserRegistration.age), lambda msg: msg.text.isdigit() and not (5 < int(msg.text) < 101))
async def process_age_failed(message: types.Message) -> None:
    await message.answer("Возраст должен быть от 6 до 100")


@dp.message(StateFilter(default_state), Command("start"))
async def start_command(message: types.Message) -> None:
    await message.answer(f"Бот спортзала X\nДля того, чтобы начать, нажмите на кнопку и введите свой возраст", reply_markup=default_keyboard) 
        

@dp.message(Command("help"))
async def help(message: types.Message) -> None:
    await message.answer("help text")
    await message.delete()


@dp.message(StateFilter(default_state), lambda _: Command("set_age") or F.text=="Change age")
async def set_age(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"{message.from_user.first_name}, введите ваш возраст:", reply_markup=ReplyKeyboardRemove()) 
    await state.set_state(UserRegistration.age)


@dp.message(Command("cancel"), ~StateFilter(default_state))
async def cancel_in_state(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Operation canceled")


@dp.message(Command("cancel"))
async def cancel(message: types.Message) -> None:
    await message.answer("Nothing to cancel")


@dp.message(~StateFilter(default_state))
async def wrong_data_sent(message: types.Message) -> None:
    await message.answer("Wrong data you can use /cancel to cancel operation or type data again:")


async def main() -> None:
    bot = Bot(str(API_TOKEN))
    dp.startup.register(startup)
    await dp.start_polling(bot, storage=storage, parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    asyncio.run(main())

