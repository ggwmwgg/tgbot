from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text, Command
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import re
from loader import dp
from states.orders import Reg, Settings
from utils.db_api import quick_commands
import os
from dotenv import load_dotenv
from twilio.rest import Client
from random import randint
from utils.misc import rate_limit


# Настройки
@rate_limit(1, key="settings")
@dp.message_handler(Command("settings"), state=None)
@dp.message_handler(Text(equals=["Настройки 🛠", "Settings 🛠", "Sozlamalar 🛠"]), state=None)
async def settings_select(message: types.Message, state: FSMContext):
    id = message.from_user.id
    text = "<b>Настройки</b>\n\nИмя: %s\nЯзык: %s\nНомер: %s\nКоличество заказов: %s\nКешбек: %s\nДата регистрации: %s\n\n"
    if await quick_commands.select_user(id):
        user = await quick_commands.select_user(id)
        lang = ""
        if user.lang_user == 'ru':
            lang = 'Русский 🇷🇺'
        elif user.lang_user == 'en':
            lang = 'English 🇺🇸'
        elif user.lang_user == 'uz':
            lang = "O'zbek 🇺🇿"
        date_reg = user.created_at.strftime("%d.%m.%Y %H:%M")
        text = text % (user.name, lang, user.number, user.orders_no, user.cashback, date_reg)
        edit = "<i>Что Вы бы хотели изменить?</i>"
        txt = text + edit
        lil = await dp.bot.send_message(id, "Загрузка", reply_markup=ReplyKeyboardRemove())
        await lil.delete()

        settings = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
        settings.row(types.InlineKeyboardButton("Имя 📝", callback_data='name'),
                     types.InlineKeyboardButton("Номер 📱", callback_data='number'),
                     types.InlineKeyboardButton("Язык 💬", callback_data='lang'))
        settings.add(types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        await message.answer(txt, reply_markup=settings, parse_mode='HTML')
        await Settings.settings.set()
    else:

        languages = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="O'zbek 🇺🇿"),
                ],
                [
                    KeyboardButton(text="Русский 🇷🇺")
                ],
                [
                    KeyboardButton(text="English 🇺🇸")
                ]
            ],
            resize_keyboard=True
        )

        await message.answer(f"Здравствуйте, {message.from_user.full_name}!\n"
                             "Выберите язык обслуживания.🗣\n\n"
                             f"Hello, {message.from_user.full_name}!\n"
                             "Please, choose your language.🗣\n\n"
                             f"Keling, {message.from_user.full_name}!\n"
                             "Avvaliga xizmat ko'rsatish tilini tanlab olaylik.🗣", reply_markup=languages)

        await Reg.language.set()


@rate_limit(1, key="settings_main")
@dp.callback_query_handler(state=Settings.settings)
async def settings_main(query: types.CallbackQuery, state: FSMContext):
    user = await quick_commands.select_user(query.from_user.id)
    await query.message.delete()
    if query.data == "name":
        text = "<b>Изменение имени</b>\n\nВаше предыдущее имя: %s\n\n<i>Введите новое Имя</i>"
        text = text % user.name
        #await query.message.edit_reply_markup(reply_markup=None)
        # await query.message.edit_text(text, parse_mode='HTML', reply_markup=None)
        await dp.bot.send_message(query.from_user.id, text, parse_mode='HTML', reply_markup=None)
        await Settings.name.set()
    elif query.data == "lang":
        text = ""
        if user.lang_user == 'ru':
            text = "<b>Изменение языка</b>\n\nВаш текущий язык: Русский\n\n<i>Выберите новый язык:</i>"
        elif user.lang_user == 'en':
            text = "<b>Change language</b>\n\nYour current language: English\n\n<i>Choose a new language:</i>"
        elif user.lang_user == 'uz':
            text = "<b>Til o'zgarishi</b>\n\nJoriy tilingiz: oʻzbek\n\n<i>Yangi tilni tanlang:</i>"

        lang_set = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        lang_set.add(types.InlineKeyboardButton("Русский 🇷🇺", callback_data='ru'),
                     types.InlineKeyboardButton("English 🇺🇸", callback_data='en'),
                     types.InlineKeyboardButton("O'zbek 🇺🇿", callback_data='uz'))
        lang_set.add(types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        await dp.bot.send_message(query.from_user.id, text, parse_mode='HTML', reply_markup=lang_set)

        await Settings.language.set()
    elif query.data == "number":
        text = "<b>Изменение номера</b>\n\nВаш текущий номер: %s\n\n<i>Отправьте ваш номер или введите его в формате +998911234567</i>"
        text = text % user.number

        nmbr_s = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Отправить номер телефона 📲", request_contact=True)
                ],
                [
                    KeyboardButton(text="Назад 🔙"),
                ]
            ],
            resize_keyboard=True
        )

        await dp.bot.send_message(query.from_user.id, text, parse_mode='HTML', reply_markup=nmbr_s)
        await Settings.number.set()
    elif query.data == "back":
        text = "С чего начнем?"
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

        await dp.bot.send_message(query.from_user.id, text, parse_mode='HTML', reply_markup=main_menu)
        await state.finish()



# Проверка валидности нового номера и отправка смс
@rate_limit(2, key="nn")
@dp.message_handler(state=Settings.number, content_types=["text", "contact"])
async def num_nn(message: types.Message, state: FSMContext):
    number = ""
    if message.text == "Back 🔙" or message.text == "Назад 🔙" or message.text == "Orqaga 🔙":

        settings = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
        settings.row(types.InlineKeyboardButton("Имя 📝", callback_data='name'),
                     types.InlineKeyboardButton("Номер 📱", callback_data='number'),
                     types.InlineKeyboardButton("Язык 💬", callback_data='lang'))
        settings.add(types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        await message.answer("Настройки 🛠", reply_markup=settings)
        await Settings.settings.set()
    if message.text:
        number = message.text
    elif message.contact.phone_number:
        number_i = message.contact.phone_number
        number = "+" + number_i


    # await message.answer(f"{number}")
    pattern = '(^\+998[8-9])\d{8}$'
    result = re.match(pattern, number)

    if result:
        if await quick_commands.check_number(number):
            await message.answer("Данный номер уже зарегистрирован\n\nВведите другой номер")
        else:

            load_dotenv()
            verification_code = str(randint(100000, 999999))
            account = str(os.getenv("account_twilio"))
            token = str(os.getenv("token_twilio"))
            client = Client(account, token)

            # messages = client.messages.create(to=f"{number}", from_="+14632231765",
            #                                  body=f"GGsellbot: {verification_code}")

            await message.answer(f"На ваш номер был отправлен код, пожалуйста введите его ниже. {verification_code}",
                                 reply_markup=ReplyKeyboardRemove())
            await state.update_data(verification_code=verification_code)
            await Settings.number_code.set()
    else:
        await message.answer(f"Неправильный формат.\n"
                             f"Пожалуйста, отправьте ваш номер или введите его в формате +998911234567")


# Проверка кода
@rate_limit(2, key="code")
@dp.message_handler(state=Settings.number_code, content_types=["text"])
async def verification_code_check(message: types.Message, state: FSMContext):
    id = message.from_user.id
    user = await quick_commands.select_user(id)
    lang = ""
    user_entry = message.text
    async with state.proxy() as data:
        verification_code = data["verification_code"]
        result = re.match(user_entry, verification_code)
        if result:
            num = data["number"]
            await quick_commands.update_user_number(id=message.from_user.id, number=num)
            text = "<b>Настройки</b>\n\nИмя: %s\nЯзык: %s\nНомер: %s\nКоличество заказов: %s\nКешбек: %s\nДата регистрации: %s\n\n"
            if user.lang_user == 'ru':
                lang = 'Русский'
            elif user.lang_user == 'en':
                lang = 'English'
            elif user.lang_user == 'uz':
                lang = "O'zbek"
            date_reg = user.created_at.strftime("%d.%m.%Y %H:%M")
            text = text % (user.name, lang, user.number, user.orders_no, user.cashback, date_reg)
            edit = "<i>Ваш номер успешно изменен на <b>%s</b></i>" % num
            txt = text + edit
            lil = await dp.bot.send_message(id, "Загрузка...", reply_markup=ReplyKeyboardRemove())
            await lil.delete()

            settings = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
            settings.row(types.InlineKeyboardButton("Имя 📝", callback_data='name'),
                         types.InlineKeyboardButton("Номер 📱", callback_data='number'),
                         types.InlineKeyboardButton("Язык 💬", callback_data='lang'))
            settings.add(types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

            await dp.bot.send_message(id, txt, reply_markup=settings, parse_mode='HTML')
            await Settings.settings.set()
        else:
            await message.answer(f"Неверный код.\n"
                                 f"Пожалуйста, введите его заново.")

# Изменение имени
@rate_limit(1, key="name")
@dp.message_handler(state=Settings.name)
async def name_confirm(message: types.Message, state: FSMContext):
    id = message.from_user.id
    name = message.text
    await quick_commands.update_user_name(id=message.from_user.id, name=name)
    user = await quick_commands.select_user(id)
    lang = ""
    text = "<b>Настройки</b>\n\nИмя: %s\nЯзык: %s\nНомер: %s\nКоличество заказов: %s\nКешбек: %s\nДата регистрации: %s\n\n"
    if user.lang_user == 'ru':
        lang = 'Русский'
    elif user.lang_user == 'en':
        lang = 'English'
    elif user.lang_user == 'uz':
        lang = "O'zbek"
    date_reg = user.created_at.strftime("%d.%m.%Y %H:%M")
    text = text % (user.name, lang, user.number, user.orders_no, user.cashback, date_reg)
    edit = "<i>Ваше имя успешно изменено на <b>%s</b></i>" % name
    txt = text + edit
    lil = await dp.bot.send_message(id, "Загрузка...", reply_markup=ReplyKeyboardRemove())
    await lil.delete()

    settings = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
    settings.row(types.InlineKeyboardButton("Имя 📝", callback_data='name'),
                 types.InlineKeyboardButton("Номер 📱", callback_data='number'),
                 types.InlineKeyboardButton("Язык 💬", callback_data='lang'))
    settings.add(types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

    await dp.bot.send_message(id, txt, reply_markup=settings, parse_mode='HTML')
    await Settings.settings.set()


# Изменение языка
@rate_limit(1, key="lang")
@dp.callback_query_handler(state=Settings.language)
async def lang_confirm(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=None)
    id = query.from_user.id
    lang_c = query.data
    user = await quick_commands.select_user(id)
    lang = ""
    text = "<b>Настройки</b>\n\nИмя: %s\nЯзык: %s\nНомер: %s\nКоличество заказов: %s\nКешбек: %s\nДата регистрации: %s\n\n"
    date_reg = user.created_at.strftime("%d.%m.%Y %H:%M")
    if lang_c == "ru":
        await quick_commands.update_user_language(id, lang_c)
        lang = 'Русский'
        text = text % (user.name, lang, user.number, user.orders_no, user.cashback, date_reg)
        edit = "<i>Язык успешно изменен на %s</i>" % lang
        txt = text + edit
        lil = await dp.bot.send_message(id, "Загрузка...", reply_markup=ReplyKeyboardRemove())
        await lil.delete()

        settings = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
        settings.row(types.InlineKeyboardButton("Имя 📝", callback_data='name'),
                     types.InlineKeyboardButton("Номер 📱", callback_data='number'),
                     types.InlineKeyboardButton("Язык 💬", callback_data='lang'))
        settings.add(types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        await dp.bot.send_message(id, txt, reply_markup=settings, parse_mode='HTML')
        await Settings.settings.set()
    elif lang_c == "en":
        await quick_commands.update_user_language(id, lang_c)
        lang = 'English'
        text = text % (user.name, lang, user.number, user.orders_no, user.cashback, date_reg)
        edit = "<i>Language successfully changed to %s</i>" % lang
        txt = text + edit
        lil = await dp.bot.send_message(id, "Загрузка...", reply_markup=ReplyKeyboardRemove())
        await lil.delete()

        settings = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
        settings.row(types.InlineKeyboardButton("Имя 📝", callback_data='name'),
                     types.InlineKeyboardButton("Номер 📱", callback_data='number'),
                     types.InlineKeyboardButton("Язык 💬", callback_data='lang'))
        settings.add(types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        await dp.bot.send_message(id, txt, reply_markup=settings, parse_mode='HTML')
        await Settings.settings.set()
    elif lang_c == "uz":
        await quick_commands.update_user_language(id, lang_c)
        lang = "O'zbek"
        text = text % (user.name, lang, user.number, user.orders_no, user.cashback, date_reg)
        edit = "<i>Til muvaffaqiyatli %s ga o'zgartirildi</i>" % lang
        txt = text + edit
        lil = await dp.bot.send_message(id, "Загрузка...", reply_markup=ReplyKeyboardRemove())
        await lil.delete()

        settings = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
        settings.row(types.InlineKeyboardButton("Имя 📝", callback_data='name'),
                     types.InlineKeyboardButton("Номер 📱", callback_data='number'),
                     types.InlineKeyboardButton("Язык 💬", callback_data='lang'))
        settings.add(types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        await dp.bot.send_message(id, txt, reply_markup=settings, parse_mode='HTML')
        await Settings.settings.set()
    elif lang_c == "back":
        if user.lang_user == 'ru':
            lang = 'Русский'
        elif user.lang_user == 'en':
            lang = 'English'
        elif user.lang_user == 'uz':
            lang = "O'zbek"
        text = text % (user.name, lang, user.number, user.orders_no, user.cashback, date_reg)
        edit = "<i>Что Вы бы хотели изменить?</i>"
        txt = text + edit
        lil = await dp.bot.send_message(id, "Загрузка", reply_markup=ReplyKeyboardRemove())
        await lil.delete()

        settings = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
        settings.row(types.InlineKeyboardButton("Имя 📝", callback_data='name'),
                     types.InlineKeyboardButton("Номер 📱", callback_data='number'),
                     types.InlineKeyboardButton("Язык 💬", callback_data='lang'))
        settings.add(types.InlineKeyboardButton("Назад 🔙", callback_data='back'))

        await dp.bot.send_message(id, txt, reply_markup=settings, parse_mode='HTML')
        await Settings.settings.set()
