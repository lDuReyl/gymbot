from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from filters import is_digit
from stategroups.stategroups import GetNutrients
from db import get_nutrients, subtract_nutrients 
from keyboards.reply import default_keyboard

router = Router()

@router.message(StateFilter(default_state), F.text=="Ввести БЖУ")
async def get_PFH(message: Message, state: FSMContext, bot : Bot):
    await bot.send_message(message.from_user.id, "Введите полученные белки:")
    await state.set_state(GetNutrients.proteins)


@router.message(StateFilter(GetNutrients.proteins), is_digit())
async def process_proteins(message: Message, state: FSMContext, bot: Bot):
    if int(message.text) >= 0:
        await state.update_data(proteins=message.text)
        await bot.send_message(message.from_user.id, "Ввведите полученные жиры:")
        await state.set_state(GetNutrients.fats)
    else:
        await bot.send_message(message.from_user.id, "Белки должны быть больше 0")


@router.message(StateFilter(GetNutrients.fats), is_digit())
async def process_fats(message: Message, state: FSMContext, bot: Bot):
    if int(message.text) >= 0:
        await state.update_data(fats=message.text)
        await bot.send_message(message.from_user.id, "Ввведите полученные углеводы:")
        await state.set_state(GetNutrients.carbohydrates)
    else:
        await bot.send_message(message.from_user.id, "Жиры должны быть больше 0")


@router.message(StateFilter(GetNutrients.carbohydrates), is_digit())
async def process_carbohydrates(message: Message, state: FSMContext, bot: Bot):
    if int(message.text) >= 0:
        await state.update_data(carbohydrates=message.text)
        nutrients = await state.get_data()
        proteins = float(nutrients.get("proteins"))
        fats = float(nutrients.get("fats"))
        carbohydrates = float(nutrients.get("carbohydrates"))
        subtract_nutrients(message.from_user.id, proteins, fats, carbohydrates)
        await bot.send_message(message.from_user.id, "Осталось:\nБелки: {0} г\nЖиры: {1} г\nУглеводы: {2} г".format(*get_nutrients(message.from_user.id)), reply_markup=default_keyboard)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, "Углеводы должны быть больше 0")

