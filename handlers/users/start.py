import gettext

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Text
import re
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from loader import dp
from states.orders import Reg
import os
from dotenv import load_dotenv
from twilio.rest import Client
from random import randint
from datetime import datetime
from utils.misc import rate_limit
from utils.db_api import quick_commands


@rate_limit(5, key="start")
@dp.message_handler(CommandStart(), state='*') #  state=None
async def bot_start(message: types.Message):
    if await quick_commands.select_user(id=message.from_user.id):
        lang = await quick_commands.select_language(message.from_user.id)
        lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
        lan.install()
        _ = lan.gettext
        main_menu = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=_("Начать заказ 🍽")),
                ],
                [
                    KeyboardButton(text=_("Оставить отзыв 📝")),
                    KeyboardButton(text=_("Мои заказы 🛒"))
                ],
                [
                    KeyboardButton(text=_("Контакты 📲")),
                    KeyboardButton(text=_("Настройки 🛠"))
                ]
            ],
            resize_keyboard=True
        )
        await message.answer(_('Приступим к оформлению? 📝'), reply_markup=main_menu)
        # await Order.d_or_d.set()
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


@rate_limit(2, key="language")
@dp.message_handler(Text(equals=["O'zbek 🇺🇿", "Русский 🇷🇺", "English 🇺🇸"]), state=Reg.language)
async def language(message: types.Message, state: FSMContext):
    language = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        username = message.from_user.username
        await state.update_data(username=username)
    except:
        username = "None"
        await state.update_data(username=username)

    await state.update_data(user_id=user_id, chat_id=chat_id)
    if language == "Русский 🇷🇺":
        await message.answer("Ваш язык: Русский", reply_markup=ReplyKeyboardRemove())
        await state.update_data(lang='ru')
        await message.answer("Как к вам обращаться?")
        await Reg.next()
    elif language == "O'zbek 🇺🇿":
        await message.answer("Sizning tilingiz: O'zbek", reply_markup=ReplyKeyboardRemove())
        await state.update_data(lang='uz')
        await message.answer("Sizga qanday nom berishim kerak?")
        await Reg.next()
    elif language == "English 🇺🇸":
        await message.answer("Your language set to: English", reply_markup=ReplyKeyboardRemove())
        await state.update_data(lang='en')
        await message.answer("What is your name?")
        await Reg.next()
    else:
        await message.answer("Ошибка")


@rate_limit(2, key="name")
@dp.message_handler(state=Reg.name)
async def name(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        lang = data['lang']
    lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
    lan.install()
    _ = lan.gettext
    await state.update_data(name=name)
    nmbr = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Отправить номер 📲"), request_contact=True)
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(_("Отправьте ваш номер или введите его в формате +998911234567"), reply_markup=nmbr)
    await Reg.next()


@rate_limit(2, key="nn")
@dp.message_handler(state=Reg.nn, content_types=["text", "contact"])
async def nn(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        lang = data['lang']
    lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
    lan.install()
    _ = lan.gettext

    number = ""

    if message.text:
        number = message.text
    elif message.contact.phone_number:
        number_i = message.contact.phone_number
        number = "+" + number_i
    pattern = '(^\+998[8-9])\d{8}$'
    result = re.match(pattern, number)

    if result:
        if await quick_commands.check_number(number):
            await message.answer(_("Данный номер уже зарегистрирован\n\nВведите другой номер"))
        else:

            load_dotenv()
            verification_code = str(randint(100000, 999999))
            account = str(os.getenv("account_twilio"))
            token = str(os.getenv("token_twilio"))
            client = Client(account, token)

            # messages = client.messages.create(to=f"{number}",from_="+14632231765",body=f"GGsellbot: {verification_code}")
            text = _("На ваш номер был отправлен код, пожалуйста введите его ниже. %s") % verification_code
            await message.answer(text,reply_markup=ReplyKeyboardRemove())
            await state.update_data(verification_code=verification_code)
            await Reg.next()
    else:
        await message.answer(_("Неправильный формат.\nПожалуйста, отправьте ваш номер или введите его в формате "
                             "+998911234567"))


@rate_limit(2, key="code")
@dp.message_handler(state=Reg.code)
async def verification(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        lang = data['lang']
    lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
    lan.install()
    _ = lan.gettext
    user_entry = message.text
    time_now = datetime.now()
    text = _('Уважаемый %s!\nВы успешно зарегистрировались!\nВаш язык: %s\nВаш номер: %s\n')
    date = time_now.strftime("%d.%m.%Y %H:%M")
    orders_no = 0
    async with state.proxy() as data:
        verification_code = data["verification_code"]
        result = re.match(user_entry, verification_code)
        if result:
            text = text % (data["name"], data["lang"], data["number"])
            await message.answer(text)

            await quick_commands.add_user(id=message.from_user.id, name=data["name"], lang_user=data["lang"],
                                          number=data["number"], username=data["username"],
                                          referral=message.from_user.id)
            main_menu = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=_("Начать заказ 🍽")),
                    ],
                    [
                        KeyboardButton(text=_("Оставить отзыв 📝")),
                        KeyboardButton(text=_("Мои заказы 🛒"))
                    ],
                    [
                        KeyboardButton(text=_("Контакты 📲")),
                        KeyboardButton(text=_("Настройки 🛠"))
                    ]
                ],
                resize_keyboard=True
            )
            await message.answer(_('Приступим к оформлению?'), reply_markup=main_menu)
            await state.finish()
        else:
            await message.answer(_("Неверный код.\nПожалуйста, введите его заново."))

