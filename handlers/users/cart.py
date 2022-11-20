from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from loader import dp
from states.orders import Order
from utils.db_api import quick_commands
from utils.misc import rate_limit


comments = "Добавьте комментарий к вашему заказу\nИли нажмите на соответствующую кнопку\n"

# Корзина
@rate_limit(1, key="cart")
async def show_cart(message: types.Message):
    id = message.from_user.id
    lang = await quick_commands.select_language(id=id)
    back = "Назад"
    clear = "Очистить"
    order = "Оформить заказ"
    cirt = "Корзина"
    tot = "Итого"
    pr = "сум"
    dll = "Доставка"
    info = f"Нажмите на название товара для его удаления\n{clear} для очистки корзины\n{order} для оформления заказа\n\n"
    if await quick_commands.select_cart(id):
        user_cart = await quick_commands.select_user(id)
        kok = f"<b>{cirt}:\n\n</b>"
        price_total = 0
        for item in await quick_commands.select_cart(id):
            name = await quick_commands.select_item_name(item.item_id, lang)
            price = await quick_commands.select_item_price(item.item_id)
            price_total += item.price
            kok += f"<b>{name}</b>\n" + f"<b>{item.quantity}</b>" + " x " + f"{price}" + " = " + f"{item.price} {pr}\n\n"
        if user_cart.last == 1:
            price_total += user_cart.last_delivery
            kok += f"<b>{dll}</b> = <b><i>{user_cart.last_delivery} {pr}</i></b>\n\n"
        kok += "\n" + f"<b><i>{tot}: </i>" + f"{price_total} {pr}</b>\n\n" + info
        cats = await quick_commands.get_cart_list(id, lang)
        inline_kb1 = types.InlineKeyboardMarkup(row_width=1)
        for a in cats:
            b = a[:-2]
            inline_kb1.add(types.InlineKeyboardButton(a, callback_data=b))
        inline_kb1.row(types.InlineKeyboardButton(back, callback_data="back"),
                       types.InlineKeyboardButton(clear, callback_data="clear"))
        inline_kb1.row(types.InlineKeyboardButton(order, callback_data="order"))
        lil = await message.answer(text="Загрузка корзины", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        await lil.delete()
        lilo = await message.answer(text=kok, parse_mode="HTML",reply_markup=inline_kb1)
        koker = lilo.message_id
        await Order.menu_cart.set()
    else:

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

        await message.answer("Ваша корзина пуста", reply_markup=main_menu)
        cats = await quick_commands.get_categories(lang)
        cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
            *[KeyboardButton(text=cat) for cat in cats])
        await message.answer("Выберите категорию", reply_markup=cat_lan)
        await Order.menu.set()


@dp.callback_query_handler(state=Order.menu_cart)
async def inline_cart_callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  # send answer to close the rounding circle
    id = query.from_user.id
    lang = await quick_commands.select_language(id)
    data = query.data
    back = "Назад"
    clear = "Очистить"
    order = "Оформить заказ"
    cirt = "Корзина"
    tot = "Итого"
    pr = "сум"
    dll = "Доставка"
    list = await quick_commands.get_cart_list_nox(id, lang)
    user_cart = await quick_commands.select_user(id)

    if data in list:  # Удаление из корзины
        item_id = await quick_commands.get_item_by_name(data, lang)
        await quick_commands.delete_cart_by_itemid(id, item_id.id)
        deleted = f"<i>Товар {data} удален из корзины</i>\n\n"
        info = f"Нажмите на название товара для его удаления\n{clear} для очистки корзины\n{order} для оформления заказа\n\n"
        kok = f"<b>{cirt}:\n\n</b>"
        price_total = 0
        for item in await quick_commands.select_cart(id):
            name = await quick_commands.select_item_name(item.item_id, lang)
            price = await quick_commands.select_item_price(item.item_id)
            price_total += item.price
            kok += f"<b>{name}</b>\n" + f"<b>{item.quantity}</b>" + " x " + f"{price}" + " = " + f"{item.price} сум\n\n"
        if user_cart.last == 1:
            price_total += user_cart.last_delivery
            kok += f"<b>{dll}</b> = <b><i>{user_cart.last_delivery} {pr}</i></b>\n\n"
        kok += "\n" + f"<b><i>{tot}: </i>" + f"{price_total} {pr}</b>\n\n" + info + deleted
        cats = await quick_commands.get_cart_list(id, lang)
        inline_kb1 = types.InlineKeyboardMarkup(row_width=1)
        for a in cats:
            b = a[:-2]
            inline_kb1.add(types.InlineKeyboardButton(a, callback_data=b))
        inline_kb1.row(types.InlineKeyboardButton(back, callback_data="back"),
                       types.InlineKeyboardButton(clear, callback_data="clear"))
        inline_kb1.row(types.InlineKeyboardButton(order, callback_data="order"))
        await query.message.edit_text(text=kok, parse_mode="HTML")
        await query.message.edit_reply_markup(reply_markup=inline_kb1)
        await Order.menu_cart.set()
    elif data == 'clear':  # Очистка корзины
        await quick_commands.clear_cart_by_user_id(id)
        text = f"<b>Корзина очищена</b>"
        await query.message.edit_text(text=text, parse_mode="HTML")
        cats = await quick_commands.get_categories(lang)
        cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
            *[KeyboardButton(text=cat) for cat in cats])
        await dp.bot.send_message(chat_id=id, text="Выберите категорию", reply_markup=cat_lan)
        await Order.menu.set()
    elif data == 'back':  # Назад
        text = "<b>" + back + "</b>"
        await query.message.edit_text(text=text, parse_mode="HTML")
        cats = await quick_commands.get_categories(lang)
        cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
            *[KeyboardButton(text=cat) for cat in cats])
        await dp.bot.send_message(chat_id=id, text="Выберите категорию", reply_markup=cat_lan)
        await Order.menu.set()
    elif data == 'order':  # Оформить заказ
        if await quick_commands.select_cart(id):
            await query.message.delete()
            lil = await dp.bot.send_message(id, text="Загрузка заказа", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
            await lil.delete()

            no_comm = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
            no_comm.add(types.InlineKeyboardButton("Нет комментариев 💭", callback_data='no_comm'),
                        types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

            lul = await dp.bot.send_message(id, comments, reply_markup=no_comm)
            await state.update_data(msg_id=lul['message_id'])
            await Order.menu_confirm.set()
        else:

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

            await dp.bot.send_message(id, "Ваша корзина пуста", reply_markup=main_menu)
            cats = await quick_commands.get_categories(lang)
            cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
                *[KeyboardButton(text=cat) for cat in cats])
            await dp.bot.send_message(id, "Выберите категорию", reply_markup=cat_lan)
            await Order.menu.set()


@dp.callback_query_handler(state=Order.menu_cart)
async def inline_cart_callback_handler(message:types.Message, state: FSMContext):
    id = message.from_user.id
    lang = await quick_commands.select_language(id)
    if message.text == "Назад":
        cats = await quick_commands.get_categories(lang)
        cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
            *[KeyboardButton(text=cat) for cat in cats])
        await message.answer("Выберите категорию", reply_markup=cat_lan)
        await Order.menu.set()
    else:
        await message.answer("Неверная команда, используйте кнопки под сообщением")