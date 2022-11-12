from aiogram import types

from data import lang_en

# Кнопки на профиле поиска в админке
keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
keyboard_markup.add(types.InlineKeyboardButton(lang_en.name_eng, callback_data='name'),
                    types.InlineKeyboardButton(lang_en.language_eng, callback_data='lang'),
                    types.InlineKeyboardButton(lang_en.number_eng, callback_data='number'),
                    types.InlineKeyboardButton(lang_en.cashback_eng, callback_data='cashback'),
                    types.InlineKeyboardButton(lang_en.ban_eng, callback_data='ban'),
                    types.InlineKeyboardButton(lang_en.rights_eng, callback_data='is_admin'),
                    types.InlineKeyboardButton(lang_en.back_eng, callback_data='back'))


lang_markup = types.InlineKeyboardMarkup(row_width=1)
lang_markup.add(types.InlineKeyboardButton(lang_en.russian_eng, callback_data='ru'),
                    types.InlineKeyboardButton(lang_en.uzbek_eng, callback_data='uz'),
                    types.InlineKeyboardButton(lang_en.english_eng, callback_data='en'))


ban_markup = types.InlineKeyboardMarkup(row_width=1)
ban_markup.add(types.InlineKeyboardButton(lang_en.bann_eng, callback_data='ban'),
                    types.InlineKeyboardButton(lang_en.unbann_eng, callback_data='unban'))


rights_markup = types.InlineKeyboardMarkup(row_width=1)
rights_markup.add(types.InlineKeyboardButton(lang_en.admin_eng, callback_data='1'),
                    types.InlineKeyboardButton(lang_en.operator_eng, callback_data='2'),
                    types.InlineKeyboardButton(lang_en.courier_eng, callback_data='3'),
                    types.InlineKeyboardButton(lang_en.user_eng, callback_data='0'))

orders_a = types.InlineKeyboardMarkup(row_width=1)
orders_a.row(types.InlineKeyboardButton("Все", callback_data='all'),
                    types.InlineKeyboardButton("<= Активные", callback_data='all_a'))
orders_a.row(types.InlineKeyboardButton("Все по филиалу", callback_data='branch'),
                    types.InlineKeyboardButton("<= Активные", callback_data='branch_a'))
orders_a.row(types.InlineKeyboardButton("Все по id/номеру пользователя", callback_data='num_id'),
                    types.InlineKeyboardButton("<= Активные", callback_data='num_id_a'))
orders_a.row(types.InlineKeyboardButton("Инфо по id заказа", callback_data='num_id_o'))
orders_a.row(types.InlineKeyboardButton("Назад", callback_data='back'))

# status (1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен)

order_info = types.InlineKeyboardMarkup(row_width=1)
order_info.row(types.InlineKeyboardButton("Подтвержден", callback_data='confirmed'),
                    types.InlineKeyboardButton("Приготовление", callback_data='cooking'))
order_info.row(types.InlineKeyboardButton("Доставка", callback_data='delivery'),
                    types.InlineKeyboardButton("Доставлен", callback_data='delivered'))
order_info.row(types.InlineKeyboardButton("Оплачен", callback_data='payed'),
                    types.InlineKeyboardButton("Не оплачен", callback_data='not_payed'))
order_info.row(types.InlineKeyboardButton("Добавить позицию", callback_data='add_pos'),
                    types.InlineKeyboardButton("Удалить позицию", callback_data='remove_pos'))
order_info.row(types.InlineKeyboardButton("Отменить заказ", callback_data='cancel'))
order_info.row(types.InlineKeyboardButton("Назначить курьера", callback_data='courier_set'))
order_info.row(types.InlineKeyboardButton("Назад", callback_data='back'))
