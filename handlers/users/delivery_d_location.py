from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text, Command
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from keyboards.default import location, d_or_d, yes_no, main_menu, delivery_yes_no, languages, old_d_or_d
from loader import dp
from states.orders import Order, Reg
from utils.db_api import quick_commands
from data import lang_en
# import os
# from dotenv import load_dotenv
# from twilio.rest import Client
# from random import randint
# from utils.db_api.models import User
from utils.misc import rate_limit, get_address_from_coords
from utils.misc.calc_distance import choose_shortest_kek


# Доставка или самовывоз?
@rate_limit(1, key="order")
@dp.message_handler(Command("order"), state=None)
@dp.message_handler(Text(equals=[lang_en.order_eng]), state='*')
async def start_ordering(message: types.Message):
    if await quick_commands.select_user(id=message.from_user.id):
        if await quick_commands.check_last_order_data(message.from_user.id):
            user = await quick_commands.select_user(id=message.from_user.id)
            latitude = user.latitude
            longitude = user.longitude
            branch = user.branch

            type = ""
            if user.last == 1:
                type = "Доставка"
            elif user.last == 2:
                type = "Самовывоз"
            a_ss = ""
            try:
                address_str = get_address_from_coords(f"{longitude},{latitude}")
                a_ss = address_str[21:]
            except:
                a_ss = "Error"

            type = f"Хотите ли вы использовать данные с последнего заказа?\n\n<b>Тип доставки:</b> {type}\n<b>Адрес доставки:</b> {a_ss}\n<b>Филиал:</b> {branch}\n\n<b><i>Или хотите использовать новые данные?</i></b>"
            await message.answer(type, reply_markup=old_d_or_d)
            await Order.d_or_d.set()


        else:
            await message.answer("Вам нужна доставка или самовывоз?", reply_markup=d_or_d)
            await Order.asklocation.set()
    else:
        await message.answer(f"Здравствуйте, {message.from_user.full_name}!\n"
                             "Выберите язык обслуживания.\n\n"
                             f"Hello, {message.from_user.full_name}!\n"
                             "Please, choose your language\n\n"
                             f"Keling, {message.from_user.full_name}!\n"
                             "Avvaliga xizmat ko'rsatish tilini tanlab olaylik", reply_markup=languages)

        await Reg.language.set()


# Использовать ли старые данные
@rate_limit(1, key="delivery")
@dp.message_handler(state=Order.d_or_d)
async def ask_delivery(message: types.Message):
    id = message.from_user.id
    lang = await quick_commands.select_language(id)

    if message.text == "Использовать старые данные":
        cats = await quick_commands.get_categories(lang)
        cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
            *[KeyboardButton(text=cat) for cat in cats])
        await message.answer("Начнем заказ?", reply_markup=cat_lan)
        # print(cats)
        await quick_commands.update_last_order_type(message.from_user.id, 1)
        await Order.menu.set()
    elif message.text == "Указать новые данные":
        await message.answer("Вам нужна доставка или самовывоз?", reply_markup=d_or_d)
        await quick_commands.update_last_order_type(id, 0)
        await quick_commands.update_last_branch(id, "Null")
        await quick_commands.update_last_order_coords(id, 0, 0)
        await Order.asklocation.set()
    else:
        await message.answer("Выберите один из вариантов на клавиатуре", reply_markup=old_d_or_d)


# При выборе доставки, просьба отправить локацию
@rate_limit(1, key="delivery")
@dp.message_handler(Text(equals=[lang_en.delivery_eng]), state=Order.asklocation)
async def ask_delivery(message: types.Message):
    await message.answer("Пожалуйста, отправьте вашу локацию вручную или с помощью кнопки "
                         "для определения ближайшего до Вас филиала для доставки", reply_markup=location)

    await Order.location_delivery.set()

# Назад в отправке локации
@dp.message_handler(Text(equals=[lang_en.back_eng]), state=Order.location_delivery)
async def ask_delivery(message: types.Message):
    await message.answer("Вам нужна доставка или самовывоз?", reply_markup=d_or_d)
    await Order.asklocation.set()




# Подтверждение адреса доставки и добавление его в бд.
@rate_limit(1, key="delivery")
@dp.message_handler(content_types=types.ContentType.LOCATION, state=Order.location_delivery)
async def delivery_set(message: types.Message, state: FSMContext):
    location = message.location
    await state.update_data(location=location)  # Запись локации для доставки в бд
    # print(location)
    address_str = get_address_from_coords(f"{location.longitude},{location.latitude}")

    a_ss = address_str[21:]
    await message.answer(f"Ваш адрес {a_ss}.\n"
                         f"Вы подтверждаете данный адрес или хотите отправить заново?",
                         reply_markup=delivery_yes_no)

    await Order.location_delivery_another.set()


# Назад в подтверждении адреса доставки
@dp.message_handler(Text(equals=[lang_en.back_eng]), state=Order.location_delivery_another)
async def ask_delivery(message: types.Message):
    await message.answer("Вам нужна доставка или самовывоз?", reply_markup=d_or_d)
    await Order.asklocation.set()


# Подтверждение адреса доставки. Отправить заново.
@rate_limit(1, key="delivery")
@dp.message_handler(Text(equals=[lang_en.send_again_eng]), state=Order.location_delivery_another)
async def confirmed_delivery(message: types.Message):
    await message.answer("Пожалуйста, отправьте вашу локацию вручную или с помощью кнопки "
                         "для определения ближайшего до Вас филиала для доставки", reply_markup=location)

    await Order.location_delivery.set()


# Адрес для доставки подтвержден, начало заказа
@rate_limit(1, key="delivery")
@dp.message_handler(Text(equals=[lang_en.confirm_eng]), state=Order.location_delivery_another)
async def confirmed_delivery(message: types.Message, state: FSMContext):
    id = message.from_user.id
    lang = await quick_commands.select_language(id)
    cats = await quick_commands.get_categories(lang)
    async with state.proxy() as data:
        location_delivery = data["location"]

        # print(location_delivery)
        # print(location_delivery.latitude)
        # print(location_delivery.longitude)
        closest_shops = await choose_shortest_kek(location_delivery)
        # print(closest_shops)
        text = ""
        del_price = 0
        for shop_name, distance, url, shop_location in closest_shops:
            # print(distance)
            kek = (distance + 2000) / 1000
            dist = round(kek, 1) + 1
            # print(shop_location)
            if dist < 3:
                del_price = 10000
            elif dist >= 3 and dist < 7:
                del_price = 15000
            else:
                del_price = 20000
            text = "Выбран филиал: %s\nРасстояние до него %s км.\nСтоимость доставки: %s сум\n\nНачнем заказ?" % (shop_name, dist, del_price)
        await quick_commands.update_delivery_price(id, del_price)

        # await message.answer(text, reply_markup=ReplyKeyboardRemove())
        await quick_commands.update_last_order_coords(message.from_user.id, location_delivery.latitude,
                                                      location_delivery.longitude)
        for shop_name, distance, url, shop_location in closest_shops:
            await state.update_data(branch=shop_name)
            await quick_commands.update_last_branch(message.from_user.id, shop_name)
    cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(*[KeyboardButton(text=cat) for cat in cats])
    await message.answer(text, reply_markup=cat_lan)
    # print(cats)
    await quick_commands.update_last_order_type(message.from_user.id, 1)
    await Order.menu.set()


# Адрес для самовывоза
@rate_limit(2, key="location")
@dp.message_handler(Text(equals=[lang_en.pickup_eng]), state=Order.asklocation)
async def ask_drive_thru(message: types.Message):
    await message.answer("Пожалуйста, отправьте вашу локацию вручную или с помощью кнопки "
                         "для определения ближайшего к Вам филиала", reply_markup=location)

    await Order.location_drive.set()


# Назад в отправке локации
@dp.message_handler(Text(equals=[lang_en.back_eng]), state=Order.location_drive)
async def ask_delivery(message: types.Message):
    await message.answer("Вам нужна доставка или самовывоз?", reply_markup=d_or_d)
    await Order.asklocation.set()


# Подтверждение филиала для самовывоза
@rate_limit(2, key="drive")
@dp.message_handler(content_types=types.ContentType.LOCATION, state=Order.location_drive)
async def ask_again_drive(message: types.Message, state: FSMContext):
    location_drive = message.location
    closest_shops = await choose_shortest_kek(location_drive)
    await state.update_data(location=location_drive)  # Запись локации для доставки в бд

    text = "\n\n".join([f"Ближайший филиал: {shop_name}. <a href='{url}'>Google</a>\n"
                        f"Расстояние до него: {(distance + 2000) / 1000:.1f} км.\n"
                        f"Желаете заказать в нем или выбрать другой филиал?"
                        for shop_name, distance, url, shop_location in closest_shops])

    await message.answer(f"Спасибо. \n"
                         f"{text}", disable_web_page_preview=True, reply_markup=yes_no)

    for shop_name, distance, url, shop_location in closest_shops:
        await message.answer_location(latitude=shop_location["lat"],
                                      longitude=shop_location["lon"])

        await state.update_data(branch=shop_name)

    await Order.location_drive_another.set()

# Назад в подтверждении адреса доставки
@dp.message_handler(Text(equals=[lang_en.back_eng]), state=Order.location_drive_another)
async def ask_delivery(message: types.Message):
    await message.answer("Вам нужна доставка или самовывоз?", reply_markup=d_or_d)
    await Order.asklocation.set()


# Адрес для самовывоза подтвержден, начало заказа
@rate_limit(2, key="drive")
@dp.message_handler(Text(equals=[lang_en.save_eng]), state=Order.location_drive_another)
async def confirm_drive(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(f'Вы выбрали филиал: {data["branch"]}')
        id = message.from_user.id
        lang = await quick_commands.select_language(id)
        cats = await quick_commands.get_categories(lang)
        cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(*[KeyboardButton(text=cat) for cat in cats])
        await message.answer("Начнем заказ?", reply_markup=cat_lan)
        location_delivery = data["location"]
        shop_name = data["branch"]
        await quick_commands.update_last_order_type(id, 2)
        await quick_commands.update_last_order_coords(id, location_delivery.latitude, location_delivery.longitude)
        await quick_commands.update_last_branch(id, shop_name)

        await Order.menu.set()


# Выбор другого филиала для самовывоза
@rate_limit(2, key="drive_a")
@dp.message_handler(Text(equals=[lang_en.choose_another_eng]), state=Order.location_drive_another)
async def change_drive(message: types.Message):
    branches_list = []
    for branch in await quick_commands.select_all_branches_list():
        branches_list.append([branch])
    branches = ReplyKeyboardMarkup(branches_list, resize_keyboard=True)
    await message.answer("Выберите филиал из списка ниже:", reply_markup=branches)
    await Order.location_drive_another.set()


# Выбор другого филиала.
@rate_limit(2, key="drive_a")
@dp.message_handler(state=Order.location_drive_another)
async def confirm_drive_again(message: types.Message, state: FSMContext):
    list = await quick_commands.select_all_branches_list()
    if message.text in list:


        await state.update_data(branch=message.text)
        await message.answer(f"Выбран филиал: {message.text}\nЖелаете заказать в нем или выбрать другой филиал?", reply_markup=yes_no)

        await Order.location_drive_another.set()
    else:
        await message.answer("Неверный филиал. Попробуйте еще раз.")

@rate_limit(1, key="delivery")
@dp.message_handler(Text(equals=[lang_en.back_eng]), state=Order.asklocation)
async def back_delivery(message: types.Message, state: FSMContext):
    await message.answer(f'Приступим к оформлению?', reply_markup=main_menu)
    await state.finish()


