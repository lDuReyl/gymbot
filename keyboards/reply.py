from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


register_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Ввести данные"),
        ]
    ],resize_keyboard=True, one_time_keyboard=True
)

default_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Ввести БЖУ"),
            KeyboardButton(text="Проверить норму"),
        ],
        [
            KeyboardButton(text="Изменить данные"),
        ]
    ],resize_keyboard=True
)
