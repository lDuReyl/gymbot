from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sex_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Мужской", callback_data="male"),
            InlineKeyboardButton(text="Женский", callback_data="female"),
        ]
    ],
)

goal_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Худеть", callback_data="goal2"),
        ],
        [
            InlineKeyboardButton(text="Набирать массу", callback_data="goal3"),
        ]
    ],
)


edit_user_info_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Вес", callback_data="change_weight"),
        ],
        [
            InlineKeyboardButton(text="Цель", callback_data="change_goal"),
            InlineKeyboardButton(text="Пол", callback_data="change_sex"),
        ],
        [
            InlineKeyboardButton(text="Закончить ввод", callback_data="cancel_edit_user_info")
        ]
    ],
)
