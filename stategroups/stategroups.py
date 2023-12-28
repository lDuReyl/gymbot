from aiogram.fsm.state import State, StatesGroup

class UserRegistration(StatesGroup):
    age = State()
    weight = State()
    height = State()


class GetNutrients(StatesGroup):
    proteins = State()
    fats = State()
    carbohydrates = State()

