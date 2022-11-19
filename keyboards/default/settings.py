from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data import lang_en

d_or_d = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.delivery_eng),
        ],
        [
            KeyboardButton(text=lang_en.pickup_eng),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

nmbr_s = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.send_number_eng, request_contact=True)
        ],
        [
            KeyboardButton(text=lang_en.back_eng),
        ]

    ],
    resize_keyboard=True

)