from aiogram.fsm.state import State, StatesGroup

class UserRegistration(StatesGroup):
    age = State()
    weight = State()
    height = State()
    sex = State()
    activity = State()
    goal = State()


class GetNutrients(StatesGroup):
    proteins = State()
    fats = State()
    carbohydrates = State()

