from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from filters import is_digit
from stategroups.stategroups import GetNutrients
from db import get_nutrients, subtract_nutrients 

router = Router()

@router.message(StateFilter(default_state), F.text=="Ввести БЖУ")
async def get_PFH(message: Message, state: FSMContext, bot : Bot):
    await bot.send_message(message.from_user.id, "Введите белки:")
    await state.set_state(GetNutrients.proteins)


@router.message(StateFilter(GetNutrients.proteins), is_digit())
async def process_proteins(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(proteins=message.text)
    await bot.send_message(message.from_user.id, "Ввведите жиры:")
    await state.set_state(GetNutrients.fats)


@router.message(StateFilter(GetNutrients.fats), is_digit())
async def process_fats(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(fats=message.text)
    await bot.send_message(message.from_user.id, "Ввведите углеводы:")
    await state.set_state(GetNutrients.carbohydrates)


@router.message(StateFilter(GetNutrients.carbohydrates), is_digit())
async def process_carbohydrates(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(carbohydrates=message.text)
    nutrients = await state.get_data()
    proteins = float(nutrients.get("proteins"))
    fats = float(nutrients.get("fats"))
    carbohydrates = float(nutrients.get("carbohydrates"))
    subtract_nutrients(message.from_user.id, proteins, fats, carbohydrates)
    await bot.send_message(message.from_user.id, "Осталось:\nБелки: {0}\nЖиры: {1}\nУглеводы: {2}".format(*get_nutrients(message.from_user.id)))
    await state.clear()
