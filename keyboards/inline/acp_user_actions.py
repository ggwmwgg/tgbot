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


order_by_id_quantity = types.InlineKeyboardMarkup(row_width=5)
order_by_id_quantity.add(types.InlineKeyboardButton("1", callback_data="1"),
                         types.InlineKeyboardButton("2", callback_data="2"),
                         types.InlineKeyboardButton("3", callback_data='3'),
                         types.InlineKeyboardButton("4", callback_data='4'),
                         types.InlineKeyboardButton("5", callback_data='5'))
order_by_id_quantity.add(types.InlineKeyboardButton("6", callback_data="6"),
                         types.InlineKeyboardButton("7", callback_data="7"),
                         types.InlineKeyboardButton("8", callback_data='8'),
                         types.InlineKeyboardButton("9", callback_data='9'),
                         types.InlineKeyboardButton("10", callback_data='10'))
order_by_id_quantity.add(types.InlineKeyboardButton("11", callback_data="11"),
                         types.InlineKeyboardButton("12", callback_data="12"),
                         types.InlineKeyboardButton("13", callback_data='13'),
                         types.InlineKeyboardButton("14", callback_data='14'),
                         types.InlineKeyboardButton("15", callback_data='15'))
order_by_id_quantity.add(types.InlineKeyboardButton("16", callback_data="16"),
                         types.InlineKeyboardButton("17", callback_data="17"),
                         types.InlineKeyboardButton("18", callback_data='18'),
                         types.InlineKeyboardButton("19", callback_data='19'),
                         types.InlineKeyboardButton("20", callback_data='20'))
order_by_id_quantity.add(types.InlineKeyboardButton("21", callback_data="21"),
                         types.InlineKeyboardButton("22", callback_data="22"),
                         types.InlineKeyboardButton("23", callback_data='23'),
                         types.InlineKeyboardButton("24", callback_data='24'),
                         types.InlineKeyboardButton("25", callback_data='25'))
