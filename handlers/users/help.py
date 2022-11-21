import gettext

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.db_api import quick_commands
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    if await quick_commands.select_user(id=message.from_user.id):
        lang = await quick_commands.select_language(id)
        lan = gettext.translation('tgbot', localedir='locales', languages=[lang])
        lan.install()
        _ = lan.gettext
        list_of_commands = _('Список команд: ')
        comm_one = _('/start - Запуск бота')
        comm_two = _('/order - Начать заказ')
        comm_three = _('/help - Помощь')
        text = [list_of_commands, comm_one, comm_two, comm_three]
        await message.answer('\n'.join(text))
    else:
        text = [
            'Список команд: ',
            '/start - Запуск бота',
            '/order - Начать заказ',
            '/help - Помощь'
        ]
        await message.answer('\n'.join(text))
