from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from loader import dp
from states.orders import Order
from utils.db_api import quick_commands
from data.config import cashback as cb
from utils.misc import rate_limit, get_address_from_coords


# Корзина тест
@rate_limit(1, key="cart")
# @dp.message_handler(Text(equals=["Корзина"]), state=Order.menu)
# @dp.message_handler(Text(equals=["Корзина"]), state=Order.menu_subcat)
# @dp.message_handler(Text(equals=["Корзина"]), state=Order.menu_item)


# Начало оформления заказа
@rate_limit(1, key="cart")
async def start_order(message: types.Message, state: FSMContext):
    id = message.from_user.id

    lang = await quick_commands.select_language(id)

    if await quick_commands.select_cart(id):


        lil = await message.answer(text="Загрузка заказа", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        await lil.delete()

        no_comm = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        no_comm.add(types.InlineKeyboardButton("Нет комментариев 💭", callback_data='no_comm'),
                    types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        text = "Добавьте комментарий к вашему заказу\nИли нажмите на соответствующую кнопку\n"
        lul = await message.answer(text, reply_markup=no_comm)
        msg = lul['message_id']
        await state.update_data(msg_id=msg)
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

        await message.answer("Ваша корзина пуста", reply_markup=main_menu)
        cats = await quick_commands.get_categories(lang)
        cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
            *[KeyboardButton(text=cat) for cat in cats])
        await message.answer("Выберите категорию", reply_markup=cat_lan)
        await Order.menu.set()


# Функция для нажатия на кнопку нет комментариев и назад
@dp.callback_query_handler(state=Order.menu_confirm)
async def comment_order_query(query: types.CallbackQuery, state: FSMContext):
    global lang
    id = query.from_user.id
    lang = await quick_commands.select_language(id)


    if query.data == "no_comm":
        text = "<b>Напишите комментарий к заказу:</b>\n\nКомментариев не добавлено"
        await query.message.edit_text(text=text, parse_mode="HTML", reply_markup=None)

        payment_type = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        payment_type.add(types.InlineKeyboardButton("Наличные 💵", callback_data='cash'),
                         types.InlineKeyboardButton("Click 💸", callback_data='click'),
                         types.InlineKeyboardButton("Payme 💸", callback_data='payme'),
                         types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        lilo = await dp.bot.send_message(chat_id=id, text="<b>Выберите способ оплаты:</b>", parse_mode="HTML", reply_markup=payment_type)
        await state.update_data(msg_id=lilo['message_id'])
        await Order.menu_confirm_payment.set()
    elif query.data == "back":

        text = "<b>Напишите комментарий к заказу\n</b>"
        await dp.bot.delete_message(chat_id=id, message_id=query.message.message_id)
        cats = await quick_commands.get_categories(lang)
        cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
            *[KeyboardButton(text=cat) for cat in cats])
        await dp.bot.send_message(chat_id=id, text="Выберите категорию", reply_markup=cat_lan)
        await Order.menu.set()

# Функция добавления комментария к заказу
@dp.message_handler(state=Order.menu_confirm)
async def comment_comm_msg(message: types.Message, state: FSMContext):
    global lang
    id = message.from_user.id
    lang = await quick_commands.select_language(id)
    await state.update_data(comment=message.text)
    async with state.proxy() as data:
        msg_id = data['msg_id']
        # print(msg_id)
    await dp.bot.edit_message_text(chat_id=id, message_id=msg_id, text="<b>Комментарий:</b>\n\n", parse_mode="HTML")

    payment_type = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
    payment_type.add(types.InlineKeyboardButton("Наличные 💵", callback_data='cash'),
                     types.InlineKeyboardButton("Click 💸", callback_data='click'),
                     types.InlineKeyboardButton("Payme 💸", callback_data='payme'),
                     types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

    lilo = await message.answer(text="<b>Выберите способ оплаты:</b>", parse_mode="HTML", reply_markup=payment_type)
    await state.update_data(msg_id=lilo['message_id'])
    await Order.menu_confirm_payment.set()


# Обработка способов оплаты (Выбран Payme, Click, Cash) и вывод списка товаров в корзине
# Функция для нажатия на кнопку нет комментариев и назад
@dp.callback_query_handler(state=Order.menu_confirm_payment)
async def payment_order_query(query: types.CallbackQuery, state: FSMContext):
    global lang
    id = query.from_user.id
    user = await quick_commands.select_user(id)
    lang = await quick_commands.select_language(id)
    async with state.proxy() as data:
        msg_id = data['msg_id']
        type = ""
        if query.data == "payme":
            type = "Payme"
        elif query.data == "click":
            type = "Click"
        elif query.data == "cash":
            type = "Наличные"
        comment = ""
        branch = user.branch
        pr = "сум"
        total = "Итого"
        address_str = get_address_from_coords(f"{user.longitude},{user.latitude}")
        adress = address_str[21:]
        try:
            comment = data['comment']
        except:
            comment = "Нет комментариев"
        cart = "<b>Содержимое:</b>\n\n"
        txt = ""
        price_total = 0
        for item in await quick_commands.select_cart(id):
            name = await quick_commands.select_item_name(item.item_id, lang)
            price = await quick_commands.select_item_price(item.item_id)
            price_total += item.price
            cart += f"<b>{name}</b>\n" + f"<b>{item.quantity}</b>" + " x " + f"{price}" + " = " + f"{item.price} {pr}\n\n"
        if user.last == 1:
            price_total += user.last_delivery
            for_txt = f"\n\nТип: Доставка\nАдрес: {adress}\nНомер: {user.number}\nСпособ оплаты: {type}\n"
            text = f"<b>Подтвердите заказ:</b>\n\nТип: Доставка\nАдрес: {adress}\nНомер: {user.number}\nСпособ оплаты: {type}\n"
            if comment != "Нет комментариев":
                text += f"Комментарий: {comment}\n"
                for_txt += f"Комментарий: {comment}\n"

            txt_for = cart + f"<b>Доставка</b> = <b><i>{user.last_delivery} {pr}</i></b>\n\n<b><i>{total}: </i>" + f"{price_total} {pr}</b>\n\n\n<b><i>Заказ оформлен</i></b>\n<i>Скоро с вами свяжется оператор</i>"
            txt = for_txt + txt_for
            cart += f"<b>Доставка</b> = <b><i>{user.last_delivery} {pr}</i></b>\n\n<b><i>{total}: </i>" + f"{price_total} {pr}</b>\n\n<i>Доставим товары в течение часа</i>\n\n\n<b><i>Вы подтверждаете заказ?</i></b>"
            text += f"\n{cart}"
            await state.update_data(price_total=price_total)
            await state.update_data(delivery_price=user.last_delivery)


        elif user.last == 2:
            for_txt = f"\n\nТип: Самовывоз\nФилиал: {branch}\nНомер: {user.number}\nСпособ оплаты: {type}\n"
            text = f"<b>Подтвердите заказ:</b>\n\nТип: Самовывоз\nФилиал: {branch}\nНомер: {user.number}\nСпособ оплаты: {type}\n"
            if comment != "Нет комментариев":
                text += f"Комментарий: {comment}\n"
                for_txt += f"Комментарий: {comment}\n"

            txt_for = f"\n<b><i>{total}: </i>" + f"{price_total} {pr}</b>\n\n\n<b><i>Заказ оформлен</i></b>\n<i>Скоро с вами свяжется оператор</i>"
            txt = for_txt + cart + txt_for
            cart += f"\n<b><i>{total}: </i>" + f"{price_total} {pr}</b>\n\n<i>Приготовим ваш заказ в течение часа</i>\n\n\n<b><i>Вы подтверждаете заказ?</i></b>"
            text = f"<b>Подтвердите заказ:</b>\n\nТип: Самовывоз\nФилиал: {branch}\nНомер: {user.number}\nСпособ оплаты: {type}\n"
            text += f"\n{cart}"
            await state.update_data(price_total=price_total)
            await state.update_data(delivery_price=0)



        text_edit = f"<b>Выбрано:</b>\n\n{type}"


    if query.data == "cash":
        await query.message.edit_text(text_edit, parse_mode="html")
        # await dp.bot.edit_message_text(chat_id=id, message_id=msg_id, text=text_edit, parse_mode="HTML")

        conf = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        conf.add(types.InlineKeyboardButton("Подтверждаю ✔", callback_data='yes'),
                 types.InlineKeyboardButton("Отменить ✖", callback_data='no'))

        lilo = await dp.bot.send_message(chat_id=id, text=text, reply_markup=conf)
        await state.update_data(msg_id=lilo['message_id'])
        await state.update_data(type=type)
        await state.update_data(text=txt)
        await Order.menu_confirmed.set()


    elif query.data == "click":
        pass
    elif query.data == "payme":

        pass
    elif query.data == "back":
        await query.message.delete()
        if await quick_commands.select_cart(id):

            no_comm = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
            no_comm.add(types.InlineKeyboardButton("Нет комментариев 💭", callback_data='no_comm'),
                        types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

            text = "Добавьте комментарий к вашему заказу\nИли нажмите на соответствующую кнопку\n"
            lul = await dp.bot.send_message(chat_id=id, text=text,
                                       reply_markup=no_comm)
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

            await dp.bot.send_message(chat_id=id, text="Ваша корзина пуста", reply_markup=main_menu)
            cats = await quick_commands.get_categories(lang)
            cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
                *[KeyboardButton(text=cat) for cat in cats])
            await dp.bot.send_message(chat_id=id, text="Выберите категорию", reply_markup=cat_lan)
            await Order.menu.set()



# Подтверждение заказа, отправка в бд, отправка сообщения оператору для дальнейшей обработки
@dp.callback_query_handler(state=Order.menu_confirmed)
async def menu_confirmed(query: types.CallbackQuery, state: FSMContext):
    id = query.from_user.id
    user = await quick_commands.select_user(id)
    async with state.proxy() as data:
        # msg_id = data['msg_id']
        type = data['type']
        txt_i = data['text']
        total_price = data['price_total']
        delivery_price = data['delivery_price']
        cashback = int(total_price * cb)
        type_delivery = user.last
        lon = user.longitude
        lat = user.latitude
        branch = user.branch
    if query.data == "yes":
        if type == "Наличные":
            is_paid = 0
            p_type = "Cash"
            items = {}
            for i in await quick_commands.select_cart(id):
                items[i.item_id] = i.quantity
            try:
                comment = data['comment']
            except:
                comment = "Null"
            await quick_commands.add_order(id, p_type, items, comment, total_price, delivery_price, cashback,
                                           type_delivery, is_paid, lon, lat, branch)
            order = await quick_commands.select_last_order_by_id(id)
            txt = f"<b>Заказ №{order.id}</b>" + txt_i
            for_admins = f"<b>Новый заказ:</b> {order.id}\n\nОжидает вашего подтверждения"
            for i in await quick_commands.select_operators():
                await dp.bot.send_message(chat_id=i, text=for_admins)
            await quick_commands.clear_cart_by_user_id(id)
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

            await dp.bot.send_message(chat_id=id, text=txt, parse_mode="HTML", reply_markup=main_menu)
            await state.finish()
        if type == "Click":
            pass
        if type == "Payme":
            pass

    elif query.data == "no":
        await query.message.delete()

        payment_type = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        payment_type.add(types.InlineKeyboardButton("Наличные 💵", callback_data='cash'),
                         types.InlineKeyboardButton("Click 💸", callback_data='click'),
                         types.InlineKeyboardButton("Payme 💸", callback_data='payme'),
                         types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        lilo = await dp.bot.send_message(chat_id=id, text="<b>Выберите способ оплаты:</b>", parse_mode="HTML", reply_markup=payment_type)
        await state.update_data(msg_id=lilo['message_id'])
        await Order.menu_confirm_payment.set()
        pass