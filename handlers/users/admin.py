import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text, Command
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import main_menu, languages, ac_main, ac_users, ac_back
from keyboards.inline import keyboard_markup, lang_markup, ban_markup, rights_markup, orders_a, order_info

from data import lang_en
from loader import dp
from states.orders import Reg, Admin
from utils.db_api import quick_commands
from utils.db_api.models import User
# from dotenv import load_dotenv
# from twilio.rest import Client
# from random import randint
# from utils.db_api.models import User
from utils.misc import rate_limit, get_address_from_coords


# Главное меню админки, с перенаправлением на клавиатуру для админа(ac_main)/оператора(oc_main)/курьера(cc_main)
@rate_limit(1, key="admin")
@dp.message_handler(Command("admin"), state=None)
async def acp(message: types.Message):
    # Проверять есть ли юзер в существующих
    if await quick_commands.select_user(id=message.from_user.id):
        # Проверять есть ли юзер в админах
        if await quick_commands.check_rights(id=message.from_user.id) == 0:
            await message.answer(lang_en.no_permission, reply_markup=main_menu)
        elif await quick_commands.check_rights(id=message.from_user.id) == 1:
            await message.answer(lang_en.succ_login, reply_markup=ac_main)
            await Admin.a_main.set()
        elif await quick_commands.check_rights(id=message.from_user.id) == 2:
            await message.answer(lang_en.no_permission, reply_markup=main_menu)
        elif await quick_commands.check_rights(id=message.from_user.id) == 3:
            await message.answer(lang_en.no_permission, reply_markup=main_menu)

    else:
        # await message.answer(f'Здравствуйте, {message.from_user.full_name}!')
        await message.answer(f"Здравствуйте, {message.from_user.full_name}!\n"
                             "Выберите язык обслуживания.\n\n"
                             f"Hello, {message.from_user.full_name}!\n"
                             "Please, choose your language\n\n"
                             f"Keling, {message.from_user.full_name}!\n"
                             "Avvaliga xizmat ko'rsatish tilini tanlab olaylik", reply_markup=languages)

        await Reg.language.set()


# Клавиатура для админа на управление пользователями (клавиатура поиск по id/номеру и назад)
@rate_limit(1, key="admin_main")
@dp.message_handler(Text(equals=[lang_en.users_eng]), state=Admin.a_main)
async def a_users_main_m(message: types.Message):
    await message.answer(lang_en.opt, reply_markup=ac_users)
    await Admin.users.set()


# Клавиатура для админа на управление заказами (клавиатура все заказы, все заказы по филиалу, все активные заказы, все активные заказы по филиалу, все заказы по id/номеру пользователя, все активные заказы по id/номеру пользователя, инфо заказа по id и назад)
@rate_limit(1, key="admin_main")
@dp.message_handler(Text(equals=[lang_en.orders_eng]), state=Admin.a_main)
async def a_orders_main_m(message: types.Message, state: FSMContext):
    orders = await quick_commands.select_all_orders()
    count_all = 0  # Счетчик всех заказов
    for i in orders:
        if i.status != 7:
            count_all += 1

    kiki = 0 # Счетчик активных заказов
    text = ""
    for branch in await quick_commands.select_all_branches_list():
        count = 0 # Счетчик заказов по филиалу
        for order in await quick_commands.select_active_orders_by_branch(branch):
            count += 1
            kiki += 1
        text += "<i>%s</i> - %s\n" % (branch, count)
    koker = "<i><b>Заказы:</b></i>\n\nКоличество активных заказов (<b>%s</b>):\n\n" % kiki
    kikir = "\n\n\n<b>Всего заказов (не считая отмененных) - %s</b>" % count_all
    txt = koker + text + kikir
    lilo = await message.answer("Загрузка...", reply_markup=ReplyKeyboardRemove())
    await lilo.delete()
    msg = await message.answer(txt, reply_markup=orders_a)
    await state.update_data(msg_id=msg.message_id)
    await Admin.orders.set()


# Возврат в главное меню из админки
@rate_limit(1, key="admin_main")
@dp.message_handler(Text(equals=[lang_en.back_eng]), state=Admin.a_main)
async def a_users_main_m_back(message: types.Message, state: FSMContext):
    await message.answer(lang_en.opt, reply_markup=main_menu)
    await state.finish()


# Возврат на первый хендлер админки при нажатии на кнопку назад из управления пользователями|заказами
@rate_limit(1, key="admin_main_id")
@dp.message_handler(Text(equals=[lang_en.back_eng]), state=Admin.users)
@dp.message_handler(Text(equals=[lang_en.back_eng]), state=Admin.orders)
async def a_users_back(message: types.Message):
    await message.answer(lang_en.opt, reply_markup=ac_main)
    await Admin.a_main.set()


# Поиск пользователя по номеру
@rate_limit(1, key="admin_main_id")
@dp.message_handler(Text(equals=[lang_en.info_by_number_eng]), state=Admin.users)
async def a_users_info_num_kok(message: types.Message):
    await message.answer(lang_en.enter_user_number, reply_markup=ac_back)
    await Admin.user_info_by_number.set()


# Поиск пользователя по id
@rate_limit(1, key="admin_main_id")
@dp.message_handler(Text(equals=[lang_en.info_by_id_eng]), state=Admin.users)
async def a_users_info_id(message: types.Message):
    await message.answer(lang_en.enter_user_id, reply_markup=ac_back)
    await Admin.user_info_by_id.set()


# Поиск пользователя по номеру после ввода номера и проверка на правильность с обработкой нажатия на кнопку назад
@rate_limit(1, key="admin_main_id")
@dp.message_handler(state=Admin.user_info_by_number, content_types=["text"])
async def a_users_n(message: types.Message, state: FSMContext):

    number = message.text
    pattern = '(^\+998[8-9])\d{8}$'
    result = re.match(pattern, number)
    if message.text == lang_en.back_eng:
        await message.answer(lang_en.opt, reply_markup=ac_users)
        await Admin.users.set()
    elif result:
        try:
            user = await quick_commands.select_user_by_number(number)
            await state.update_data(user_id=user.id)
            rights_s = await quick_commands.check_rights_info(user.id)

            banned_s = await quick_commands.check_ban_info(user.id)
            time_registered = user.created_at.strftime("%d.%m.%Y %H:%M:%S")
            time_updated = user.updated_at.strftime("%d.%m.%Y %H:%M:%S")
            info_a = lang_en.info_admin % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            lilo = await message.answer("Загрузка...", reply_markup=ReplyKeyboardRemove())
            await lilo.delete()
            await message.answer(info_a, reply_markup=keyboard_markup)

            await Admin.user_main_info.set()

        except Exception as e:
            err_en = lang_en.err_en % e
            err = "Ошибка:\n%s" % err_en
            await message.answer(err, reply_markup=ac_users)
            await Admin.users.set()
    else:
        err_wrong_en = "Wrong number format\nPlease, entry number in format +998901234567"
        await message.answer(err_wrong_en, reply_markup=ac_back)


# Поиск пользователя по id после ввода id и проверка на правильность с обработкой нажатия на кнопку назад
@rate_limit(1, key="admin_main_id")
@dp.message_handler(state=Admin.user_info_by_id, content_types=["text"])
async def a_users(message: types.Message, state: FSMContext):
    if message.text == lang_en.back_eng:

        await message.answer(lang_en.opt, reply_markup=ac_users)
        await Admin.users.set()
    else:
        try:
            user_m = int(message.text)
            user = await quick_commands.select_user(user_m)
            await state.update_data(user_id=user.id)
            rights_s = await quick_commands.check_rights_info(user.id)

            banned_s = await quick_commands.check_ban_info(user.id)
            time_registered = user.created_at.strftime("%d.%m.%Y %H:%M:%S")
            time_updated = user.updated_at.strftime("%d.%m.%Y %H:%M:%S")
            info_a = lang_en.info_admin % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            lilo = await message.answer("Загрузка...", reply_markup=ReplyKeyboardRemove())
            await lilo.delete()
            await message.answer(info_a, reply_markup=keyboard_markup)

            await Admin.user_main_info.set()

        except Exception as e:
            err_en = lang_en.err_en % e
            err = "Ошибка:\n%s" % err_en
            await message.answer(err, reply_markup=ac_users)
            await Admin.users.set()


# Переход в меню управления пользователем после верного результата поиска по id/номеру
@dp.callback_query_handler(lambda cb: cb.data in ["name", "lang", "number", "orders_no",
                                                  "cashback", "ban", "is_admin", "back"],
                           state=Admin.user_main_info)
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  # send answer to close the rounding circle

    answer_data = query.data
    # logging.info(f"answer_data={answer_data}")
    # here we can work with query.data
    # "name", "lang", "number", "orders_no", "cashback", "ban", "is_admin", "back"
    async with state.proxy() as data:
        user_id = int(data["user_id"])
        user = await quick_commands.select_user(user_id)
        rights_s = await quick_commands.check_rights_info(user.id)
        banned_s = await quick_commands.check_ban_info(user.id)
        time_registered = user.created_at.strftime("%d.%m.%Y %H:%M:%S")
        time_updated = user.updated_at.strftime("%d.%m.%Y %H:%M:%S")

        if answer_data == 'name':
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)
            name_change = lang_en.name_change_succ % user.id
            await dp.bot.send_message(query.from_user.id, name_change, reply_markup=ReplyKeyboardRemove())
            await Admin.user_main_info_name.set()
        elif answer_data == 'lang':
            info_a = lang_en.info_admin % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            lang_choose = info_a + lang_en.lang_choose
            await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                           text=lang_choose, reply_markup=lang_markup)
            await Admin.user_main_info_lang.set()
        elif answer_data == 'number':
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)
            number_change = lang_en.number_change_succ % user.id
            await dp.bot.send_message(query.from_user.id, number_change, reply_markup=ReplyKeyboardRemove())
            await Admin.user_main_info_number.set()
        elif answer_data == 'cashback':
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)
            cashback_change = lang_en.cashback_change_succ % user.id
            await dp.bot.send_message(query.from_user.id, cashback_change, reply_markup=ReplyKeyboardRemove())
            await Admin.user_main_info_cashback.set()
        elif answer_data == 'ban':
            info_a = lang_en.info_admin % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            ban_choose = info_a + lang_en.choose_action_succ
            await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                           text=ban_choose, reply_markup=ban_markup)
            await Admin.user_main_info_ban.set()
        elif answer_data == 'is_admin':
            info_a = lang_en.info_admin % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            rights_choose = info_a + lang_en.rights_select_succ
            await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                           text=rights_choose, reply_markup=rights_markup)
            await Admin.user_main_info_rights.set()
        else:
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)
            await dp.bot.send_message(query.from_user.id,lang_en.opt, reply_markup=ac_users)
            await Admin.users.set()

        # await dp.bot.edit_message_reply_markup(query.from_user.id, query.message.message_id, reply_markup=lang_markup)
    # else:
    #     await bot.send_message(query.from_user.id, "Invalid callback data!")


# Изменение имени пользователя
@rate_limit(1, key="admin_main_id")
@dp.message_handler(state=Admin.user_main_info_name)
async def name_ac_change(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        user_id = int(data["user_id"])
        user1 = await quick_commands.select_user(user_id)
        rights_s = await quick_commands.check_rights_info(user1.id)
        banned_s = await quick_commands.check_ban_info(user1.id)
        time_registered = user1.created_at.strftime("%d.%m.%Y %H:%M:%S")
        time_updated = user1.updated_at.strftime("%d.%m.%Y %H:%M:%S")
        await quick_commands.update_user_name(user_id, name)
        info_a = lang_en.info_admin % (
            user1.id, user1.name, user1.lang_user, user1.number, user1.username, user1.orders_no, user1.referral,
            user1.cashback, banned_s, rights_s, time_registered, time_updated)
        info_b = lang_en.user_name_changed_succ % (user_id, name)
        name_changed = info_a + info_b
        c_c = "Your name was changed to %s" % name
        await dp.bot.send_message(user_id, c_c)
        await message.answer(name_changed, reply_markup=keyboard_markup)
        await Admin.user_main_info.set()


# Изменение языка пользователя
@dp.callback_query_handler(lambda cb: cb.data in ["ru", "uz", "en"], state=Admin.user_main_info_lang)
async def inline_kb_answer_lang_callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  # send answer to close the rounding circle

    answer_data = query.data
    # logging.info(f"answer_data={answer_data}")
    # here we can work with query.data
    # "name", "lang", "number", "orders_no", "cashback", "ban", "is_admin", "back"
    async with state.proxy() as data:
        user_id = int(data["user_id"])
        user = await quick_commands.select_user(user_id)
        rights_s = await quick_commands.check_rights_info(user.id)
        banned_s = await quick_commands.check_ban_info(user.id)
        time_registered = user.created_at.strftime("%d.%m.%Y %H:%M:%S")
        time_updated = user.updated_at.strftime("%d.%m.%Y %H:%M:%S")
        await quick_commands.update_user_language(user_id, answer_data)
        info_a = lang_en.info_admin % (
            user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
            user.cashback, banned_s, rights_s, time_registered, time_updated)
        lang_changed = lang_en.lang_changed_to_succ % (answer_data, user_id)
        lang_changed_a = info_a + lang_changed
        if answer_data == 'ru':
            ans = "Ваш язык был изменен на русский"
        elif answer_data == 'uz':
            ans = "Tiliz o'zgartirildi"
        elif answer_data == 'en':
            ans = "Your language was changed to English"

        await dp.bot.send_message(user_id, ans)
        await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                       text=lang_changed_a, reply_markup=keyboard_markup)
        await Admin.user_main_info.set()
        # await dp.bot.edit_message_reply_markup(query.from_user.id, query.message.message_id, reply_markup=lang_markup)
    # else:
    #     await bot.send_message(query.from_user.id, "Invalid callback data!")


# Изменение номера пользователя
@rate_limit(2, key="nn")
@dp.message_handler(state=Admin.user_main_info_number)
async def acp_nn(message: types.Message, state: FSMContext):
    number = message.text

    pattern = '(^\+998[8-9])\d{8}$'
    result = re.match(pattern, number)

    if result:
        async with state.proxy() as data:
            user_id = int(data["user_id"])
            user1 = await quick_commands.select_user(user_id)
            rights_s = await quick_commands.check_rights_info(user1.id)
            banned_s = await quick_commands.check_ban_info(user1.id)
            time_registered = user1.created_at.strftime("%d.%m.%Y %H:%M:%S")
            time_updated = user1.updated_at.strftime("%d.%m.%Y %H:%M:%S")

            await quick_commands.update_user_number(user_id, number)
            info_a = lang_en.info_admin % (
                user1.id, user1.name, user1.lang_user, user1.number, user1.username, user1.orders_no, user1.referral,
                user1.cashback, banned_s, rights_s, time_registered, time_updated)
            number_changed = lang_en.number_changed_to_succ % (number, user_id)
            number_changed_a = info_a + number_changed
            c_c = "Your number was changed to %s" % number
            await dp.bot.send_message(user_id, c_c)
            await message.answer(number_changed_a, reply_markup=keyboard_markup)
            await Admin.user_main_info.set()
    else:
        await message.answer(lang_en.wrong_number_format)


# Изменение кешбека пользователя
@rate_limit(2, key="nn")
@dp.message_handler(state=Admin.user_main_info_cashback)
async def acp_cashback(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        number = int(message.text)
        async with state.proxy() as data:
            user_id = int(data["user_id"])
            user1 = await quick_commands.select_user(user_id)
            rights_s = await quick_commands.check_rights_info(user1.id)
            banned_s = await quick_commands.check_ban_info(user1.id)
            time_registered = user1.created_at.strftime("%d.%m.%Y %H:%M:%S")
            time_updated = user1.updated_at.strftime("%d.%m.%Y %H:%M:%S")
            await quick_commands.set_cashback(user_id, number)
            info_a = lang_en.info_admin % (
                user1.id, user1.name, user1.lang_user, user1.number, user1.username, user1.orders_no, user1.referral,
                user1.cashback, banned_s, rights_s, time_registered, time_updated)
            cashback_changed = lang_en.cashback_changed_to_succ % (number, user_id)
            cashback_changed_a = info_a + cashback_changed
            c_c = "Your cashback was changed to %s" % number
            await dp.bot.send_message(user_id, c_c)
            await message.answer(cashback_changed_a, reply_markup=keyboard_markup)
            await Admin.user_main_info.set()
    else:
        await message.answer(lang_en.wrong_digit_only_format)


# Изменение статуса бана пользователя
@dp.callback_query_handler(lambda cb: cb.data in ["ban", "unban"], state=Admin.user_main_info_ban)
async def inline_kb_answer_lang_callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  # send answer to close the rounding circle

    answer_data = query.data
    #logging.info(f"answer_data={answer_data}")
    # here we can work with query.data
    # "name", "lang", "number", "orders_no", "cashback", "ban", "is_admin", "back"
    async with state.proxy() as data:
        user_id = int(data["user_id"])
        user = await quick_commands.select_user(user_id)
        if answer_data == "ban":
            await quick_commands.ban_user(user_id)
            await quick_commands.block_user(user)

        else:
            await quick_commands.unban_user(user_id)
            await quick_commands.unblock_user(user)

        # user = await quick_commands.select_user(user_id)
        rights_s = await quick_commands.check_rights_info(user.id)
        banned_s = await quick_commands.check_ban_info(user.id)
        time_registered = user.created_at.strftime("%d.%m.%Y %H:%M:%S")
        time_updated = user.updated_at.strftime("%d.%m.%Y %H:%M:%S")
        info_a = lang_en.info_admin % (
            user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
            user.cashback, banned_s, rights_s, time_registered, time_updated)
        ban_changed = lang_en.ban_changed_to_succ % (answer_data, user_id)
        ban_changed_a = info_a + ban_changed
        c_c = "Your ban status was changed to %s" % answer_data
        await dp.bot.send_message(user_id, c_c)
        await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                       text=ban_changed_a, reply_markup=keyboard_markup)
        await Admin.user_main_info.set()


# Изменение прав пользователю
@dp.callback_query_handler(lambda cb: cb.data in ["0", "1", "2", "3"], state=Admin.user_main_info_rights)
async def inline_kb_answer_lang_callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  # send answer to close the rounding circle

    answer_data = query.data
    #logging.info(f"answer_data={answer_data}")
    # here we can work with query.data
    # "name", "lang", "number", "orders_no", "cashback", "ban", "is_admin", "back"
    async with state.proxy() as data:
        user_id = int(data["user_id"])
        kok = ""
        if answer_data == "1":
            await quick_commands.set_rights(user_id, 1)
            kok = lang_en.admin_eng
        elif answer_data == "2":
            await quick_commands.set_rights(user_id, 2)
            kok = lang_en.operator_eng
        elif answer_data == "3":
            await quick_commands.set_rights(user_id, 3)
            kok = lang_en.courier_eng
        else:
            await quick_commands.set_rights(user_id, 0)
            kok = lang_en.user_eng

        user = await quick_commands.select_user(user_id)
        rights_s = await quick_commands.check_rights_info(user.id)
        banned_s = await quick_commands.check_ban_info(user.id)
        time_registered = user.created_at.strftime("%d.%m.%Y %H:%M:%S")
        time_updated = user.updated_at.strftime("%d.%m.%Y %H:%M:%S")
        info_a = lang_en.info_admin % (
            user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
            user.cashback, banned_s, rights_s, time_registered, time_updated)
        rights_changed = lang_en.rights_changed_to_succ % (kok, user_id)
        rights_changed_a = info_a + rights_changed
        c_c = "Your rights were changed to %s" % kok
        await dp.bot.send_message(user_id, c_c)
        await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                       text=rights_changed_a, reply_markup=keyboard_markup)
        await Admin.user_main_info.set()

# Обработка кнопок в меню заказов
@dp.callback_query_handler(lambda cb: cb.data in ["all", "all_a", "branch", "branch_a","num_id", "num_id_a", "num_id_o", "back"],
                           state=Admin.orders)
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  # send answer to close the rounding circle

    answer_data = query.data

    async with state.proxy() as data:
        msg = data["msg_id"]


        if answer_data == 'all':
            pass
        elif answer_data == 'all_a':
            pass
        elif answer_data == 'branch':
            pass
        elif answer_data == 'branch_a':
            pass
        elif answer_data == 'num_id':
            pass
        elif answer_data == 'num_id_a':
            pass
        elif answer_data == 'num_id_o':
            txt = "Введите номер заказа"
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
            await dp.bot.send_message(query.message.chat.id, txt)
            await Admin.order_by_ID.set()
            # pass
        else:
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id) # Удаляем сообщение с кнопками
            await dp.bot.send_message(query.message.chat.id, lang_en.opt, reply_markup=ac_main)
            await Admin.a_main.set()

        # await dp.bot.edit_message_reply_markup(query.from_user.id, query.message.message_id, reply_markup=lang_markup)
    # else:
    #     await bot.send_message(query.from_user.id, "Invalid callback data!")


# Обработка кнопки поиска по id заказа
# @dp.callback_query_handler(state=Admin.order_by_ID)
@dp.message_handler(state=Admin.order_by_ID)
async def process_order_by_ID(message: types.Message, state: FSMContext):
    global lang # Для перевода
    user_id = message.from_user.id
    lang = await quick_commands.select_language(user_id)
    id = message.text
    try:
        id = int(id)
        await state.update_data(order_id=id)  # Записываем id заказа в state
        order = await quick_commands.select_order_by_id(id)
        txt = "<b>Заказ №%s</b>\n\n" % order.id
        type = ""
        kok = ""
        if order.type_delivery == 1:  # Если доставка
            type = "Доставка"
            coords = f"{order.lon},{order.lat}"
            # print(coords)
            adress = get_address_from_coords(coords)
            kok = "Адрес: %s" % adress[21:]
        elif order.type_delivery == 2:  # Если самовывоз
            type = "Самовывоз"
            kok = "Филиал: %s" % order.branch

        txt += "Тип : %s\n%s\n" % (type, kok)
        number = await quick_commands.select_number(order.user_id)
        paid = ""
        if order.is_paid == 1:
            paid = "Оплачен"
        elif order.is_paid == 0:
            paid = "Не оплачен"
        txt += "Телефон: %s\nСпособ оплаты: %s\nСтатус оплаты: %s\n" % (number, order.p_type, paid)
        if order.comment != "Null":
            txt += "Комментарий: %s\n" % order.comment
        txt += "\n<b>Содержимое:</b>\n\n"
        a = order.items
        # print(a)
        for i, q in a.items():
            # print(id, q)

            name = await quick_commands.select_item_name(int(i), lang)
            # print(name)
            price = await quick_commands.select_item_price(int(i))
            total = int(price) * q
            txt += "<b>%s</b>\n%s x %s = %s\n\n" % (name, price, q, total)
            # print(txt)
        if order.type_delivery == 1:
            txt += "<b>Доставка = </b>%s" % order.delivery_price
        txt += "\n\n\n<b>Итого: </b>%s\n" % order.total_price
        status = ""
        if order.status == 1:
            status = "В обработке"
        elif order.status == 2:
            status = "Подтвержден"
        elif order.status == 3:
            status = "Приготовление"
        elif order.status == 4:
            status = "Доставка"
        elif order.status == 5:
            status = "Доставлен"
        elif order.status == 6:
            status = "Отменен"
        # (1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен)
        await state.update_data(txt=txt)
        txt += "\n<i><b>Статус: %s</b></i>" % status
        # await state.update_data()

        await dp.bot.send_message(message.from_user.id, txt, parse_mode="HTML", reply_markup=order_info)

        await Admin.order_by_ID_action.set()

    except Exception as e:
        error = "Заказа с таким номером не существует"
        await message.answer(error)

        pass


# Хендлер обработки данных при нажатии поиска по ID заказа
@dp.callback_query_handler(state=Admin.order_by_ID_action)
async def process_order_by_ID_action(query: types.CallbackQuery, state: FSMContext):
    global lang
    user_id = query.from_user.id
    status = ""

    async with state.proxy() as data:
        order_id = data["order_id"]
        txt = data["txt"]
        order_id = int(order_id)
    order = await quick_commands.select_order_by_id(order_id)
    if query.data == "confirmed":

        text = ""
        if order.status == 2:
            status = "Заказ уже подтвержден"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        else:

            status = "Подтвержден"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        msg_f_u = "Ваш заказ №%s подтвержден" % order_id
        await quick_commands.change_status(order_id, 2)

        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
        # pass
    elif query.data == "cooking":

        text = ""
        if order.status == 3:
            status = "Заказ уже готовится"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        else:

            status = "Приготовление"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        msg_f_u = "Ваш заказ №%s в процессе приготовления" % order_id
        await quick_commands.change_status(order_id, 3)

        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
    elif query.data == "delivery":
        text = ""
        if order.status == 4:
            status = "Заказ уже доставляется"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        else:

            status = "Доставка"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        msg_f_u = "Ваш заказ №%s в процессе доставки" % order_id
        await quick_commands.change_status(order_id, 4)

        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
    elif query.data == "delivered":
        text = ""
        if order.status == 5:
            status = "Заказ уже доставлен"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        else:

            status = "Доставлен"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        msg_f_u = "Ваш заказ №%s доставлен" % order_id
        await quick_commands.change_status(order_id, 5)

        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
    elif query.data == "payed":
        text = ""
        if order.is_paid == 1:
            status = "Заказ уже оплачен"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        else:

            status = "Оплачен"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        msg_f_u = "Ваш заказ №%s оплачен" % order_id

        await quick_commands.change_payment_status(order_id, 1)

        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)

    elif query.data == "not_payed":
        text = ""
        if order.is_paid == 0:
            status = "Заказ не оплачен"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        else:

            status = "Не оплачен"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        msg_f_u = "Ваш заказ №%s имеет статус неоплачен" % order_id

        await quick_commands.change_payment_status(order_id, 0)

        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
    elif query.data == "add_pos":
        pass
    elif query.data == "remove_pos":
        pass
    elif query.data == "courier_set":
        pass
    elif query.data == "cancel":
        text = ""
        if order.status == 6:
            status = "Заказ уже отменен"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        else:

            status = "Отменен"
            toxt = "\n<i><b>Статус: %s</b></i>" % status
            text = txt + toxt
        msg_f_u = "Ваш заказ №%s отменен" % order_id
        await quick_commands.change_status(order_id, 6)

        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
    elif query.data == "back":
        await query.message.delete()
        orders = await quick_commands.select_all_orders()
        count_all = 0  # Счетчик всех заказов
        for i in orders:
            if i.status != 7:
                count_all += 1

        kiki = 0  # Счетчик активных заказов
        text = ""
        for branch in await quick_commands.select_all_branches_list():
            count = 0  # Счетчик заказов по филиалу
            for order in await quick_commands.select_active_orders_by_branch(branch):
                count += 1
                kiki += 1
            text += "<i>%s</i> - %s\n" % (branch, count)

        koker = "<i><b>Заказы:</b></i>\n\nКоличество активных заказов (<b>%s</b>):\n\n" % kiki
        kikir = "\n\n\n<b>Всего заказов (не считая отмененных) - %s</b>" % count_all
        txt = koker + text + kikir
        lilo = await dp.bot.send_message(query.from_user.id,"Загрузка...", reply_markup=ReplyKeyboardRemove())
        await lilo.delete()
        msg = await dp.bot.send_message(query.from_user.id, txt, parse_mode="HTML", reply_markup=orders_a)
        #  msg = await message.answer(txt, reply_markup=orders_a)
        await state.update_data(msg_id=msg.message_id)
        await Admin.orders.set()
