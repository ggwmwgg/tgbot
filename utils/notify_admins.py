import logging

from aiogram import Dispatcher

# from data.config import admins
from utils.db_api import quick_commands


async def on_startup_notify(dp: Dispatcher):
    admins = await quick_commands.get_admins()
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен и готов к работе")

        except Exception as err:
            logging.exception(err)


