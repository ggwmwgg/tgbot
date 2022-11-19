from aiogram import types
from data import lang_en


settings = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
settings.row(types.InlineKeyboardButton("Имя", callback_data='name'),
                    types.InlineKeyboardButton("Номер", callback_data='number'),
                    types.InlineKeyboardButton("Язык", callback_data='lang'))
settings.add(types.InlineKeyboardButton("Назад", callback_data='back'))

lang_set = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
lang_set.add(types.InlineKeyboardButton("Русский", callback_data='ru'),
                    types.InlineKeyboardButton("English", callback_data='en'),
                    types.InlineKeyboardButton("O'zbek", callback_data='uz'))
lang_set.add(types.InlineKeyboardButton("Назад", callback_data='back'))