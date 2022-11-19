from aiogram import types
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import main_menu
from keyboards.inline import courier_ed, courier_ing, courier_yn
from loader import dp
from states.orders import Admin
from utils.db_api import quick_commands
# from dotenv import load_dotenv
# from twilio.rest import Client
from utils.misc import rate_limit, get_address_from_coords


@rate_limit(1, 'courier')
@dp.callback_query_handler(state=Admin.c_main)
async def admin_courier(query: types.CallbackQuery, state: FSMContext):
    data = query.data
    id = query.from_user.id
    if data == 'refresh':
        await query.message.delete()
        user = await quick_commands.select_user(id)
        orders = await quick_commands.select_all_orders_courier(user.id)

        orders_list = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        count = 0
        count_all = 0
        for order in orders:
            status = ""
            if order.status == 1:
                status = "В обработке"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 2:
                status = "Подтвержден"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 3:
                status = "Приготовление"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 4:
                status = "Доставка"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 5:
                count_all += 1
            elif order.status == 6:
                count_all += 1
        orders_list.add(types.InlineKeyboardButton("Обновить список", callback_data="refresh"))
        orders_list.add(types.InlineKeyboardButton("Назад", callback_data="back"))
        greeting = "<b>Обновлено.</b>\n\nВам назначено <b>%s</b> заказов(а).\nВсего заказов: <b>%s</b>\n\n<i>Выберите заказ из списка ниже:</i>\n"
        greeting = greeting % (count, count_all)
        await dp.bot.send_message(id, greeting, reply_markup=orders_list)
        await Admin.c_main.set()
    elif data == 'back':
        await query.message.delete()
        await dp.bot.send_message(id, "Choose option", reply_markup=main_menu)
        await state.finish()
    elif await quick_commands.select_order_by_id(int(data)):
        await query.message.delete()
        # status (1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен)
        await state.update_data(order_id=int(data))
        order = await quick_commands.select_order_by_id(int(data))
        user = await quick_commands.select_user(order.user_id)
        user_name = user.name
        user_number = user.number
        coords = f"{order.lon},{order.lat}"
        address = get_address_from_coords(coords)  # % address[21:]
        if order.p_type == "Cash":
            delivery_price = order.delivery_price
            total_price = order.total_price
            text = "<b>Заказ <i>№%s</i></b>\n\nТип: <i>Наличные</i>\nПокупатель: %s\nНомер: %s\nАдрес: %s\nДоставка: %s\nИтого: %s\nСтатус: <b>%s</b>\n\n<i>Выберите действие:</i>\n"
            if order.status == 1 or order.status == 2 or order.status == 3:
                status = "Приготовление"
                text = text % (order.id, user_name, user_number, address[21:], delivery_price, total_price, status)
                await dp.bot.send_message(id, text, reply_markup=courier_ing)
                await Admin.c_process.set()
            elif order.status == 4:
                status = "Доставка"
                text = text % (order.id, user_name, user_number, address[21:], delivery_price, total_price, status)
                await dp.bot.send_message(id, text, reply_markup=courier_ed)
                await Admin.c_process.set()
        else:
            text = "<b>Заказ <i>№%s</i></b>\n\nТип: %s\nПокупатель: %s\nНомер: %s\nАдрес: %s\nСтатус: <b>%s</b>\n\n<i>Выберите действие:</i>\n"
            if order.p_type == "Payme":
                p_type = "Payme"

                if order.status == 1 or order.status == 2 or order.status == 3:
                    status = "Приготовление"
                    text = text % (order.id, p_type, user_name, user_number, address[21:], status)
                    await dp.bot.send_message(id, text, reply_markup=courier_ing)
                    await Admin.c_process.set()
                elif order.status == 4:
                    status = "Доставка"
                    text = text % (order.id, p_type, user_name, user_number, address[21:], status)
                    await dp.bot.send_message(id, text, reply_markup=courier_ed)
                    await Admin.c_process.set()
            elif order.p_type == "Click":
                p_type = "Click"

                if order.status == 1 or order.status == 2 or order.status == 3:
                    status = "Приготовление"
                    text = text % (order.id, p_type, user_name, user_number, address[21:], status)
                    await dp.bot.send_message(id, text, reply_markup=courier_ing)
                    await Admin.c_process.set()
                elif order.status == 4:
                    status = "Доставка"
                    text = text % (order.id, p_type, user_name, user_number, address[21:], status)
                    await dp.bot.send_message(id, text, reply_markup=courier_ed)
                    await Admin.c_process.set()


@rate_limit(1, 'c_process')
@dp.callback_query_handler(state=Admin.c_process)
async def c_process(query: types.CallbackQuery, state: FSMContext):
    data = query.data
    id = query.from_user.id
    async with state.proxy() as datap:
        order_id = datap['order_id']
    order = await quick_commands.select_order_by_id(order_id)
    if data == 'back':
        await query.message.delete()
        user = await quick_commands.select_user(id)
        orders = await quick_commands.select_all_orders_courier(user.id)
        orders_list = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        count = 0
        count_all = 0
        for order in orders:
            status = ""
            if order.status == 1:
                status = "В обработке"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 2:
                status = "Подтвержден"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 3:
                status = "Приготовление"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 4:
                status = "Доставка"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 5:
                count_all += 1
            elif order.status == 6:
                count_all += 1
        orders_list.add(types.InlineKeyboardButton("Обновить список", callback_data="refresh"))
        orders_list.add(types.InlineKeyboardButton("Назад", callback_data="back"))
        greeting = "<b>Назад</b>\n\nВам назначено <b>%s</b> заказов(а).\nВсего заказов: <b>%s</b>\n\n<i>Выберите заказ из списка ниже:</i>\n"
        greeting = greeting % (count, count_all)
        await dp.bot.send_message(id, greeting, reply_markup=orders_list)
        await Admin.c_main.set()
    elif data == 'delivery':

        await query.message.delete()
        await quick_commands.change_status(order.id, 4)
        user = await quick_commands.select_user(order.user_id)
        user_text = "Ваш заказ №%s доставляется курьером.\n\n" % order.id
        await dp.bot.send_message(order.user_id, user_text)
        user_name = user.name
        user_number = user.number
        coords = f"{order.lon},{order.lat}"
        address = get_address_from_coords(coords)  # % address[21:]
        order = await quick_commands.select_order_by_id(order.id)
        if order.p_type == "Cash":
            delivery_price = order.delivery_price
            total_price = order.total_price
            text = "<b>Заказ <i>№%s</i></b>\n\nТип: <i>Наличные</i>\nПокупатель: %s\nНомер: %s\nАдрес: %s\nДоставка: %s\nИтого: %s\nСтатус: <b>%s</b>\n\n<i>Выберите действие:</i>\n"

            status = "Доставка"
            text = text % (order.id, user_name, user_number, address[21:], delivery_price, total_price, status)
            await dp.bot.send_message(id, text, reply_markup=courier_ed)
            await Admin.c_process.set()
        else:
            text = "<b>Заказ <i>№%s</i></b>\n\nТип: %s\nПокупатель: %s\nНомер: %s\nАдрес: %s\nСтатус: <b>%s</b>\n\n<i>Выберите действие:</i>\n"
            if order.p_type == "Payme":
                p_type = "Payme"
                status = "Доставка"
                text = text % (order.id, p_type, user_name, user_number, address[21:], status)
                await dp.bot.send_message(id, text, reply_markup=courier_ed)
                await Admin.c_process.set()
            elif order.p_type == "Click":
                p_type = "Click"
                status = "Доставка"
                text = text % (order.id, p_type, user_name, user_number, address[21:], status)
                await dp.bot.send_message(id, text, reply_markup=courier_ed)
                await Admin.c_process.set()

    elif data == 'delivered':
        if order.p_type == "Cash":
            await query.message.delete()
            text = "<b>Спасибо за доставку!</b>\n\nБыл ли данный заказ (%s) оплачен?"
            text = text % order.id
            await dp.bot.send_message(id, text, reply_markup=courier_yn)
            await Admin.c_process_paid.set()

        else:
            await query.message.delete()
            await quick_commands.add_order_to_user(order.user_id)
            await quick_commands.set_cashback_to_user(order.user_id, order.id)
            await quick_commands.change_status(order.id, 5)
            user = await quick_commands.select_user(id)

            orders = await quick_commands.select_all_orders_courier(user.id)
            order = await quick_commands.select_order_by_id(order.id)
            user_text = "Ваш заказ №%s был доставлен.\n\n<i>Спасибо за заказ!</i>" % order.id
            await dp.bot.send_message(order.user_id, user_text)
            orders_list = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
            count = 0
            count_all = 0
            for order in orders:
                status = ""
                if order.status == 1:
                    status = "В обработке"
                    stat = f"№{order.id} | {status}"
                    orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                    count += 1
                    count_all += 1
                elif order.status == 2:
                    status = "Подтвержден"
                    stat = f"№{order.id} | {status}"
                    orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                    count += 1
                    count_all += 1
                elif order.status == 3:
                    status = "Приготовление"
                    stat = f"№{order.id} | {status}"
                    orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                    count += 1
                    count_all += 1
                elif order.status == 4:
                    status = "Доставка"
                    stat = f"№{order.id} | {status}"
                    orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                    count += 1
                    count_all += 1
                elif order.status == 5:
                    count_all += 1
                elif order.status == 6:
                    count_all += 1
            orders_list.add(types.InlineKeyboardButton("Обновить список", callback_data="refresh"))
            orders_list.add(types.InlineKeyboardButton("Назад", callback_data="back"))
            greeting = "<b>Заказ №%s доставлен! Спасибо.</b>\n\nВам назначено <b>%s</b> заказов(а).\nВсего заказов: <b>%s</b>\n\n<i>Выберите заказ из списка ниже:</i>\n"
            greeting = greeting % (order.id, count, count_all)
            await dp.bot.send_message(id, greeting, reply_markup=orders_list)
            await Admin.c_main.set()
    elif data == 'location':
        await dp.bot.send_location(id, order.lat, order.lon)


@rate_limit(5, 'payed_yn')
@dp.callback_query_handler(state=Admin.c_process_paid)
async def process_paid(query: types.CallbackQuery, state: FSMContext):
    data = query.data
    id = query.from_user.id
    async with state.proxy() as data_p:
        order_id = data_p['order_id']
    order = await quick_commands.select_order_by_id(order_id)
    if data == "yes":
        await query.message.delete()
        await quick_commands.add_order_to_user(order.user_id)
        await quick_commands.set_cashback_to_user(order.user_id, order.id)
        await quick_commands.change_status(order.id, 5)
        await quick_commands.change_payment_status(order.id, 1)
        user = await quick_commands.select_user(id)

        orders = await quick_commands.select_all_orders_courier(user.id)
        order = await quick_commands.select_order_by_id(order.id)
        user_text = "Ваш заказ №%s был доставлен и оплачен.\n\n<i>Спасибо за заказ!</i>" % order.id
        await dp.bot.send_message(order.user_id, user_text)
        orders_list = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        count = 0
        count_all = 0
        for order in orders:
            status = ""
            if order.status == 1:
                status = "В обработке"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 2:
                status = "Подтвержден"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 3:
                status = "Приготовление"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 4:
                status = "Доставка"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 5:
                count_all += 1
            elif order.status == 6:
                count_all += 1
        orders_list.add(types.InlineKeyboardButton("Обновить список", callback_data="refresh"))
        orders_list.add(types.InlineKeyboardButton("Назад", callback_data="back"))
        greeting = "<b>Заказ №%s доставлен и оплачен! Спасибо.</b>\n\nВам назначено <b>%s</b> заказов(а).\nВсего заказов: <b>%s</b>\n\n<i>Выберите заказ из списка ниже:</i>\n"
        greeting = greeting % (order.id, count, count_all)
        await dp.bot.send_message(id, greeting, reply_markup=orders_list)
        await Admin.c_main.set()
    else:
        await query.message.delete()
        await quick_commands.add_order_to_user(order.user_id)
        # await quick_commands.set_cashback_to_user(order.user_id, order.id)
        await quick_commands.change_status(order.id, 5)
        # await quick_commands.change_payment_status(order.id, 1)
        user = await quick_commands.select_user(id)
        orders = await quick_commands.select_all_orders_courier(user.id)
        order = await quick_commands.select_order_by_id(order.id)
        user_text = "Ваш заказ №%s был доставлен но не был оплачен.\n\n<i>Пожалуйста, свяжитесь с нами.</i>" % order.id
        await dp.bot.send_message(order.user_id, user_text)
        orders_list = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        count = 0
        count_all = 0
        for order in orders:
            status = ""
            if order.status == 1:
                status = "В обработке"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 2:
                status = "Подтвержден"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 3:
                status = "Приготовление"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 4:
                status = "Доставка"
                stat = f"№{order.id} | {status}"
                orders_list.add(types.InlineKeyboardButton(stat, callback_data=order.id))
                count += 1
                count_all += 1
            elif order.status == 5:
                count_all += 1
            elif order.status == 6:
                count_all += 1
        orders_list.add(types.InlineKeyboardButton("Обновить список", callback_data="refresh"))
        orders_list.add(types.InlineKeyboardButton("Назад", callback_data="back"))
        greeting = "<b>Заказ №%s доставлен без получения оплаты! Спасибо.</b>\n\nВам назначено <b>%s</b> заказов(а).\nВсего заказов: <b>%s</b>\n\n<i>Выберите заказ из списка ниже:</i>\n"
        greeting = greeting % (order.id, count, count_all)
        await dp.bot.send_message(id, greeting, reply_markup=orders_list)
        await Admin.c_main.set()
