
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import location, d_or_d, yes_no, main_menu, delivery_yes_no, languages, old_d_or_d
from loader import dp



@dp.message_handler()
async def bot_echo(message: types.Message, state: FSMContext):
    text = "Неизвестная команда\nНажмите /start для перезапуска"
    await message.answer(text, reply_markup=main_menu)
    await state.finish()


