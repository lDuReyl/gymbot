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
            InlineKeyboardButton(text="1️⃣", callback_data="activity1"),
            InlineKeyboardButton(text="2️⃣", callback_data="activity2"),
            InlineKeyboardButton(text="3️⃣", callback_data="activity3"),
            InlineKeyboardButton(text="4️⃣", callback_data="activity4"),
            InlineKeyboardButton(text="5️⃣", callback_data="activity5"),
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
        ]
    ],
)


edit_user_info_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Вес", callback_data="change_weight"),
            InlineKeyboardButton(text="Возраст", callback_data="change_age"),
            InlineKeyboardButton(text="Рост", callback_data="change_height"),
        ],
        [
            InlineKeyboardButton(text="Цель", callback_data="change_goal"),
            InlineKeyboardButton(text="Активность", callback_data="change_activity"),
        ],
        [
            InlineKeyboardButton(text="Закончить ввод", callback_data="cancel_edit_user_info")
        ]
    ],
)
