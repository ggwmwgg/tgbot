from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data import lang_en

ac_main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.users_eng),
            KeyboardButton(text=lang_en.cats_eng)
        ],
        [
            KeyboardButton(text=lang_en.orders_eng),
            KeyboardButton(text=lang_en.items_eng)
        ],
        [
            KeyboardButton(text=lang_en.back_eng)
        ]
    ],
    resize_keyboard=True

)

ac_users = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.info_by_id_eng),
            KeyboardButton(text=lang_en.info_by_number_eng)
        ],
        [
            KeyboardButton(text=lang_en.back_eng)
        ]
    ],
    resize_keyboard=True
)

ac_back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.back_eng)
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)