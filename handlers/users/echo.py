import gettext

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from utils.db_api import quick_commands


@dp.message_handler()
async def bot_echo(message: types.Message, state: FSMContext):
    if await quick_commands.select_user(id=message.from_user.id):
        lang = await quick_commands.select_language(message.from_user.id)
        lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
        lan.install()
        _ = lan.gettext
        text = _("Неизвестная команда\nНажмите /start для перезапуска")

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

        await message.answer(text, reply_markup=main_menu)
        await state.finish()
    else:
        text = "Неизвестная команда\nНажмите /start для перезапуска"

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

        await message.answer(text, reply_markup=main_menu)
        await state.finish()


