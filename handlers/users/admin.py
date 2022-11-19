import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text, Command
from aiogram.types import ReplyKeyboardRemove
from keyboards.default import main_menu, languages, ac_main, ac_users, ac_back
from keyboards.inline import keyboard_markup, lang_markup, ban_markup, rights_markup, orders_a, order_info, \
    order_by_id_quantity
from loader import dp
from states.orders import Reg, Admin
from utils.db_api import quick_commands
# from dotenv import load_dotenv
# from twilio.rest import Client
from utils.misc import rate_limit


# Главное меню админки, с перенаправлением на клавиатуру для админа(ac_main)/оператора(oc_main)/курьера(cc_main)
@rate_limit(1, key="admin")
@dp.message_handler(Command("admin"), state=None)
async def acp(message: types.Message):
    # Проверять есть ли юзер в существующих
    if await quick_commands.select_user(id=message.from_user.id):
        # Проверять есть ли юзер в админах
        if await quick_commands.check_rights(id=message.from_user.id) == 0:
            await message.answer("You do not have permission to use this command", reply_markup=main_menu)
        elif await quick_commands.check_rights(id=message.from_user.id) == 1:
            await message.answer("You have successfully logged in", reply_markup=ac_main)
            await Admin.a_main.set()
        elif await quick_commands.check_rights(id=message.from_user.id) == 2:
            await message.answer("You do not have permission to use this command", reply_markup=main_menu)
        elif await quick_commands.check_rights(id=message.from_user.id) == 3:
            await message.answer("You do not have permission to use this command", reply_markup=main_menu)

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
@dp.message_handler(Text(equals=["Users"]), state=Admin.a_main)
async def a_users_main_m(message: types.Message):
    await message.answer("Choose option", reply_markup=ac_users)
    await Admin.users.set()


# Клавиатура для админа на управление заказами (клавиатура все заказы, филиалу, активные,
# все активные заказы по филиалу, все заказы по id/номеру пользователя, все активные заказы по id/номеру пользователя,
# инфо заказа по id и назад)
@rate_limit(1, key="admin_main")
@dp.message_handler(Text(equals=["Orders"]), state=Admin.a_main)
async def a_orders_main_m(message: types.Message, state: FSMContext):
    orders = await quick_commands.select_all_orders()
    count_all = 0  # Счетчик всех заказов
    count_not_all = 0  # Счетчик заказов
    for i in orders:
        if i.status != 6:
            count_not_all += 1
            if i.status != 5:
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
    kikir = "\n\n\n<b>Всего заказов (не считая отмененных)- %s</b>\n<b>Всего заказов (не считая отмененных и доставленных)- %s</b>" % (
    count_not_all, count_all)
    txt = koker + text + kikir
    lilo = await message.answer("Загрузка...", reply_markup=ReplyKeyboardRemove())
    await lilo.delete()
    msg = await message.answer(txt, reply_markup=orders_a)
    await state.update_data(msg_id=msg.message_id)
    await Admin.orders.set()


# Возврат в главное меню из админки
@rate_limit(1, key="admin_main")
@dp.message_handler(Text(equals=["Back"]), state=Admin.a_main)
async def a_users_main_m_back(message: types.Message, state: FSMContext):
    await message.answer("Choose option", reply_markup=main_menu)
    await state.finish()


# Возврат на первый хендлер админки при нажатии на кнопку назад из управления пользователями|заказами
@rate_limit(1, key="admin_main_id")
@dp.message_handler(Text(equals=["Back"]), state=Admin.users)
@dp.message_handler(Text(equals=["Back"]), state=Admin.orders)
async def a_users_back(message: types.Message):
    await message.answer("Choose option", reply_markup=ac_main)
    await Admin.a_main.set()


# Поиск пользователя по номеру
@rate_limit(1, key="admin_main_id")
@dp.message_handler(Text(equals=["Info by number"]), state=Admin.users)
async def a_users_info_num_kok(message: types.Message):
    await message.answer("Enter user number", reply_markup=ac_back)
    await Admin.user_info_by_number.set()


# Поиск пользователя по id
@rate_limit(1, key="admin_main_id")
@dp.message_handler(Text(equals=["Info by ID"]), state=Admin.users)
async def a_users_info_id(message: types.Message):
    await message.answer("Enter user ID", reply_markup=ac_back)
    await Admin.user_info_by_id.set()


# Поиск пользователя по номеру после ввода номера и проверка на правильность с обработкой нажатия на кнопку назад
@rate_limit(1, key="admin_main_id")
@dp.message_handler(state=Admin.user_info_by_number, content_types=["text"])
async def a_users_n(message: types.Message, state: FSMContext):
    number = message.text
    pattern = '(^\+998[8-9])\d{8}$'
    result = re.match(pattern, number)
    if message.text == "Back":
        await message.answer("Choose option", reply_markup=ac_users)
        await Admin.users.set()
    elif result:
        try:
            user = await quick_commands.select_user_by_number(number)
            await state.update_data(user_id=user.id)
            rights_s = await quick_commands.check_rights_info(user.id)

            banned_s = await quick_commands.check_ban_info(user.id)
            time_registered = user.created_at.strftime("%d.%m.%Y %H:%M:%S")
            time_updated = user.updated_at.strftime("%d.%m.%Y %H:%M:%S")
            info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            lilo = await message.answer("Загрузка...", reply_markup=ReplyKeyboardRemove())
            await lilo.delete()
            await message.answer(info_a, reply_markup=keyboard_markup)

            await Admin.user_main_info.set()

        except Exception as e:
            err_en = "Error: %s" % e
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
    if message.text == "Back":

        await message.answer("Choose option", reply_markup=ac_users)
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
            info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            lilo = await message.answer("Загрузка...", reply_markup=ReplyKeyboardRemove())
            await lilo.delete()
            await message.answer(info_a, reply_markup=keyboard_markup)

            await Admin.user_main_info.set()

        except Exception as e:
            err_en = "Error: %s" % e
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
            name_change = "Enter a new name for user %s" % user.id
            await dp.bot.send_message(query.from_user.id, name_change, reply_markup=ReplyKeyboardRemove())
            await Admin.user_main_info_name.set()
        elif answer_data == 'lang':
            info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            lang_choose = info_a + "Choose language"
            await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                           text=lang_choose, reply_markup=lang_markup)
            await Admin.user_main_info_lang.set()
        elif answer_data == 'number':
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)
            number_change = "Enter a new number in format +998911234567 for user %s" % user.id
            await dp.bot.send_message(query.from_user.id, number_change, reply_markup=ReplyKeyboardRemove())
            await Admin.user_main_info_number.set()
        elif answer_data == 'cashback':
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)
            cashback_change = "Enter a new cashback amount for user %s" % user.id
            await dp.bot.send_message(query.from_user.id, cashback_change, reply_markup=ReplyKeyboardRemove())
            await Admin.user_main_info_cashback.set()
        elif answer_data == 'ban':
            info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            ban_choose = info_a + "Choose an action"
            await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                           text=ban_choose, reply_markup=ban_markup)
            await Admin.user_main_info_ban.set()
        elif answer_data == 'is_admin':
            info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
                user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
                user.cashback, banned_s, rights_s, time_registered, time_updated)
            rights_choose = info_a + "Choose user rights"
            await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                           text=rights_choose, reply_markup=rights_markup)
            await Admin.user_main_info_rights.set()
        else:
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)
            await dp.bot.send_message(query.from_user.id, "Choose option", reply_markup=ac_users)
            await Admin.users.set()


# Изменение имени пользователя
@rate_limit(1, key="admin_main_id")
@dp.message_handler(state=Admin.user_main_info_name)
async def name_ac_change(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        user_id = int(data["user_id"])
        await quick_commands.update_user_name(user_id, name)
        user1 = await quick_commands.select_user(user_id)
        rights_s = await quick_commands.check_rights_info(user1.id)
        banned_s = await quick_commands.check_ban_info(user1.id)
        time_registered = user1.created_at.strftime("%d.%m.%Y %H:%M:%S")
        time_updated = user1.updated_at.strftime("%d.%m.%Y %H:%M:%S")

        info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
            user1.id, user1.name, user1.lang_user, user1.number, user1.username, user1.orders_no, user1.referral,
            user1.cashback, banned_s, rights_s, time_registered, time_updated)
        info_b = "User %s name changed to %s" % (user_id, name)
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
        await quick_commands.update_user_language(user_id, answer_data)
        user = await quick_commands.select_user(user_id)
        rights_s = await quick_commands.check_rights_info(user.id)
        banned_s = await quick_commands.check_ban_info(user.id)
        time_registered = user.created_at.strftime("%d.%m.%Y %H:%M:%S")
        time_updated = user.updated_at.strftime("%d.%m.%Y %H:%M:%S")

        info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
            user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
            user.cashback, banned_s, rights_s, time_registered, time_updated)
        lang_changed = "Language changed to %s for user %s" % (answer_data, user_id)
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
            await quick_commands.update_user_number(user_id, number)
            user1 = await quick_commands.select_user(user_id)
            rights_s = await quick_commands.check_rights_info(user1.id)
            banned_s = await quick_commands.check_ban_info(user1.id)
            time_registered = user1.created_at.strftime("%d.%m.%Y %H:%M:%S")
            time_updated = user1.updated_at.strftime("%d.%m.%Y %H:%M:%S")

            info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
                user1.id, user1.name, user1.lang_user, user1.number, user1.username, user1.orders_no, user1.referral,
                user1.cashback, banned_s, rights_s, time_registered, time_updated)
            number_changed = "Number changed to %s for user %s" % (number, user_id)
            number_changed_a = info_a + number_changed
            c_c = "Your number was changed to %s" % number
            await dp.bot.send_message(user_id, c_c)
            await message.answer(number_changed_a, reply_markup=keyboard_markup)
            await Admin.user_main_info.set()
    else:
        await message.answer("Wrong number format.\nPlease enter a number in format +998911234567")


# Изменение кешбека пользователя
@rate_limit(2, key="nn")
@dp.message_handler(state=Admin.user_main_info_cashback)
async def acp_cashback(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        number = int(message.text)
        async with state.proxy() as data:
            user_id = int(data["user_id"])
            await quick_commands.set_cashback(user_id, number)
            user1 = await quick_commands.select_user(user_id)
            rights_s = await quick_commands.check_rights_info(user1.id)
            banned_s = await quick_commands.check_ban_info(user1.id)
            time_registered = user1.created_at.strftime("%d.%m.%Y %H:%M:%S")
            time_updated = user1.updated_at.strftime("%d.%m.%Y %H:%M:%S")
            info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
                user1.id, user1.name, user1.lang_user, user1.number, user1.username, user1.orders_no, user1.referral,
                user1.cashback, banned_s, rights_s, time_registered, time_updated)
            cashback_changed = "Cashback changed to %s for user %s" % (number, user_id)
            cashback_changed_a = info_a + cashback_changed
            c_c = "Your cashback was changed to %s" % number
            await dp.bot.send_message(user_id, c_c)
            await message.answer(cashback_changed_a, reply_markup=keyboard_markup)
            await Admin.user_main_info.set()
    else:
        await message.answer("Wrong number format.\nPlease enter a number in digits only")


# Изменение статуса бана пользователя
@dp.callback_query_handler(lambda cb: cb.data in ["ban", "unban"], state=Admin.user_main_info_ban)
async def inline_kb_answer_lang_callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  # send answer to close the rounding circle

    answer_data = query.data
    # logging.info(f"answer_data={answer_data}")
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
        info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
            user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
            user.cashback, banned_s, rights_s, time_registered, time_updated)
        ban_changed = "Ban status changed to %s for user %s" % (answer_data, user_id)
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
    # logging.info(f"answer_data={answer_data}")
    # here we can work with query.data
    # "name", "lang", "number", "orders_no", "cashback", "ban", "is_admin", "back"
    async with state.proxy() as data:
        user_id = int(data["user_id"])
        kok = ""
        if answer_data == "1":
            await quick_commands.set_rights(user_id, 1)
            kok = "Admin"
        elif answer_data == "2":
            await quick_commands.set_rights(user_id, 2)
            kok = "Operator"
        elif answer_data == "3":
            await quick_commands.set_rights(user_id, 3)
            kok = "Courier"
        else:
            await quick_commands.set_rights(user_id, 0)
            kok = "User"

        user = await quick_commands.select_user(user_id)
        rights_s = await quick_commands.check_rights_info(user.id)
        banned_s = await quick_commands.check_ban_info(user.id)
        time_registered = user.created_at.strftime("%d.%m.%Y %H:%M:%S")
        time_updated = user.updated_at.strftime("%d.%m.%Y %H:%M:%S")
        info_a = "ID: %s\nName: %s\nLanguage: %s\nNumber: %s\nUsername: @%s\nOrders number: %s\nReferral link: %s\nCashback: %s\nBanned? %s\nRights: %s\nRegistration date: %s\nLast update date: %s\n\n" % (
            user.id, user.name, user.lang_user, user.number, user.username, user.orders_no, user.referral,
            user.cashback, banned_s, rights_s, time_registered, time_updated)
        rights_changed = "Rights changed to %s for user %s" % (kok, user_id)
        rights_changed_a = info_a + rights_changed
        c_c = "Your rights were changed to %s" % kok
        await dp.bot.send_message(user_id, c_c)
        await dp.bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                       text=rights_changed_a, reply_markup=keyboard_markup)
        await Admin.user_main_info.set()


# Обработка кнопок в меню заказов
@dp.callback_query_handler(
    lambda cb: cb.data in ["all", "all_a", "branch", "branch_a", "num_id", "num_id_a", "num_id_o", "back"],
    state=Admin.orders)
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  # send answer to close the rounding circle

    answer_data = query.data

    async with state.proxy() as data:
        msg = data["msg_id"]

        if answer_data == 'all':  # Все заказы
            keyboard_all_orders = types.InlineKeyboardMarkup(row_width=1)
            orders = await quick_commands.select_all_orders()
            for order in orders:
                text = "Список всех заказов.\n\n<i>Выберите заказ из списка ниже:</i>"
                if order.status == 1:
                    status = "Активный"
                elif order.status == 2:  # 1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен
                    status = "Подтвержден"
                elif order.status == 3:
                    status = "Приготовление"
                elif order.status == 4:
                    status = "Доставка"
                elif order.status == 5:
                    status = "Доставлен"
                elif order.status == 6:
                    status = "Отменен"

                button = "№%s %s" % (order.id, status)
                keyboard_all_orders.add(types.InlineKeyboardButton(text=button, callback_data=order.id))
            keyboard_all_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
            await dp.bot.send_message(query.message.chat.id, text, reply_markup=keyboard_all_orders)
            await Admin.order_call.set()

        elif answer_data == 'all_a':  # Все активные заказы
            keyboard_all_a_orders = types.InlineKeyboardMarkup(row_width=1)
            orders = await quick_commands.select_all_active_orders()
            for order in orders:
                text = "Список всех активных заказов.\n\n<i>Выберите заказ из списка ниже:</i>"
                status = "Активный"
                button = "№%s %s" % (order.id, status)
                keyboard_all_a_orders.add(types.InlineKeyboardButton(text=button, callback_data=order.id))
            keyboard_all_a_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
            await dp.bot.send_message(query.message.chat.id, text, reply_markup=keyboard_all_a_orders)
            await Admin.order_call.set()
        elif answer_data == 'branch':  # Все заказы по филиалу
            keyboard_all_a_orders = types.InlineKeyboardMarkup(row_width=1)
            orders = await quick_commands.select_all_branches()
            for order in orders:
                text = "<i>Выберите филиал из списка ниже:</i>"
                keyboard_all_a_orders.add(types.InlineKeyboardButton(order.name, callback_data=order.name))
            keyboard_all_a_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
            await dp.bot.send_message(query.message.chat.id, text, reply_markup=keyboard_all_a_orders)
            await Admin.order_by_fil.set()
        elif answer_data == 'branch_a':  # Активные заказы по филиалу
            keyboard_all_a_orders = types.InlineKeyboardMarkup(row_width=1)
            orders = await quick_commands.select_all_branches()
            for order in orders:
                text = "<i>Выберите филиал из списка ниже:</i>"
                keyboard_all_a_orders.add(types.InlineKeyboardButton(order.name, callback_data=order.name))
            keyboard_all_a_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
            await dp.bot.send_message(query.message.chat.id, text, reply_markup=keyboard_all_a_orders)
            await Admin.order_a_by_fil.set()
        elif answer_data == 'num_id':  # Заказы по id/номеру пользователя
            txt = "Введите <b>id</b> или <b>номер</b> пользователя:"
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
            await dp.bot.send_message(query.message.chat.id, txt)
            await Admin.order_by_num.set()
        elif answer_data == 'num_id_a':  # Активные заказы по id/номеру пользователя
            txt = "Введите <b>id</b> или <b>номер</b> пользователя:"
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
            await dp.bot.send_message(query.message.chat.id, txt)
            await Admin.order_a_by_num.set()
        elif answer_data == 'num_id_o':  # Поиск по номеру заказа
            txt = "Введите номер заказа"
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
            await dp.bot.send_message(query.message.chat.id, txt)
            await Admin.order_by_ID.set()
            # pass
        elif answer_data == 'back':  # Назад
            await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем сообщение с кнопками
            await dp.bot.send_message(query.message.chat.id, "Choose option", reply_markup=ac_main)
            await Admin.a_main.set()

        # await dp.bot.edit_message_reply_markup(query.from_user.id, query.message.message_id, reply_markup=lang_markup)
    # else:
    #     await bot.send_message(query.from_user.id, "Invalid callback data!")


# Вывод списка активных заказов по филиалу
@dp.callback_query_handler(state=Admin.order_a_by_fil)
async def process_a_orders_by_branch(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'back':
        orders = await quick_commands.select_all_orders()
        count_all = 0  # Счетчик всех заказов
        count_not_all = 0  # Счетчик заказов
        for i in orders:
            if i.status != 6:
                count_not_all += 1
                if i.status != 5:
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
        kikir = "\n\n\n<b>Всего заказов (не считая отмененных)- %s</b>\n<b>Всего заказов (не считая отмененных и доставленных)- %s</b>" % (
            count_not_all, count_all)
        txt = koker + text + kikir
        await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
        msg = await dp.bot.send_message(query.message.chat.id, txt, reply_markup=orders_a)
        # msg = await message.answer(txt, reply_markup=orders_a)
        await state.update_data(msg_id=msg.message_id)
        await Admin.orders.set()
    else:

        user_id = query.from_user.id
        lang = await quick_commands.select_language(user_id)
        branch = query.data
        text = "<i>Выберите заказ из списка ниже:</i>"
        keyboard_all_a_orders = types.InlineKeyboardMarkup(row_width=1)
        orders = await quick_commands.select_active_orders_by_branch(branch)
        for order in orders:
            status = ""
            if order.status == 1:
                status = "Активный"
            elif order.status == 2:  # 1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен
                status = "Подтвержден"
            elif order.status == 3:
                status = "Приготовление"
            elif order.status == 4:
                status = "Доставка"
            elif order.status == 5:
                status = "Доставлен"
            elif order.status == 6:
                status = "Отменен"
            # text = "<i>Выберите заказ из списка ниже:</i>"
            order_in = "№%s %s" % (order.id, status)
            keyboard_all_a_orders.add(types.InlineKeyboardButton(order_in, callback_data=order.id))
        keyboard_all_a_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
        await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
        await dp.bot.send_message(query.message.chat.id, text, reply_markup=keyboard_all_a_orders)
        await Admin.order_call.set()


# Вывод списка заказов по выбранному филиалу
@dp.callback_query_handler(state=Admin.order_by_fil)
async def process_orders_by_branch(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'back':
        orders = await quick_commands.select_all_orders()
        count_all = 0  # Счетчик всех заказов
        count_not_all = 0  # Счетчик заказов
        for i in orders:
            if i.status != 6:
                count_not_all += 1
                if i.status != 5:
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
        kikir = "\n\n\n<b>Всего заказов (не считая отмененных)- %s</b>\n<b>Всего заказов (не считая отмененных и доставленных)- %s</b>" % (
            count_not_all, count_all)
        txt = koker + text + kikir
        await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
        msg = await dp.bot.send_message(query.message.chat.id, txt, reply_markup=orders_a)
        # msg = await message.answer(txt, reply_markup=orders_a)
        await state.update_data(msg_id=msg.message_id)
        await Admin.orders.set()
    else:
        user_id = query.from_user.id
        lang = await quick_commands.select_language(user_id)
        branch = query.data
        text = "<i>Выберите заказ из списка ниже:</i>"
        keyboard_all_a_orders = types.InlineKeyboardMarkup(row_width=1)
        orders = await quick_commands.select_orders_by_branch(branch)
        for order in orders:
            status = ""
            if order.status == 1:
                status = "Активный"
            elif order.status == 2:  # 1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен
                status = "Подтвержден"
            elif order.status == 3:
                status = "Приготовление"
            elif order.status == 4:
                status = "Доставка"
            elif order.status == 5:
                status = "Доставлен"
            elif order.status == 6:
                status = "Отменен"
            # text = "<i>Выберите заказ из списка ниже:</i>"
            order_in = "№%s %s" % (order.id, status)
            keyboard_all_a_orders.add(types.InlineKeyboardButton(order_in, callback_data=order.id))
        keyboard_all_a_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
        await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
        await dp.bot.send_message(query.message.chat.id, text, reply_markup=keyboard_all_a_orders)
        await Admin.order_call.set()


# Обработка поиска заказа по id/номеру пользователя
@dp.message_handler(state=Admin.order_by_num)
async def process_order_by_user_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await quick_commands.select_language(user_id)
    id = message.text
    text = ""
    pattern = '(^\+998[8-9])\d{8}$'
    result = re.match(pattern, id)
    int_id = int(id)

    keyboard_all_a_orders = types.InlineKeyboardMarkup(row_width=1)
    if result:
        user = await quick_commands.select_user_by_number(id)
        orders = await quick_commands.select_all_orders_by_id(user.id)
        for order in orders:
            status = ""
            if order.status == 1:
                status = "Активный"
            elif order.status == 2:  # 1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен
                status = "Подтвержден"
            elif order.status == 3:
                status = "Приготовление"
            elif order.status == 4:
                status = "Доставка"
            elif order.status == 5:
                status = "Доставлен"
            elif order.status == 6:
                status = "Отменен"
            text = "<i>Выберите заказ из списка ниже:</i>"
            order_in = "№%s %s" % (order.id, status)
            keyboard_all_a_orders.add(types.InlineKeyboardButton(order_in, callback_data=order.id))
        keyboard_all_a_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
        # await dp.bot.delete_message(message.chat.id, message.message_id)  # Удаляем смс
        await dp.bot.send_message(message.chat.id, text, reply_markup=keyboard_all_a_orders)
        await Admin.order_call.set()
    elif int_id:
        user = await quick_commands.select_user(int_id)
        orders = await quick_commands.select_all_orders_by_id(user.id)
        for order in orders:
            status = ""
            if order.status == 1:
                status = "Активный"
            elif order.status == 2:  # 1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен
                status = "Подтвержден"
            elif order.status == 3:
                status = "Приготовление"
            elif order.status == 4:
                status = "Доставка"
            elif order.status == 5:
                status = "Доставлен"
            elif order.status == 6:
                status = "Отменен"
            text = "<i>Выберите заказ из списка ниже:</i>"
            order_in = "№%s %s" % (order.id, status)
            keyboard_all_a_orders.add(types.InlineKeyboardButton(order_in, callback_data=order.id))
        keyboard_all_a_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
        # await dp.bot.delete_message(message.chat.id, message.message_id)  # Удаляем смс
        await dp.bot.send_message(message.chat.id, text, reply_markup=keyboard_all_a_orders)
        await Admin.order_call.set()
    else:
        text = "Неверный формат данных!"
        await dp.bot.send_message(message.chat.id, text)  # Удаляем смс


# Обработка поиска активных заказов по id/номеру пользователя
@dp.message_handler(state=Admin.order_a_by_num)
async def process_order_by_user_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await quick_commands.select_language(user_id)
    id = message.text
    text = ""
    pattern = '(^\+998[8-9])\d{8}$'
    result = re.match(pattern, id)
    int_id = int(id)

    keyboard_all_a_orders = types.InlineKeyboardMarkup(row_width=1)
    if result:
        user = await quick_commands.select_user_by_number(id)
        orders = await quick_commands.select_all_active_orders_by_id(user.id)
        for order in orders:
            status = ""
            if order.status == 1:
                status = "Активный"
            elif order.status == 2:  # 1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен
                status = "Подтвержден"
            elif order.status == 3:
                status = "Приготовление"
            elif order.status == 4:
                status = "Доставка"
            elif order.status == 5:
                status = "Доставлен"
            elif order.status == 6:
                status = "Отменен"
            text = "<i>Выберите заказ из списка ниже:</i>"
            order_in = "№%s %s" % (order.id, status)
            keyboard_all_a_orders.add(types.InlineKeyboardButton(order_in, callback_data=order.id))
        keyboard_all_a_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
        # await dp.bot.delete_message(message.chat.id, message.message_id)  # Удаляем смс
        await dp.bot.send_message(message.chat.id, text, reply_markup=keyboard_all_a_orders)
        await Admin.order_call.set()
    elif int_id:
        user = await quick_commands.select_user(int_id)
        orders = await quick_commands.select_all_active_orders_by_id(user.id)
        for order in orders:
            status = ""
            if order.status == 1:
                status = "Активный"
            elif order.status == 2:  # 1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен
                status = "Подтвержден"
            elif order.status == 3:
                status = "Приготовление"
            elif order.status == 4:
                status = "Доставка"
            elif order.status == 5:
                status = "Доставлен"
            elif order.status == 6:
                status = "Отменен"
            text = "<i>Выберите заказ из списка ниже:</i>"
            order_in = "№%s %s" % (order.id, status)
            keyboard_all_a_orders.add(types.InlineKeyboardButton(order_in, callback_data=order.id))
        keyboard_all_a_orders.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
        # await dp.bot.delete_message(message.chat.id, message.message_id)  # Удаляем смс
        await dp.bot.send_message(message.chat.id, text, reply_markup=keyboard_all_a_orders)
        await Admin.order_call.set()
    else:
        text = "Неверный формат данных!"
        await dp.bot.send_message(message.chat.id, text)  # Удаляем смс


# Обработка кнопки поиска по id заказа
# @dp.callback_query_handler(state=Admin.order_by_ID)
@dp.message_handler(state=Admin.order_by_ID)
async def process_order_by_ID(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await quick_commands.select_language(user_id)
    id = message.text
    try:
        id = int(id)
        await state.update_data(order_id=id)  # Записываем id заказа в state
        order = await quick_commands.select_order_by_id(id)
        txt = await quick_commands.admin_text(id, lang)
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
        txt += "\n<i><b>Статус: %s</b></i>" % status
        # await state.update_data()

        await dp.bot.send_message(message.from_user.id, txt, parse_mode="HTML", reply_markup=order_info)

        await Admin.order_by_ID_action.set()

    except Exception as e:
        error = "Заказа с таким номером не существует"
        await message.answer(error)


# Хендлер обработки данных при нажатии поиска по ID заказа
@dp.callback_query_handler(state=Admin.order_by_ID_action)
async def process_order_by_ID_action(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    status = ""
    lang = await quick_commands.select_language(user_id)

    async with state.proxy() as data:
        order_id = data["order_id"]
        txt = await quick_commands.admin_text(order_id, lang)
        order_id = int(order_id)
    order = await quick_commands.select_order_by_id(order_id)
    if query.data == "confirmed":

        text = ""
        msg_f_u = "Статус вашего заказа №%s: %s"
        toxt = "\n<i><b>Статус: %s</b></i>"
        status = ""
        if order.status == 2:
            status = "Заказ уже подтвержден"
        elif order.status == 3:
            status = "изменен с приготовления на подтвержден"
        elif order.status == 4:
            status = "изменен с доставки на подтвержден"
        elif order.status == 5:
            status = "изменен с доставлен на подтвержден"
            await quick_commands.remove_order_from_user(order.user_id)
            await quick_commands.remove_cashback_from_user(order.user_id, order.id)
        elif order.status == 6:
            status = "изменен с отменен на подтвержден"
        else:
            status = "Подтвержден"
        toxt = toxt % status
        text = txt + toxt
        msg_f_u = msg_f_u % (order_id, status)
        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await quick_commands.change_status(order_id, 2)
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
        # pass
    elif query.data == "cooking":

        text = ""
        msg_f_u = "Статус вашего заказа №%s: %s"
        toxt = "\n<i><b>Статус: %s</b></i>"
        status = ""
        if order.status == 3:
            status = "Заказ уже в процессе приготовления"
        elif order.status == 4:
            status = "изменен с доставка на в процессе приготовления"
        elif order.status == 5:
            status = "изменен с доставлен на в процессе приготовления"
            await quick_commands.remove_order_from_user(order.user_id)
            await quick_commands.remove_cashback_from_user(order.user_id, order.id)
        elif order.status == 6:
            status = "изменен с отменен на в процессе приготовления"
        else:
            status = "Приготовление"
        toxt = toxt % status
        text = txt + toxt
        msg_f_u = msg_f_u % (order_id, status)
        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await quick_commands.change_status(order_id, 3)
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
    elif query.data == "delivery":
        text = ""
        msg_f_u = "Статус вашего заказа №%s: %s"
        toxt = "\n<i><b>Статус: %s</b></i>"
        status = ""
        if order.status == 4:
            status = "Заказ уже доставляется"
        elif order.status == 5:
            status = "изменен с доставлен на доставляется"
            await quick_commands.remove_order_from_user(order.user_id)
            await quick_commands.remove_cashback_from_user(order.user_id, order.id)
        elif order.status == 6:
            status = "изменен с отменен на доставляется"
        else:
            status = "Доставка"
        toxt = toxt % status
        text = txt + toxt
        msg_f_u = msg_f_u % (order_id, status)
        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await quick_commands.change_status(order_id, 4)
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
    elif query.data == "delivered":
        text = ""
        msg_f_u = "Статус вашего заказа №%s: %s"
        toxt = "\n<i><b>Статус: %s</b></i>"
        status = ""
        if order.status == 5:
            status = "Заказ уже доставлен"
        elif order.status == 6:
            status = "изменен с отменен на доставлен"
            await quick_commands.add_order_to_user(order.user_id)
            await quick_commands.set_cashback_to_user(order.user_id, order.id)
        else:
            status = "Доставлен"
            await quick_commands.add_order_to_user(order.user_id)
            await quick_commands.set_cashback_to_user(order.user_id, order.id)
        toxt = toxt % status
        text = txt + toxt
        msg_f_u = msg_f_u % (order_id, status)
        await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        # await quick_commands.add_order_to_user(order.user_id)
        await quick_commands.change_status(order_id, 5)
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
    elif query.data == "payed":
        text = ""
        status_o = ""
        if order.is_paid == 1:
            status_o = "Заказ уже оплачен"
        else:
            status_o = "Оплачен"
            msg_f_u = "Ваш заказ №%s оплачен" % order_id
            await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await quick_commands.change_payment_status(order_id, 1)
        # await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)

        try:
            order = await quick_commands.select_order_by_id(order_id)
            txt = await quick_commands.admin_text(order_id, lang)
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
            txt += "\n<i><b>Статус: %s</b></i>" % status
            txt += "\n\n\n<i>Статус оплаты заказа изменен на <b>%s</b></i>" % status_o
            await query.message.edit_text(txt, parse_mode="HTML", reply_markup=order_info)
            # await dp.bot.send_message(message.from_user.id, txt, parse_mode="HTML", reply_markup=order_info)

            await Admin.order_by_ID_action.set()

        except Exception as e:
            error = "Заказа с таким номером не существует"
            # await dp.bot.answer_callback_query(user_id, text=error, show_alert=True)
            # await query.answer(error, show_alert=True)
            # await dp.bot.send_message(user_id, error)

    elif query.data == "not_payed":
        text = ""
        status_o = ""
        if order.is_paid == 0:
            status_o = "Заказ не оплачен"
        else:

            status_o = "Не оплачен"
            msg_f_u = "Ваш заказ №%s имеет статус неоплаченного" % order_id
            await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await quick_commands.change_payment_status(order_id, 0)
        try:
            order = await quick_commands.select_order_by_id(order_id)
            txt = await quick_commands.admin_text(order_id, lang)
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
            txt += "\n<i><b>Статус: %s</b></i>" % status
            txt += "\n\n\n<i>Статус оплаты заказа изменен на <b>%s</b></i>" % status_o
            await query.message.edit_text(txt, parse_mode="HTML", reply_markup=order_info)
            await dp.bot.answer_callback_query(query.id, "koker", show_alert=True)
            # await dp.bot.send_message(message.from_user.id, txt, parse_mode="HTML", reply_markup=order_info)

            await Admin.order_by_ID_action.set()

        except Exception as e:
            error = "Заказа с таким номером не существует"
            # await dp.bot.answer_callback_query(user_id,text=error, show_alert=True)
            # await query.answer(error, show_alert=True)
            # await dp.bot.send_message(user_id, error)
    elif query.data == "add_pos":
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
        toxt = "\n<i><b>Статус: %s</b></i>\n\n" % status
        text = txt + toxt
        tix_t = "Какой товар добавить?\n\n"
        text += tix_t

        items_keyboard = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        items_list = await quick_commands.select_all_items()
        # print(items_list)
        # print(order.items)

        for i in items_list:
            id = int(i)
            item = await quick_commands.get_item_by_id(id)
            # print(item.id)
            if lang == "ru":
                # print(item.name_ru)
                items_keyboard.add(types.InlineKeyboardButton(item.name_ru, callback_data=f"{item.id}"))
            elif lang == "en":
                items_keyboard.add(types.InlineKeyboardButton(item.name_en, callback_data=f"{item.id}"))
            elif lang == "uz":
                items_keyboard.add(types.InlineKeyboardButton(item.name_uz, callback_data=f"{item.id}"))

        # await query.message.edit_reply_markup(reply_markup=items_keyboard)
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=items_keyboard)
        await Admin.order_add_item.set()

    elif query.data == "remove_pos":
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
        toxt = "\n<i><b>Статус: %s</b></i>\n\n" % status
        text = txt + toxt
        tix_t = "Какой товар удалить?\n\n"
        text += tix_t

        items_keyboard = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        items_list = await quick_commands.get_items_in_order(order_id)
        # print(items_list)
        # print(order.items)

        for i in items_list:
            id = int(i)
            item = await quick_commands.get_item_by_id(id)
            # print(item.id)
            if lang == "ru":
                # print(item.name_ru)
                items_keyboard.add(types.InlineKeyboardButton(item.name_ru, callback_data=f"{item.id}"))
            elif lang == "en":
                items_keyboard.add(types.InlineKeyboardButton(item.name_en, callback_data=f"{item.id}"))
            elif lang == "uz":
                items_keyboard.add(types.InlineKeyboardButton(item.name_uz, callback_data=f"{item.id}"))

        # await query.message.edit_reply_markup(reply_markup=items_keyboard)
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=items_keyboard)
        await Admin.order_remove_item.set()
    elif query.data == "courier_set":
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
        toxt = "\n<i><b>Статус: %s</b></i>\n\n" % status
        text = txt + toxt

        select_courier_keyboard = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
        couriers_list = await quick_commands.select_all_couriers()
        print(couriers_list)
        # print(order.items)

        for i in couriers_list:
            user = await quick_commands.select_user(i)

            courier_info = f"{user.number} {user.name}"
            # print(item.id)
            select_courier_keyboard.add(types.InlineKeyboardButton(courier_info, callback_data=f"{user.id}"))

        if order.type_delivery == 1:
            tix_t = "Какого курьера назначить?\n\n"
            text += tix_t
            await query.message.edit_text(text, parse_mode="HTML", reply_markup=select_courier_keyboard)
            await Admin.order_set_courier.set()
        else:
            tix_t = "Невозможно назначить курьера на самовывоз\n\n"
            text += tix_t
            await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
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
            await dp.bot.send_message(order.user_id, msg_f_u, parse_mode="HTML")
        await quick_commands.change_status(order_id, 6)
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
    elif query.data == "back":
        await query.message.delete()
        orders = await quick_commands.select_all_orders()
        count_all = 0  # Счетчик всех заказов
        count_not_all = 0
        for i in orders:
            if i.status != 6:
                count_not_all += 1
                if i.status == 5:
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
        kikir = "\n\n\n<b>Всего заказов (не считая отмененных)- %s</b>\n<b>Всего заказов (не считая отмененных и доставленных) - %s</b>" % (
            count_not_all, count_all)
        txt = koker + text + kikir
        lilo = await dp.bot.send_message(query.from_user.id, "Загрузка...", reply_markup=ReplyKeyboardRemove())
        await lilo.delete()
        msg = await dp.bot.send_message(query.from_user.id, txt, parse_mode="HTML", reply_markup=orders_a)
        #  msg = await message.answer(txt, reply_markup=orders_a)
        await state.update_data(msg_id=msg.message_id)
        await Admin.orders.set()


# Хендлер обработки предмета на добавление в заказ и вывод клавиатуры с количеством
@dp.callback_query_handler(state=Admin.order_add_item)
async def process_order_add_action(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    status = ""
    lang = await quick_commands.select_language(user_id)
    items_list = await quick_commands.select_all_items()
    await state.update_data(item_id=query.data)
    item_id = int(query.data)
    async with state.proxy() as data:
        order_id = data["order_id"]

        order_id = int(order_id)
        txt = await quick_commands.admin_text(order_id, lang)
        i_id = data["item_id"]
    order = await quick_commands.select_order_by_id(order_id)
    if item_id in items_list:
        item = await quick_commands.get_item_by_id(item_id)
        item_name = ""
        if lang == "ru":
            item_name = item.name_ru
        elif lang == "en":
            item_name = item.name_en
        elif lang == "uz":
            item_name = item.name_uz
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
        toxt = "\n<i><b>Статус: %s</b></i>\n\n" % status
        text = txt + toxt
        tix_t = "Выбран товар: <b>%s</b>. \nВыберите количество из списка ниже.\n\n" % item_name
        text += tix_t
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_by_id_quantity)
        await Admin.order_add_item_quantity.set()


# Хендлер обработки предмета на удаление из заказа и вывод клавиатуры с количеством
@dp.callback_query_handler(state=Admin.order_remove_item)
async def process_order_remove_action(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    status = ""
    lang = await quick_commands.select_language(user_id)
    await state.update_data(item_id=query.data)
    item_id = int(query.data)
    async with state.proxy() as data:
        order_id = data["order_id"]

        order_id = int(order_id)
        txt = await quick_commands.admin_text(order_id, lang)
        i_id = data["item_id"]
    order = await quick_commands.select_order_by_id(order_id)
    items_list = await quick_commands.get_items_in_order(order.id)
    if item_id in items_list:
        item = await quick_commands.get_item_by_id(item_id)
        item_name = ""
        if lang == "ru":
            item_name = item.name_ru
        elif lang == "en":
            item_name = item.name_en
        elif lang == "uz":
            item_name = item.name_uz
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
        toxt = "\n<i><b>Статус: %s</b></i>\n\n" % status
        text = txt + toxt
        tix_t = "Выбран товар: <b>%s</b>. \nВыберите количество из списка ниже.\n\n" % item_name
        text += tix_t
        number = order.items[f'{item_id}']
        # print(number)
        quan = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
        rem = number % 3
        rang = range(1, number, 3)
        del_e = int(number / 3) - 1
        count = 0
        for i in rang:
            if count <= del_e:
                count += 1
                quan.row(types.InlineKeyboardButton(text=f"{i}", callback_data=f"{i}"),
                         types.InlineKeyboardButton(text=f"{i + 1}", callback_data=f"{i + 1}"),
                         types.InlineKeyboardButton(text=f"{i + 2}", callback_data=f"{i + 2}"))
        if rem % 2 == 0:
            for k in range(0, rem, 2):
                quan.add(
                    types.InlineKeyboardButton(text=f"{number - rem + k + 1}", callback_data=f"{number - rem + k + 1}"),
                    types.InlineKeyboardButton(text=f"{number - rem + k + 2}", callback_data=f"{number - rem + k + 2}"))
        if rem % 2 != 0:
            for k in range(0, rem, 1):
                quan.add(
                    types.InlineKeyboardButton(text=f"{number - rem + k + 1}", callback_data=f"{number - rem + k + 1}"))

        await query.message.edit_text(text, parse_mode="HTML", reply_markup=quan)
        await Admin.order_remove_item_quantity.set()


# Хендлер обработки количества выбранного товара и обновление сообщения с содержимым
@dp.callback_query_handler(state=Admin.order_add_item_quantity)
async def process_order_item_action(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    lang = await quick_commands.select_language(user_id)

    quantity = int(query.data)
    async with state.proxy() as data:
        order_id = data["order_id"]
        order_id = int(order_id)
        i_id = data["item_id"]
    order = await quick_commands.select_order_by_id(order_id)
    item_name = await quick_commands.select_item_name(int(i_id), lang)
    if quantity in range(26):
        order_items = order.items
        # print(order.items)
        try:
            order_items[i_id] += quantity
        except KeyError:
            order_items[i_id] = quantity
        # print(order_items)
        item = await quick_commands.get_item_by_id(int(i_id))
        price = item.price * quantity
        # print(price)
        await quick_commands.update_order_price(order_id, price, "add")
        await quick_commands.update_order_items(order_id, order_items)
        id = order_id
        try:
            id = int(id)
            await state.update_data(order_id=id)  # Записываем id заказа в state
            order = await quick_commands.select_order_by_id(id)
            txt = await quick_commands.admin_text(order.id, lang)
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
            txt += "\n\n<b>Товар: <i>%s %sшт</i> добавлен в корзину.\n\n\nВыберите действие</b>"
            txt = txt % (item_name, query.data)
            await query.message.edit_text(txt, parse_mode="HTML", reply_markup=order_info)
            # await dp.bot.send_message(message.from_user.id, txt, parse_mode="HTML", reply_markup=order_info)

            await Admin.order_by_ID_action.set()

        except Exception as e:
            error = "Заказа с таким номером не существует"
            await dp.bot.send_message(user_id, error)


# Хендлер обработки количества выбранного товара для удаления и обновление сообщения с содержимым
@dp.callback_query_handler(state=Admin.order_remove_item_quantity)
async def process_order_itemr_action(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    lang = await quick_commands.select_language(user_id)

    quantity = int(query.data)
    async with state.proxy() as data:
        order_id = data["order_id"]
        order_id = int(order_id)
        i_id = data["item_id"]
    order = await quick_commands.select_order_by_id(order_id)
    item_name = await quick_commands.select_item_name(int(i_id), lang)
    if quantity in range(1, order.items[i_id] + 1):
        order_items = order.items
        # print(order.items)
        print(order_items)
        order_items[i_id] -= quantity
        if order.items[i_id] == 0:
            del order.items[str(i_id)]

        # print(order_items)
        item = await quick_commands.get_item_by_id(int(i_id))
        price = item.price * quantity
        print(order_items)
        # print(price)
        await quick_commands.update_order_price(order_id, price, "remove")
        await quick_commands.update_order_items(order_id, order_items)
        id = order_id
        try:
            id = int(id)
            await state.update_data(order_id=id)  # Записываем id заказа в state
            order = await quick_commands.select_order_by_id(id)
            txt = await quick_commands.admin_text(order.id, lang)
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
            txt += "\n\n<b>Товар: <i>%s %sшт</i> удален из корзины.\n\n\nВыберите действие</b>"
            txt = txt % (item_name, query.data)
            await query.message.edit_text(txt, parse_mode="HTML", reply_markup=order_info)
            # await dp.bot.send_message(message.from_user.id, txt, parse_mode="HTML", reply_markup=order_info)

            await Admin.order_by_ID_action.set()

        except Exception as e:
            error = "Заказа с таким номером не существует"
            await dp.bot.send_message(user_id, error)


# Хендлер установки курьера на заказ и отправки нужной информации курьеру
@dp.callback_query_handler(state=Admin.order_set_courier)
async def process_order_add_action(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    async with state.proxy() as data:
        order_id = data["order_id"]
        order_id = int(order_id)
    txt = await quick_commands.admin_text(order_id, "ru")
    order = await quick_commands.select_order_by_id(order_id)
    couriers_list = await quick_commands.select_all_couriers()
    courier = query.data
    courier_int = int(courier)
    await quick_commands.set_courier(order_id, courier_int)
    cour = await quick_commands.select_user(courier_int)
    if courier_int in couriers_list:
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
        toxt = "\n<i><b>Статус: %s</b></i>\n\n" % status
        text = txt + toxt
        tix_t = "Курьер <b>%s</b> назначен\n\n" % cour.number
        text += tix_t
        cour_txt = "<i>Вам назначен заказ <b>№%s</b></i>\n\n" % order_id
        # print(items_list)
        # print(order.items)
        us_t = "Курьер с номером <b>%s</b> назначен на Ваш заказ №%s\n\n" % (cour.number, order_id)

        # await query.message.edit_reply_markup(reply_markup=items_keyboard)
        await dp.bot.send_message(order.user_id, us_t, parse_mode="HTML")
        await dp.bot.send_message(courier_int, cour_txt, parse_mode="HTML", reply_markup=order_info)
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
        await Admin.order_by_ID_action.set()
    else:
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
        toxt = "\n<i><b>Статус: %s</b></i>\n\n" % status
        text = txt + toxt
        tix_t = "Такого курьера не существует\n\n"
        text += tix_t

        # print(items_list)
        # print(order.items)

        # await query.message.edit_reply_markup(reply_markup=items_keyboard)
        await query.message.edit_text(text, parse_mode="HTML", reply_markup=order_info)
        await Admin.order_by_ID_action.set()


# Обработка функций по id заказа
@dp.callback_query_handler(state=Admin.order_call)
async def process_call_orders(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'back':
        orders = await quick_commands.select_all_orders()
        count_all = 0  # Счетчик всех заказов
        count_not_all = 0  # Счетчик заказов
        for i in orders:
            if i.status != 6:
                count_not_all += 1
                if i.status != 5:
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
        kikir = "\n\n\n<b>Всего заказов (не считая отмененных)- %s</b>\n<b>Всего заказов (не считая отмененных и доставленных)- %s</b>" % (
            count_not_all, count_all)
        txt = koker + text + kikir
        await dp.bot.delete_message(query.message.chat.id, query.message.message_id)  # Удаляем смс
        msg = await dp.bot.send_message(query.message.chat.id, txt, reply_markup=orders_a)
        # msg = await message.answer(txt, reply_markup=orders_a)
        await state.update_data(msg_id=msg.message_id)
        await Admin.orders.set()
    else:

        user_id = query.from_user.id
        lang = await quick_commands.select_language(user_id)
        id = int(query.data)

        # id = int(id)
        await state.update_data(order_id=id)  # Записываем id заказа в state
        order = await quick_commands.select_order_by_id(id)
        txt = await quick_commands.admin_text(id, lang)
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
        txt += "\n<i><b>Статус: %s</b></i>" % status
        # await state.update_data()
        await query.message.delete()
        await dp.bot.send_message(user_id, txt, parse_mode="HTML", reply_markup=order_info)

        await Admin.order_by_ID_action.set()
