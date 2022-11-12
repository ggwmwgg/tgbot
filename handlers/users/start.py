import os
import re
# from utils.db_api.models import User
from datetime import datetime
from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.types import ReplyKeyboardRemove
from dotenv import load_dotenv
from twilio.rest import Client

from keyboards.default import languages, nmbr, main_menu
from loader import dp
from states.orders import Reg
from utils.db_api import quick_commands
from utils.misc import rate_limit


@rate_limit(5, key="start")
@dp.message_handler(CommandStart(), state='*') #  state=None
async def bot_start(message: types.Message):

    await message.answer(f"Здравствуйте, {message.from_user.full_name}!\n"
                         "Выберите язык обслуживания.\n\n"
                         f"Hello, {message.from_user.full_name}!\n"
                         "Please, choose your language\n\n"
                         f"Keling, {message.from_user.full_name}!\n"
                         "Avvaliga xizmat ko'rsatish tilini tanlab olaylik", reply_markup=languages)

    await Reg.language.set()


@rate_limit(2, key="language")
@dp.message_handler(Text(equals=["O'zbek", "Русский", "English"]), state=Reg.language)
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
    if language == "Русский":
        await message.answer(f"Ваш язык: Русский", reply_markup=ReplyKeyboardRemove())
        await state.update_data(language='ru')
        await message.answer(f"Как к вам обращаться?")
        await Reg.next()
    elif language == "O'zbek":
        await message.answer(f"Sizning tilingiz: O'zbek", reply_markup=ReplyKeyboardRemove())
        await state.update_data(language='uz')
        await message.answer(f"Sizga qanday nom berishim kerak?")
        await Reg.next()
    elif language == "English":
        await message.answer(f"Your language set to: English", reply_markup=ReplyKeyboardRemove())
        await state.update_data(language='en')
        await message.answer(f"What is your name?")
        await Reg.next()
    else:
        await message.answer(f"Error")


@rate_limit(2, key="name")
@dp.message_handler(state=Reg.name)
async def name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(f"Отправьте ваш номер или введите его в формате +998911234567", reply_markup=nmbr)
    await Reg.next()


@rate_limit(2, key="nn")
@dp.message_handler(state=Reg.nn, content_types=["text", "contact"])
async def nn(message: types.Message, state: FSMContext):
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
        await Reg.next()
    else:
        await message.answer(f"Неправильный формат.\n"
                             f"Пожалуйста, отправьте ваш номер или введите его в формате +998911234567")


@rate_limit(2, key="code")
@dp.message_handler(state=Reg.code)
async def verification(message: types.Message, state: FSMContext):
    user_entry = message.text
    time_now = datetime.now()
    date = time_now.strftime("%d.%m.%Y %H:%M")
    orders_no = 0
    async with state.proxy() as data:
        verification_code = data["verification_code"]
        result = re.match(user_entry, verification_code)
        if result:
            await message.answer(f'Здравствуйте, {data["name"]}!\n'
                                 f'Вы успешно зарегистрировались!\n'
                                 f'Ваш язык: {data["language"]}\n'
                                 f'Ваш номер: {data["number"]}\n'
                                 f'Ваш id: {data["user_id"]}\n'
                                 f'Ваш chat_id: {data["chat_id"]}\n'
                                 f'Ваш username: {data["username"]}')

            await quick_commands.add_user(id=message.from_user.id, name=data["name"], lang_user=data["language"],
                                          number=data["number"], username=data["username"],
                                          referral=message.from_user.id)
            await message.answer(f'Приступим к оформлению?', reply_markup=main_menu)
            await state.finish()
        else:
            await message.answer(f"Неверный код.\n"
                                 f"Пожалуйста, введите его заново.")
    # await state.finish()


# Настройки
