import asyncio
from aiogram import Bot, Dispatcher, F, types
from keyboards.default import default_keyboard
from aiogram.types import ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv
from dotenv import load_dotenv
from stategroups import UserRegistration

from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from users_db import add_user

load_dotenv()
API_TOKEN = getenv("API_TOKEN")
dp = Dispatcher()
storage = MemoryStorage()
all_commands_text = """
/help - help menu
"""

async def startup():
    print("Бот запущен")


@dp.message(StateFilter(UserRegistration.age), lambda msg: msg.text.isdigit() and 5 < int(msg.text) <= 100)
async def process_age(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(age=message.text)
    await state.set_state(UserRegistration.weight)
    await bot.send_message(message.from_user.id, "Введите свой вес: ")


@dp.message(StateFilter(UserRegistration.age), lambda msg: msg.text.isdigit())
async def process_age_failed(message: types.Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Возраст должен быть от 6 до 100")


@dp.message(StateFilter(UserRegistration.weight), lambda msg: msg.text.isdigit() and 30 <= int(msg.text) <= 250)
async def process_weight(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(weight=message.text)
    await state.set_state(UserRegistration.height)
    await bot.send_message(message.from_user.id, "Введите свой рост:")


@dp.message(StateFilter(UserRegistration.weight), lambda msg: msg.text.isdigit())
async def process_weight_failed(message: types.Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Вес должен быть от 30 до 250")
    

@dp.message(StateFilter(UserRegistration.height), lambda msg: msg.text.isdigit() and 90 < int(msg.text) <= 250)
async def process_height(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(height=message.text)
    state_data = await state.get_data()
    age = state_data.get("age")
    weight = state_data.get("weight")
    height = state_data.get("height")
    add_user(message.from_user.id, age, weight, height)
    await bot.send_message(message.from_user.id, f"Вы успешно ввели данные.\n Возраст: {age}, вес: {weight}, рост: {height}\n При необходимости их можно изменить нажав, на кнопку снизу\n", reply_markup=default_keyboard)
    await state.clear()


@dp.message(StateFilter(UserRegistration.weight), lambda msg: msg.text.isdigit())
async def process_weight_failed(message: types.Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Рост должен быть от 90 до 250 (см)")


@dp.message(StateFilter(default_state), Command("start"))
async def start_command(message: types.Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Бот спортзала X\nДля того, чтобы начать, нажмите на кнопку и введите свой возраст", reply_markup=default_keyboard) 
        

@dp.message(Command("help"))
async def help(message: types.Message, bot: Bot) -> None:
    await bot.send_message(bot.send_message(message.from_user.id, "help text"))
    await message.delete()


@dp.message(StateFilter(default_state), lambda _: Command("set_age") or F.text=="Change age")
async def set_age(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, f"{message.from_user.first_name}, введите ваш возраст:", reply_markup=ReplyKeyboardRemove()) 
    await state.set_state(UserRegistration.age)


@dp.message(Command("cancel"), ~StateFilter(default_state), bot: Bot)
async def cancel_in_state(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await bot.send_message(message.from_user.id, "Operation canceled")


@dp.message(Command("cancel"))
async def cancel(message: types.Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Nothing to cancel")


@dp.message(~StateFilter(default_state))
async def wrong_data_sent(message: types.Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, "Wrong data you can use /cancel to cancel operation or type data again:")


async def main() -> None:
    bot = Bot(str(API_TOKEN))
    dp.startup.register(startup)
    await dp.start_polling(bot, storage=storage, parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    asyncio.run(main())

