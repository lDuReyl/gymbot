from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sex_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Мужской", callback_data="male"),
            InlineKeyboardButton(text="Женский", callback_data="female"),
        ]
    ],
)

activity_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1️⃣", callback_data="low_activity"),
            InlineKeyboardButton(text="2️⃣", callback_data="mid_activity"),
            InlineKeyboardButton(text="3️⃣", callback_data="high_activity"),
            InlineKeyboardButton(text="4️⃣", callback_data="higher_activity"),
            InlineKeyboardButton(text="5️⃣", callback_data="highest_activity"),
        ]
    ],
)

goal_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Поддерживать массу", callback_data="goal1"),
        ],
        [
            InlineKeyboardButton(text="Худеть", callback_data="goal2"),
        ],
        [
            InlineKeyboardButton(text="Набирать массу", callback_data="goal3"),
        ],
    ],
)
