from aiogram import executor

import middlewares, filters, handlers
from loader import dp
from loader import db
from utils.db_api import db_gino
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

async def on_startup(dp):
    # Уведомляет про запуск
    print("Подключаем БД")
    await db_gino.on_startup(dp)

    # print("Чистим базу")
    # await db.gino.drop_all()

    print("Создаем таблицы")
    await db.gino.create_all()

    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
