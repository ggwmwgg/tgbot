
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import main_menu
from loader import dp


# Echo handler example
@dp.message_handler()
async def bot_echo(message: types.Message, state: FSMContext):
    text = "Неизвестная команда\nНажмите /start для перезапуска"
    await message.answer(text, reply_markup=main_menu)
    await state.finish()


