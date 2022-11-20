import asyncio

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup

from data import config
from utils.db_api import quick_commands
from utils.db_api.db_gino import db
from loader import dp, bot
from typing import List
from data import lang_en

from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
# from utils.db_api.schemas.user import User
from utils.db_api.schemas.order import Order
from utils.db_api.schemas.item import Item
from utils.db_api.schemas.cart import Cart
from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.db_api.models import User
from utils.misc import get_address_from_coords
from utils.misc.calc_distance import choose_shortest_kek
from utils.misc.sentinel import allow_access
from keyboards.inline import no_comm, orders_a




# from aiogram.utils.

@allow_access()
async def test():
    await db.set_bind(config.POSTGRES_URI)
    # await db.gino.drop_all()
    # await db.gino.create_all()


    count_users = await quick_commands.count_users()
    print(f"Всего пользователей: {count_users}")

    # Добавление филиалов

    # await quick_commands.add_branch(name="KFC C1", location={"lat":41.311882, "lon":69.290753}, contacts="")
    # await quick_commands.add_branch(name="KFC Chilanzor", location={"lat":41.275180, "lon":69.204455}, contacts="")
    # await quick_commands.add_branch(name="KFC Compass", location={"lat":41.239035, "lon":69.329702}, contacts="")
    # await quick_commands.add_branch(name="KFC Kefayat", location={"lat":41.363426, "lon":69.288095}, contacts="")
    # await quick_commands.add_branch(name="KFC Kokand Drive", location={"lat":40.553458, "lon":70.928854}, contacts="")
    # await quick_commands.add_branch(name="KFC Magic City", location={"lat":41.301427, "lon":69.243220}, contacts="")
    # await quick_commands.add_branch(name="KFC Oazis", location={"lat":41.285794, "lon":69.185997}, contacts="")
    # await quick_commands.add_branch(name="KFC Rossini", location={"lat":41.327371, "lon":69.248053}, contacts="")
    # await quick_commands.add_branch(name="KFC Samarkand Darvoza", location={"lat":41.316420, "lon":69.230976}, contacts="")
    # await quick_commands.add_branch(name="KFC Westminster", location={"lat":41.305353, "lon":69.289093}, contacts="")




    # await dp.bot.edit_message_text(chat_id=id, message_id=5085, text=kokir, parse_mode="HTML", reply_markup=None)
    # await dp.bot.edit_message_reply_markup(chat_id=id, message_id=5081, reply_markup=None)
    # await dp.bot.delete_message(chat_id=id, message_id=5081)

    # back = "Назад"
    # clear = "Очистить"
    # order = "Оформить заказ"
    # cirt = "Корзина"
    # tot = "Итого"
    # pr = "сум"
    #
    #
    # kok = f"<b>{cirt}:\n\n</b>"
    # price_total = 0
    # for item in await quick_commands.select_cart(id):
    #     name = await quick_commands.select_item_name(item.item_id, lang)
    #     price = await quick_commands.select_item_price(item.item_id)
    #     price_total += item.price
    #     kok += f"<b>{name}</b>\n" + f"<b>{item.quantity}</b>" + " x " + f"{price}" + " = " + f"{item.price} сум\n\n"
    #
    # kok += "\n" + f"<b><i>{tot}: </i>" + f"{price_total} {pr}</b>"
    # cats = await quick_commands.get_cart_list(id, lang)
    #
    # inline_kb1 = types.InlineKeyboardMarkup(row_width=1)
    # for a in cats:
    #     b = a[:-2]
    #     inline_kb1.add(types.InlineKeyboardButton(a, callback_data=b))
    # inline_kb1.row(types.InlineKeyboardButton(back, callback_data="back"),
    #                types.InlineKeyboardButton(clear, callback_data="clear"))
    # inline_kb1.row(types.InlineKeyboardButton(order, callback_data="order"))
    #
    #
    #
    # cat_lan = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(
    #     *[KeyboardButton(text=cat) for cat in cats]).row(back, clear).add(KeyboardButton(text=order))
    # # await message.answer(text=kok, parse_mode="HTML", reply_markup=cat_lan)
    # await dp.bot.send_message(chat_id=id, text=kok, parse_mode="HTML", reply_markup=inline_kb1)

    # print("Удаляю пользователя с id 2")
    # await quick_commands.delete_user(2)
    # print("Пользователь удален")

    # print("Чищу корзину")
    # await quick_commands.clear_cart_by_user_id(id)
    # print("Корзина очищена")

    # photo = "../img/bun.png"
    # await dp.bot.send_photo(chat_id=33180657, photo=open(photo, "rb"), caption=kok, parse_mode="HTML", reply_markup=cat_lan) # reply_markup=cats


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
