from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


register_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Ввести данные"),
        ]
    ],resize_keyboard=True, one_time_keyboard=True
)

default_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Изменить данные"),
        ],
        [
            KeyboardButton(text="Здоровое питание"),
        ]
    ],resize_keyboard=True, one_time_keyboard=True, 
)

healthy_eating_keyboard= ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Изменить данные"),
            KeyboardButton(text="Ввести БЖУ"),
            KeyboardButton(text="Проверить норму"),
        ]
    ],resize_keyboard=True
)
