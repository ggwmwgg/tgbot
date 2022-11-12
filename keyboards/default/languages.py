from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data import lang_en
from utils.db_api import quick_commands

languages = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="O'zbek"),
        ],
        [
            KeyboardButton(text="Русский")
        ],
        [
            KeyboardButton(text="English")
        ]

    ],
    resize_keyboard=True

)

nmbr = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.send_number_eng, request_contact=True)
        ]

    ],
    resize_keyboard=True

)

location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.send_location_eng, request_location=True)
        ],
        [
            KeyboardButton(text=lang_en.back_eng)
        ]

    ],
    resize_keyboard=True

)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.order_eng),
        ],
        [
            KeyboardButton(text=lang_en.leave_feedback_eng),
            KeyboardButton(text=lang_en.my_points_eng)
        ],
        [
            KeyboardButton(text=lang_en.contacts_eng),
            KeyboardButton(text=lang_en.settings_eng)

        ]

    ],
    resize_keyboard=True

)

d_or_d = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.delivery_eng),
            KeyboardButton(text=lang_en.pickup_eng)
        ],
        [
            KeyboardButton(text=lang_en.back_eng)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

#branches_list = []

#shops = await quick_commands.select_all_branches_list()
# for a in shops:
#     branches_list.append([a])

# print(branches_list)
#branches = ReplyKeyboardMarkup(branches_list, resize_keyboard=True)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.save_eng),
        ],
        [
            KeyboardButton(text=lang_en.choose_another_eng)
        ],
        [
            KeyboardButton(text=lang_en.back_eng)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

delivery_yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=lang_en.confirm_eng),
        ],
        [
            KeyboardButton(text=lang_en.send_again_eng)
        ],
        [
            KeyboardButton(text=lang_en.back_eng)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


quantity = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
        ],
        [
            KeyboardButton(text="4"),
            KeyboardButton(text="5"),
            KeyboardButton(text="6"),
        ],
        [
            KeyboardButton(text="7"),
            KeyboardButton(text="8"),
            KeyboardButton(text="9"),

        ],
        [
            KeyboardButton(text="Корзина"),
            KeyboardButton(text=lang_en.back_eng)

        ]

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

old_d_or_d = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Использовать старые данные"),
        ],
        [
            KeyboardButton(text="Указать новые данные")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

back_only = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
