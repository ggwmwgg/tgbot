
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import dp



@dp.message_handler()
async def bot_echo(message: types.Message, state: FSMContext):
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


