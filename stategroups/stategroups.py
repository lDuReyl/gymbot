from aiogram.fsm.state import State, StatesGroup

class UserRegistration(StatesGroup):
    weight = State()
    sex = State()
    goal = State()


class GetNutrients(StatesGroup):
    proteins = State()
    fats = State()
    carbohydrates = State()


class EditUserInfo(StatesGroup):
    choose = State()
    weight = State()
    sex = State()
    goal = State()

