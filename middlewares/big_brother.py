import logging

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api import quick_commands
from aiogram import Dispatcher
from loader import dp
from data.config import banned_users


# Message/Updates processing middleware example
class BigBrother(BaseMiddleware):
    # 1
    async def on_pre_process_update(self, update: types.Update, data: dict):
        # logging.info("[----------------------Новый апдейт!----------------------]")
        # logging.info("1. Pre Process Update")
        # logging.info("Следующая точка: Process Update")
        data["middleware_data"] = "Это пройдет до on_post_process_update"
        if update.message:
            user = update.message.from_user.id
            # print(update.message.text)
        elif update.callback_query:
            user = update.callback_query.from_user.id
            # print(update.callback_query)
        else:
            return

        try:
            ban = await quick_commands.check_ban(user)
        except Exception as e:
            ban = False
        if ban:
            await dp.bot.send_message(user, "Вы забанены")
            raise CancelHandler()

    # 2
    async def on_process_update(self, update: types.Update, data: dict):
        pass
        # logging.info(f"2. Process Update, {data=}")
        # logging.info("Следующая точка: Pre Process Message")

    # 3
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # logging.info(f"3. Pre Process Message, {data=}")
        # logging.info("Следующая точка: Filters, Process Message")
        data["middleware_data"] = "Это пройдет в on_process_message"


    # 4 Filters

    # 5
    async def on_process_message(self, message: types.Message, data: dict):
        # logging.info(f"5. Process Message")
        # logging.info("Следующая точка: Handler")
        data["middleware_data"] = "Это попадет в хендлер"


    # 6 Handler

    # 7
    async def on_post_process_message(self, message: types.Message, data_from_handler: list, data: dict):
        pass
        # logging.info(f"7. Post Process Message, {data=}, {data_from_handler=}")
        # logging.info("Следующая точка: Post Process Update")

    # 8
    async def on_post_process_update(self, update: types.Update, data_from_handler: list, data: dict):
        pass
        # logging.info(f"8. Post Process Update, {data=}, {data_from_handler=}")
        # logging.info(f"[----------------------Выход------------------------------]\n")

    async def on_pre_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        await cq.answer()
