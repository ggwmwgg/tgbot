from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text, Command
from aiogram.types import ReplyKeyboardRemove
import re

from keyboards.default import location, d_or_d, nmbr, nmbr_s, yes_no, main_menu, delivery_yes_no, languages, settings
from loader import dp
from states.orders import Order, Reg, Settings
from utils.db_api import quick_commands
import os
from dotenv import load_dotenv
from twilio.rest import Client
from random import randint
from utils.db_api.models import User
from data import lang_en
from utils.misc import rate_limit, get_address_from_coords


# import re


# Доставка или самовывоз?
@rate_limit(1, key="settings")
@dp.message_handler(Command("settings"), state=None)
@dp.message_handler(Text(equals=["Настройки"]), state=None)
async def settings_select(message: types.Message, state: FSMContext):
    if await quick_commands.select_user(id=message.from_user.id):
        await message.answer("Выберите опцию", reply_markup=settings)
        await Settings.settings.set()
    else:
        await message.answer(f"Здравствуйте, {message.from_user.full_name}!\n"
                             "Выберите язык обслуживания.\n\n"
                             f"Hello, {message.from_user.full_name}!\n"
                             "Please, choose your language\n\n"
                             f"Keling, {message.from_user.full_name}!\n"
                             "Avvaliga xizmat ko'rsatish tilini tanlab olaylik", reply_markup=languages)

        await Reg.language.set()


# Кнопка назад в настройках
@rate_limit(1, key="settings_main")
@dp.message_handler(Text(equals=["Назад"]), state=Settings.settings)
async def back_nz(message: types.Message, state: FSMContext):
    await message.answer(f'Приступим к оформлению?', reply_markup=main_menu)
    await state.finish()

# Кнопка изменить номер в настройках
@rate_limit(1, key="number")
@dp.message_handler(Text(equals=["Изменить номер телефона"]), state=Settings.settings)
async def back_nz(message: types.Message, state: FSMContext):
    numm = await quick_commands.select_number(id=message.from_user.id)

    await message.answer(f"Ваш текущий номер {numm}\n"
                         f"Отправьте ваш номер или введите его в формате +998911234567", reply_markup=nmbr_s)
    await Settings.number.set()

# Проверка валидности нового номера и отправка смс
@rate_limit(2, key="nn")
@dp.message_handler(state=Settings.number, content_types=["text", "contact"])
async def num_nn(message: types.Message, state: FSMContext):

    if message.text == "Назад":
        await message.answer("Выберите опцию", reply_markup=settings)
        await Settings.settings.set()
    else:
        number = ""
        if message.text:
            number = message.text
        elif message.contact.phone_number:
            number_i = message.contact.phone_number
            number = "+" + number_i


        # await message.answer(f"{number}")
        pattern = '(^\+998[8-9])\d{8}$'
        result = re.match(pattern, number)

        if result:
            await state.update_data(number=number)

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
    user_entry = message.text
    async with state.proxy() as data:
        verification_code = data["verification_code"]
        result = re.match(user_entry, verification_code)
        if result:
            num = data["number"]
            await quick_commands.update_user_number(id=message.from_user.id, number=num)
            await message.answer(f'Номер успешно изменен на {num}', reply_markup=settings)
            await Settings.settings.set()
        else:
            await message.answer(f"Неверный код.\n"
                                 f"Пожалуйста, введите его заново.")

# Кнопка изменить язык в настройках
@rate_limit(1, key="language")
@dp.message_handler(Text(equals=["Изменить язык"]), state=Settings.settings)
async def back_nz(message: types.Message, state: FSMContext):
    lang_kek = await quick_commands.select_language(id=message.from_user.id)
    kok = "1"
    if lang_kek == "ru":
        kok = "Русский"
    elif lang_kek == "uz":
        kok = "O'zbek"
    else:
        kok = "English"

    await message.answer(f"Выбранный Вами язык ранее: {kok}\n"
                         "Выберите язык обслуживания.\n\n"
                         f"Hello, {message.from_user.full_name}!\n"
                         "Please, choose your language\n\n"
                         f"Keling, {message.from_user.full_name}!\n"
                         "Avvaliga xizmat ko'rsatish tilini tanlab olaylik", reply_markup=languages)
    await Settings.language.set()

# Изменение языка
@rate_limit(2, key="language")
@dp.message_handler(Text(equals=["O'zbek", "Русский", "English"]), state=Settings.language)
async def language_change_c(message: types.Message, state: FSMContext):
    language = message.text
    id = message.from_user.id
    if language == "Русский":
        await quick_commands.update_user_language(id=id, lang_user="ru")
        await message.answer(f"Ваш язык изменен на: Русский", reply_markup=settings)
        await Settings.settings.set()
    elif language == "O'zbek":
        await quick_commands.update_user_language(id=id, lang_user="uz")
        await message.answer(f"Sizning tilingiz: O'zbek", reply_markup=settings)
        await Settings.settings.set()
    else:
        await quick_commands.update_user_language(id=id, lang_user="en")
        await message.answer(f"Your language is changed to: English", reply_markup=settings)
        await Settings.settings.set()

# Кнопка изменить имя
@rate_limit(1, key="name")
@dp.message_handler(Text(equals=["Изменить имя"]), state=Settings.settings)
async def name_change(message: types.Message, state: FSMContext):
    name = await quick_commands.select_name(id=message.from_user.id)
    await message.answer(f"Ваше предыдущее имя: {name}\n"
                         f"Введите новое Имя", reply_markup=ReplyKeyboardRemove())
    await Settings.name.set()

# Изменение имени
@rate_limit(1, key="name")
@dp.message_handler(state=Settings.name)
async def name_confirm(message: types.Message, state: FSMContext):
    name = message.text
    await quick_commands.update_user_name(id=message.from_user.id, name=name)
    await message.answer(f"Ваше имя успешно изменено на {name}", reply_markup=settings)
    await Settings.settings.set()

