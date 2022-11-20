from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp
from states.orders import Orders
from utils.misc import rate_limit
from utils.db_api import quick_commands
import gettext


@rate_limit(1, key="my_orders")
@dp.message_handler(Text(equals=["My orders", "Мои заказы", "Mening buyurtmalarim"]), state=None)
async def orders_view(message: types.Message, state: FSMContext):
    lang = await quick_commands.select_language(message.from_user.id)
    lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
    lan.install()
    _ = lan.gettext
    id = message.from_user.id
    orders = await quick_commands.select_all_orders_by_id(id)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if orders:
        count = 0
        for order in orders:
            if count <= 10:
                time_registered = order.created_at.strftime("%d.%m.%Y %H:%M")
                text = _("Заказ №%s от %s") % (order.id, time_registered)
                keyboard.add(types.InlineKeyboardButton(text=text, callback_data=order.id))
                count += 1
    keyboard.add(types.InlineKeyboardButton(text="Назад 🔙", callback_data='back'))
    text_msg = _("<b>Список последних 10 заказов</b>\n\nВыберите заказ для просмотра:")
    await message.answer(text_msg, reply_markup=keyboard)
    await Orders.o_main.set()


@rate_limit(1, 'orders')
@dp.callback_query_handler(state=Orders.o_main)
async def order_view(query: types.CallbackQuery, state: FSMContext):
    id = query.from_user.id
    lang = await quick_commands.select_language(id)
    lan = gettext.translation('tgbot', localedir='locales', languages=["ru"])
    lan.install()
    _ = lan.gettext
    if query.data == 'back':
        await query.message.delete()
        main_menu = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Начать заказ 🍽"),
                ],
                [
                    KeyboardButton(text="Оставить отзыв 📝"),
                    KeyboardButton(text="Мои заказы 🛒")
                ],
                [
                    KeyboardButton(text="Контакты 📲"),
                    KeyboardButton(text="Настройки 🛠")
                ]
            ],
            resize_keyboard=True
        )
        await dp.bot.send_message(id, "Главное меню 🌫", reply_markup=main_menu)
        await state.finish()
    else:
        await query.message.delete()
        order = await quick_commands.select_order_by_id(int(query.data))
        if order:
            txt = await quick_commands.admin_text(int(query.data), lang)
            status = ""
            if order.status == 1:
                status = "Ожидает подтверждения ⌛"
            elif order.status == 2:
                status = "Подтвержден ✅"
            elif order.status == 3:
                status = "В процессе приготовления 🍳"
            elif order.status == 4:
                status = "В процессе доставки 🚚"
            elif order.status == 5:
                status = "Доставлен ✅"
            elif order.status == 6:
                status = "Отменен ❌"
            # (1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен)
            txt += _("\n<i><b>Статус заказа: %s</b></i>") % status
            inline_kb1 = types.InlineKeyboardMarkup(row_width=1)
            inline_kb1.row(types.InlineKeyboardButton("Назад 🔙", callback_data="back"))
            await dp.bot.send_message(id, txt, parse_mode="HTML", reply_markup=inline_kb1)
            await Orders.o_main_action.set()
        else:
            await query.message.edit_text("Заказ не найден")

@rate_limit(1, 'orders_action')
@dp.callback_query_handler(state=Orders.o_main_action)
async def orders_a(query: types.CallbackQuery, state: FSMContext):
    id = query.from_user.id
    lang = await quick_commands.select_language(id)
    lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
    lan.install()
    _ = lan.gettext
    if query.data == 'back':
        await query.message.delete()
        orders = await quick_commands.select_all_orders_by_id(id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if orders:
            count = 0
            for order in orders:
                if count <= 10:
                    time_registered = order.created_at.strftime("%d.%m.%Y %H:%M")
                    text = "Заказ №%s от %s" % (order.id, time_registered)
                    keyboard.add(types.InlineKeyboardButton(text=text, callback_data=order.id))
                    count += 1
        keyboard.add(types.InlineKeyboardButton(text="Назад 🔙", callback_data='back'))
        text_msg = "<b>Список последних 10 заказов</b>\n\nВыберите заказ для просмотра:"
        await dp.bot.send_message(id, text_msg, reply_markup=keyboard)
        await Orders.o_main.set()


