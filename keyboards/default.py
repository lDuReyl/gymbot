from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


default_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Change age"),
        ]
    ],resize_keyboard=True
)
