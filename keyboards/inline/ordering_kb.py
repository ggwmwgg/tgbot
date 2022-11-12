from aiogram import types

from data import lang_en

# Кнопки на профиле поиска в админке
no_comm = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
no_comm.add(types.InlineKeyboardButton("Нет комментариев", callback_data='no_comm'),
            types.InlineKeyboardButton("Назад", callback_data='back'))


payment_type = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
payment_type.add(types.InlineKeyboardButton("Наличные", callback_data='cash'),
                    types.InlineKeyboardButton("Click", callback_data='click'),
                    types.InlineKeyboardButton("Payme", callback_data='payme'),
                    types.InlineKeyboardButton("Назад", callback_data='back'))


conf = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
conf.add(types.InlineKeyboardButton("Подтверждаю", callback_data='yes'),
            types.InlineKeyboardButton("Отменить", callback_data='no'))