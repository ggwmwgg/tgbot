import gettext
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers.users.cart import show_cart
from handlers.users.create_order import start_order
from loader import dp
from states.orders import Order
from utils.db_api import quick_commands
from utils.misc import rate_limit
import datetime


# Меню (напитки, боксы итд) + возврат к выбору доставки или самовывоза

@rate_limit(1, key="menu")
@dp.message_handler(state=Order.menu)
async def menu_cat(message: types.Message, state: FSMContext):
    id = message.from_user.id
    lang = await quick_commands.select_language(id)
    lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
    lan.install()
    _ = lan.gettext
    back = ["Назад 🔙", "Orqaga 🔙", "Back 🔙"]
    cart = ["Корзина 🛒", "Savat 🛒", "Cart 🛒"]
    order_make = ["Оформить заказ 🚚", "Buyurtma berish 🚚", "Make an order 🚚"]
    cats_list = await quick_commands.get_only_categories(lang)
    list_cat = await quick_commands.get_categories(lang)
    if message.text in list_cat:
        if message.text in back:

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

            await message.answer('Приступим к оформлению?', reply_markup=main_menu)
            await state.finish()
        elif message.text in cart:
            #await Order.cart.set()
            await show_cart(message)
        elif message.text == order_make[0] or message.text == order_make[1] or message.text == order_make[2]:
            # Проверка по времени
            FROM_TIME = str(os.getenv("from_t"))
            TO_TIME = str(os.getenv("to_t"))
            NOW = datetime.datetime.now().strftime("%H")
            t_now = datetime.datetime.strptime(NOW, "%H")
            from_t = datetime.datetime.strptime(FROM_TIME, "%H")
            to_t = datetime.datetime.strptime(TO_TIME, "%H")

            if from_t <= t_now <= to_t:
                await start_order(message, state)
            else:
                text = "Заказы принимаются с <b>%s:00</b> до <b>%s:00</b>"
                text = text % (FROM_TIME, TO_TIME)
                dp.bot.send_message(message.from_user.id, text, parse_mode="HTML")
            # await start_order(message, state)
            await Order.menu_confirm.set()
        elif message.text in cats_list:
            category = message.text
            cats = await quick_commands.get_subcategories(category, lang)
            # print(cats)
            cats_l = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
                *[KeyboardButton(text=cat) for cat in cats])
            text = "Выбрана категория: %s" % message.text
            await message.answer(text, reply_markup=cats_l)
            await state.update_data(category=category)
            await Order.menu_subcat.set()
    else:
        id = message.from_user.id
        lang = await quick_commands.select_language(id)
        cats = await quick_commands.get_categories(lang)
        cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
            *[KeyboardButton(text=cat) for cat in cats])
        await message.answer("Такой категории не существует", reply_markup=cat_lan)
        await Order.menu.set()


# Список товаров в категории (кока-кола, спрайт и тд)
@rate_limit(1, key="submenu")
@dp.message_handler(state=Order.menu_subcat)
async def menu_sub_cat(message: types.Message, state: FSMContext):
    id = message.from_user.id
    lang = await quick_commands.select_language(id)
    lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
    lan.install()
    _ = lan.gettext
    back = ["Назад 🔙", "Orqaga 🔙", "Back 🔙"]
    cart = ["Корзина 🛒", "Savat 🛒", "Cart 🛒"]
    order_make = ["Оформить заказ 🚚", "Buyurtma berish 🚚", "Make an order 🚚"]
    category = ""
    # await state.update_data(items={})
    async with state.proxy() as data:
        category = data["category"]
        cats_list = await quick_commands.get_only_subcategories(category, lang)
        list_cat = await quick_commands.get_subcategories(category, lang)
        if message.text in list_cat:  # Если выбрана категория, корзина, оформление заказа или кнопка назад
            if message.text == back[0] or message.text == back[1] or message.text == back[2]:
                cats = await quick_commands.get_categories(lang)
                cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
                    *[KeyboardButton(text=cat) for cat in cats])
                await message.answer("Назад 🔙", reply_markup=cat_lan)
                await Order.menu.set()
            elif message.text in cart:
                # await Order.cart.set()
                await show_cart(message)
            elif message.text == order_make[0] or message.text == order_make[1] or message.text == order_make[2]:
                await start_order(message, state)
                #await message.answer("Оформление заказа")
                await Order.menu_confirm.set()
            elif message.text in cats_list:

                item_name = message.text

                item = await quick_commands.get_item_by_name(item_name, lang)
                name_select_lang = ""
                desc_select_lang = ""
                if lang == "ru":
                    name_select_lang = item.name_ru
                    desc_select_lang = item.d_ru
                elif lang == "uz":
                    name_select_lang = item.name_uz
                    desc_select_lang = item.d_uz
                elif lang == "en":
                    name_select_lang = item.name_en
                    desc_select_lang = item.d_en

                photo_n = item.photo
                price = item.price
                # caption = "<b>" + name_select_lang + "\n\n</b>" + "<i>" + desc_select_lang + "\n\n\n</i>" + str(price) + " сум\n\n" + "<b>Выберите количество</b>"
                caption = "<b>%s\n\n</b><i>%s\n\n\n</i>%s сум\n\n<b>Выберите количество:</b>" % (name_select_lang, desc_select_lang, str(price))

                quantity = ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text="1"),
                            KeyboardButton(text="2"),
                            KeyboardButton(text="3"),
                        ],
                        [
                            KeyboardButton(text="4"),
                            KeyboardButton(text="5"),
                            KeyboardButton(text="6"),
                        ],
                        [
                            KeyboardButton(text="7"),
                            KeyboardButton(text="8"),
                            KeyboardButton(text="9"),
                        ],
                        [
                            KeyboardButton(text="Корзина 🛒"),
                            KeyboardButton(text="Назад 🔙")
                        ]
                    ],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )

                await dp.bot.send_photo(chat_id=id, photo=open(photo_n, "rb"), caption=caption, parse_mode="HTML",
                                        reply_markup=quantity)  # reply_markup=cats
                await state.update_data(item_id=item.id)
                await Order.menu_item.set()
        else:
            cats = await quick_commands.get_categories(lang)
            cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
                *[KeyboardButton(text=cat) for cat in cats])
            await message.answer("Такой категории не существует", reply_markup=cat_lan)
            await Order.menu.set()


# Выбор количества товара и добавление его в бд
@rate_limit(1, key="item_s_menu")
@dp.message_handler(state=Order.menu_item)
async def menu_item(message: types.Message, state: FSMContext):
    id = message.from_user.id
    lang = await quick_commands.select_language(id)
    lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
    lan.install()
    _ = lan.gettext
    back = ["Назад 🔙", "Orqaga 🔙", "Back 🔙"]
    cart = ["Корзина 🛒", "Savat 🛒", "Cart 🛒"]

    # await state.update_data(items={})
    async with state.proxy() as data:
        category = data["category"]
        item_id = data["item_id"]


        if message.text.isdigit():
            # Добавление товара через бд
            cats = await quick_commands.get_categories(lang)
            price_one = await quick_commands.select_item_price(item_id)
            # amount = message.text
            amount = message.text
            amount = int(amount)
            price = amount * price_one
            await quick_commands.add_or_update_cart(user_id=id,item_id=item_id, quantity=amount, price=price)
            cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
                *[KeyboardButton(text=cat) for cat in cats])
            await message.answer("Товар добавлен в корзину, продолжим?", reply_markup=cat_lan)
            await Order.menu.set()
        elif message.text in cart:
            #await Order.cart.set()
            await show_cart(message)


        elif message.text == back[0] or message.text == back[1] or message.text == back[2]:
            cats = await quick_commands.get_subcategories(category, lang)
            cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
                *[KeyboardButton(text=cat) for cat in cats])
            await message.answer("Назад 🔙", reply_markup=cat_lan)
            await Order.menu_subcat.set()
        else:
            await message.answer("Неверный формат,выберите количество товара ниже или введите число вручную")