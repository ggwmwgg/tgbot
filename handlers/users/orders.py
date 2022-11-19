from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from aiogram.types import ReplyKeyboardRemove, ContentType

from keyboards.default import main_menu
from loader import dp
from states.orders import Orders

from data import lang_en
from datetime import datetime
from utils.misc import rate_limit
from utils.db_api import quick_commands
import gettext


_ = gettext.gettext


@rate_limit(1, key="my_orders")
@dp.message_handler(Text(equals=["My orders", "Мои заказы"]), state=None)
async def orders_view(message: types.Message, state: FSMContext):
    id = message.from_user.id
    orders = await quick_commands.select_all_orders_by_id(id)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if orders:
        count = 0
        for order in orders:
            if count <= 10:
                time_registered = order.created_at.strftime("%d.%m.%Y %H:%M")
                text = lang_en.button_o_txt % (order.id, time_registered)
                keyboard.add(types.InlineKeyboardButton(text=text, callback_data=order.id))
                count += 1
    keyboard.add(types.InlineKeyboardButton(text=lang_en.back_eng, callback_data='back'))
    text_msg = lang_en.orders_view_txt
    await message.answer(text_msg, reply_markup=keyboard)
    await Orders.o_main.set()


@rate_limit(1, 'orders')
@dp.callback_query_handler(state=Orders.o_main)
async def order_view(query: types.CallbackQuery, state: FSMContext):
    id = query.from_user.id
    lang = await quick_commands.select_language(id)
    if query.data == 'back':
        await query.message.delete()
        await dp.bot.send_message(id, lang_en.orders_main_menu_txt, reply_markup=main_menu)
        await state.finish()
    else:
        await query.message.delete()
        order = await quick_commands.select_order_by_id(int(query.data))
        if order:
            txt = await quick_commands.admin_text(int(query.data), lang)
            status = ""
            if order.status == 1:
                status = lang_en.orders_status_1
            elif order.status == 2:
                status = lang_en.orders_status_2
            elif order.status == 3:
                status = lang_en.orders_status_3
            elif order.status == 4:
                status = lang_en.orders_status_4
            elif order.status == 5:
                status = lang_en.orders_status_5
            elif order.status == 6:
                status = lang_en.orders_status_6
            # (1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен)
            txt += lang_en.orders_status_txt % status
            inline_kb1 = types.InlineKeyboardMarkup(row_width=1)
            inline_kb1.row(types.InlineKeyboardButton(lang_en.back_eng, callback_data="back"))
            await dp.bot.send_message(id, txt, parse_mode="HTML", reply_markup=inline_kb1)
            await Orders.o_main_action.set()
        else:
            await query.message.edit_text(lang_en.orders_not_found_txt)

@rate_limit(1, 'orders_action')
@dp.callback_query_handler(state=Orders.o_main_action)
async def orders_a(query: types.CallbackQuery, state: FSMContext):
    id = query.from_user.id
    lang = await quick_commands.select_language(id)
    if query.data == 'back':
        await query.message.delete()
        orders = await quick_commands.select_all_orders_by_id(id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if orders:
            count = 0
            for order in orders:
                if count <= 10:
                    time_registered = order.created_at.strftime("%d.%m.%Y %H:%M")
                    text = lang_en.button_o_txt % (order.id, time_registered)
                    keyboard.add(types.InlineKeyboardButton(text=text, callback_data=order.id))
                    count += 1
        keyboard.add(types.InlineKeyboardButton(text=lang_en.back_eng, callback_data='back'))
        text_msg = lang_en.orders_view_txt
        await dp.bot.send_message(id, text_msg, reply_markup=keyboard)
        await Orders.o_main.set()


