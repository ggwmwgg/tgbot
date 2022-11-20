from typing import List

from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User
from utils.db_api.schemas.order import Order
from utils.db_api.schemas.item import Item
from utils.db_api.schemas.cart import Cart
from utils.db_api.schemas.branches import Branch
from utils.misc import get_address_from_coords
from data.config import cashback


# Добавить заказ
async def add_order(user_id: int, p_type: str, items: dict, comment: str, total_price: int, delivery_price: int, cashback: int, type_delivery: int, is_paid: int, lon: float, lat: float, branch: str):
    try:
        order = Order(user_id=user_id, p_type=p_type,items=items, comment=comment, total_price=total_price,delivery_price=delivery_price, cashback=cashback, type_delivery=type_delivery, is_paid=is_paid, lon=lon, lat=lat, branch=branch)
        await order.create()

    except UniqueViolationError:
        pass

# Добавить пользователя
async def add_user(id: int, name: str, lang_user: str, number: str, username: str, referral: int):
    try:
        user = User(id=id, name=name, lang_user=lang_user, number=number, username=username, referral=referral)
        await user.create()

    except UniqueViolationError:
        pass

# Добавить товар
async def add_item(name_ru: str, name_uz: str, name_en: str, d_ru: str, d_uz: str, d_en: str, price: int,
                   cat_ru: str, cat_uz: str, cat_en: str, photo: str,):
    try:
        item = Item(name_ru=name_ru, name_uz=name_uz, name_en=name_en, d_ru=d_ru, d_uz=d_uz, d_en=d_en, price=price,
                    cat_ru=cat_ru, cat_uz=cat_uz, cat_en=cat_en, photo=photo)
        await item.create()

    except UniqueViolationError:
        pass


# Добавить филиал
async def add_branch(name: str, location: dict, contacts: str):
    try:
        branch = Branch(name=name, location=location, contacts=contacts)
        await branch.create()

    except UniqueViolationError:
        pass


# Выбрать товар по его id в корзине пользователя
async def select_cart_by_itemid(user_id: int,id: int):
    cart = await Cart.query.where(Cart.user_id == user_id).where(Cart.item_id == id).gino.first()
    return cart


# Узнать цену товара
async def select_item_price(id: int):
    item = await Item.query.where(Item.id == id).gino.first()
    price = item.price
    return price


# Добавить или обновить товар в корзине пользователя
async def add_or_update_cart(user_id: int, item_id: int, quantity: int, price: int):
    if await select_cart_by_itemid(user_id, item_id):
        cart = await Cart.query.where(Cart.user_id == user_id).where(Cart.item_id == item_id).gino.first()
        quantity = cart.quantity + quantity
        price = cart.price + price
        await cart.update(quantity=quantity, price=price).apply()
    else:
        cart = Cart(user_id=user_id, item_id=item_id, quantity=quantity, price=price)
        await cart.create()


# Выбрать все товары из корзины пользователя
async def select_cart(user_id: int):
    cart = await Cart.query.where(Cart.user_id == user_id).gino.all()
    return cart
# Выбрать всех пользователей
async def select_all_users():
    users = await User.query.gino.all()
    return users

# Выбрать одного пользователя
async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user

# Удалить пользователя
async def delete_user(id: int):
    user = await User.get(id)
    await user.delete()

# Удалить товар из корзины пользователя по его id и id товара
async def delete_cart_by_itemid(user_id: int, id: int):
    cart = await Cart.query.where(Cart.user_id == user_id).where(Cart.item_id == id).gino.first()
    await cart.delete()

# Выбрать пользователя по номеру
async def select_user_by_number(number: str):
    user = await User.query.where(User.number == number).gino.first()
    return user


# Выбрать название товара по id
async def select_item_name(id: int, lang: str):
    if lang == 'ru':
        item = await Item.query.where(Item.id == id).gino.first()
        name = item.name_ru
        return name
    elif lang == 'uz':
        item = await Item.query.where(Item.id == id).gino.first()
        name = item.name_uz
        return name
    elif lang == 'en':
        item = await Item.query.where(Item.id == id).gino.first()
        name = item.name_en
        return name

# Установить права админа (1 = админ, 2 = оператор, 3 = доставка)
async def set_rights(id: int, is_admin: int):
    user = await User.get(id)
    await user.update(is_admin=is_admin).apply()


# Получить список товаров из корзины пользователя
async def get_cart_list(user_id: int, lang: str):
    cart = await select_cart(user_id)
    list = []
    for i in cart:
        item = await select_item_name(i.item_id, lang)
        list.append(item + " ❌")
    return list

async def get_cart_list_nox(user_id: int, lang: str):
    cart = await select_cart(user_id)
    list = []
    for i in cart:
        item = await select_item_name(i.item_id, lang)
        list.append(item)
    return list

# Проверить права пользователя
async def check_rights(id: int):
    user = await User.query.where(User.id == id).gino.first()
    rights = user.is_admin
    return rights

# Выбрать имя пользователя
async def select_name(id: int):
    user = await User.query.where(User.id == id).gino.first()
    name = user.name
    return name

# Выбрать номер пользователя
async def select_number(id: int):
    user = await User.query.where(User.id == id).gino.first()
    num = user.number
    return num


# Установить cashback
async def set_cashback(id: int, cashback: int):
    user = await User.get(id)
    await user.update(cashback=cashback).apply()

# Выбрать язык пользователя
async def select_language(id: int):
    user = await User.query.where(User.id == id).gino.first()
    lang = user.lang_user
    return lang

# Посчитать количество пользователей
async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total

# Проверить наличие бана (True = да, False = нет)
async def check_ban(id: int):
    user = await User.query.where(User.id == id).gino.first()
    ban = user.is_banned
    if ban == 1:
        return True
    else:
        return False


# Проверить бан с ответом да или нет для инфо
async def check_ban_info(id: int):
    user = await User.query.where(User.id == id).gino.first()
    ban = user.is_banned
    if ban == 1:
        return "Да"
    else:
        return "Нет"

# Проверить наличие прав для инфо
async def check_rights_info(id: int):
    user = await User.query.where(User.id == id).gino.first()
    rights = user.is_admin
    if rights == 1:
        return "Админ"
    elif rights == 2:
        return "Оператор"
    elif rights == 3:
        return "Доставка"
    else:
        return "Пользователь"

# Забанить пользователя
async def ban_user(id: int):
    user = await User.get(id)
    await user.update(is_banned=1).apply()

# Разбанить пользователя
async def unban_user(id: int):
    user = await User.get(id)
    await user.update(is_banned=0).apply()

# Обновить номер пользователя
async def update_user_number(id, number):
    user = await User.get(id)
    await user.update(number=number).apply()

# Обновить язык пользователя
async def update_user_language(id, lang_user):
    user = await User.get(id)
    await user.update(lang_user=lang_user).apply()

# Обновить имя пользователя
async def update_user_name(id, name):
    user = await User.get(id)
    await user.update(name=name).apply()

# Выбрать id последнего заказа по id пользователя
async def select_order(id: int):
    order = await Order.query.where(Order.user_id == id).order_by(Order.id.desc()).gino.first()
    # order = await Order.query.where(Order.id == id).gino.first()
    return order.id

# Проверить есть ли больше одного доставленного или двух активных неоплаченных заказов у пользователя
async def check_debt_active(id: int):
    count_active = 0
    for i in await Order.query.where(Order.user_id == id).gino.all():
        if i.is_paid == 0:
            if i.status == 1 or i.status == 2 or i.status == 3 or i.status == 4:
                count_active += 1
            if i.status == 5:
                return True
        if i.is_paid == 1:
            pass
        if count_active >= 2:
            return True
    return False




# Проверить количество активных неоплаченных заказов
async def count_active_orders(id: int):
    count_active = 0
    for i in await Order.query.where(Order.user_id == id).gino.all():
        if i.is_paid == 0:
            if i.status == 1 or i.status == 2 or i.status == 3 or i.status == 4:
                count_active += 1


    return count_active

# Изменить статус заказа (1 = активный, 2 = подтвержден, 3 = приготовление, 4 = приготовлен, 5 = доставка, 6 = доставлен, 7 = отменен)
async def change_status(id: int, status: int):
    order = await Order.get(id)
    await order.update(status=status).apply()

# Проверить оплачен ли заказ (1 = да, 0 = нет)
async def payment_status(id: int):
    order = await Order.get(id)
    return order.is_paid

# Изменить статус оплаты заказа (1 = да, 0 = нет)
async def change_payment_status(id: int, is_paid: int):
    order = await Order.get(id)
    await order.update(is_paid=is_paid).apply()

# Проверить статус заказа (1 = активный, 2 = подтвержден, 3 = приготовление, 4 = приготовлен, 5 = доставка, 6 = доставлен, 7 = отменен)
async def check_status(id: int):
    order = await Order.get(id)
    return order.status

# Получаем категории и кнопки
async def get_categories(lang: str) -> List[Item]:
#async def get_categories(lang: str):
    list = []
    if lang == "ru":
        list_lul = ["Оформить заказ 🚚", "Корзина 🛒", "Назад 🔙"]
        list.append(list_lul[0])
        list.append(list_lul[1])
        ru = await Item.query.distinct(Item.cat_ru).gino.all()
        for i in ru:
            list.append(i.cat_ru)
        list.append(list_lul[2])

        return list
    elif lang == "uz":
        list_lul = ["Buyurtma berish 🚚", "Savat 🛒", "Ortga 🔙"]
        list.append(list_lul[0])
        list.append(list_lul[1])
        uz = await Item.query.distinct(Item.cat_uz).gino.all()
        for i in uz:
            list.append(i.cat_uz)
        list.append(list_lul[2])
        return list
    elif lang == "en":
        list_lul = ["Make an order 🚚", "Cart 🛒", "Back 🔙"]
        en = await Item.query.distinct(Item.cat_en).gino.all()
        list.append(list_lul[0])
        list.append(list_lul[1])
        for i in en:
            list.append(i.cat_en)
        list.append(list_lul[2])
        return list

# Получаем товары и кнопки
async def get_subcategories(category: str, lang: str):
    list = []
    if lang == "ru":
        list_lul = ["Оформить заказ 🚚", "Корзина 🛒", "Назад 🔙"]
        list.append(list_lul[0])
        list.append(list_lul[1])
        ru = await Item.query.where(Item.cat_ru == category).order_by(Item.id.desc()).gino.all()
        for i in ru:
            list.append(i.name_ru)
        list.append(list_lul[2])
        return list
    elif lang == "uz":
        list_lul = ["Buyurtma berish 🚚", "Savat 🛒", "Ortga 🔙"]
        list.append(list_lul[0])
        list.append(list_lul[1])
        uz = await Item.query.where(Item.cat_uz == category).order_by(Item.id.desc()).gino.all()
        for i in uz:
            list.append(i.name_uz)
        list.append(list_lul[2])
        return list
    elif lang == "en":
        list_lul = ["Make an order 🚚", "Cart 🛒", "Back 🔙"]
        en = await Item.query.where(Item.cat_en == category).order_by(Item.id.desc()).gino.all()
        list.append(list_lul[0])
        list.append(list_lul[1])
        for i in en:
            list.append(i.name_en)
        list.append(list_lul[2])
        return list


# Получаем только список категорий
async def get_only_categories(lang) -> List[Item]:
#async def get_categories(lang: str):
    list = []
    if lang == "ru":
        ru = await Item.query.distinct(Item.cat_ru).gino.all()
        for i in ru:
            list.append(i.cat_ru)
        return list
    elif lang == "uz":
        uz = await Item.query.distinct(Item.cat_uz).gino.all()
        for i in uz:
            list.append(i.cat_uz)
        return list
    elif lang == "en":
        en = await Item.query.distinct(Item.cat_en).gino.all()
        for i in en:
            list.append(i.cat_en)
        return list

# Получаем только список товаров
async def get_only_subcategories(category, lang) -> List[Item]:
    list = []
    if lang == "ru":
        ru = await Item.query.where(Item.cat_ru == category).order_by(Item.id.desc()).gino.all()
        for i in ru:
            list.append(i.name_ru)
        return list
    elif lang == "uz":
        uz = await Item.query.where(Item.cat_uz == category).order_by(Item.id.desc()).gino.all()
        for i in uz:
            list.append(i.name_uz)
        return list
    elif lang == "en":
        en = await Item.query.where(Item.cat_en == category).order_by(Item.id.desc()).gino.all()
        for i in en:
            list.append(i.name_en)
        return list


# Получить товар по названию
async def get_item_by_name(name: str, lang: str) -> Item:
    if lang == "ru":
        return await Item.query.where(Item.name_ru == name).gino.first()
    elif lang == "uz":
        return await Item.query.where(Item.name_uz == name).gino.first()
    elif lang == "en":
        return await Item.query.where(Item.name_en == name).gino.first()

# Получить товар по id
async def get_item_by_id(id: int) -> Item:
    return await Item.query.where(Item.id == id).gino.first()

# Очистить корзину по id пользователя
async def clear_cart_by_user_id(user_id: int):
    await Cart.delete.where(Cart.user_id == user_id).gino.status()

# Обновить тип последнего заказа пользователя 0 = no, 1 = delivery, 2 = pickup
async def update_last_order_type(user_id: int, last: int):
    await User.update.values(last=last).where(User.id == user_id).gino.status()


# Обновить адрес последнего заказа пользователя
async def update_last_order_coords(user_id: int, lat: float, long: float):
    await User.update.values(latitude=lat).where(User.id == user_id).gino.status()
    await User.update.values(longitude=long).where(User.id == user_id).gino.status()

# Обновить стоимость доставки
async def update_delivery_price(user_id: int, price: int):
    await User.update.values(last_delivery=price).where(User.id == user_id).gino.status()

# Обновить последний филиал пользователя
async def update_last_branch(user_id: int, branch: str):
    await User.update.values(branch=branch).where(User.id == user_id).gino.status()

# Проверить есть ли последние данные по доставке у пользователя, если нет, то вернуть False:
async def check_last_order_data(user_id: int) -> bool:
    user = await select_user(user_id)
    if user.last == 0:
        return False
    elif user.latitude == 0:
        return False
    elif user.longitude == 0:
        return False
    elif user.branch == 'Null':
        return False
    else:
        return True

# Получить список администраторов
async def get_admins() -> List[User]:
    admin = await User.query.where(User.is_admin == 1).gino.all()
    admins = []
    for i in admin:
        admins.append(i.id)
    return admins

async def block_user(user: User):
    user.allowed = False

async def unblock_user(user: User):
    user.allowed = True


# Выбрать последний заказ пользователя по id пользователя
async def select_last_order_by_id(user_id: int) -> Order:
    return await Order.query.where(Order.user_id == user_id).order_by(Order.id.desc()).gino.first()

# Выбрать операторов и администраторов
async def select_operators() -> List[User]:
    list = []
    operators = await User.query.where(User.is_admin == 2).gino.all()
    admins = await User.query.where(User.is_admin == 1).gino.all()
    for i in operators:
        list.append(i.id)
    for i in admins:
        list.append(i.id)
    return list

# Выбрать все заказы
async def select_all_orders():
    return await Order.query.gino.all()

# Выбрать все активные заказы
async def select_all_active_orders():
    return await Order.query.where(Order.status == 1).gino.all()

# Выбрать все филиалы
async def select_all_branches():
    return await Branch.query.gino.all()

# Выбрать все филиалы списком
async def select_all_branches_list() -> List[Branch]:
    list = []
    for i in await select_all_branches():
        list.append(i.name)
    return list

# Выбрать все активные заказы по id пользователя
async def select_all_active_orders_by_id(user_id: int):
    return await Order.query.where(Order.status == 1).where(Order.user_id == user_id).gino.all()

# Выбрать все заказы по id пользователя
async def select_all_orders_by_id(user_id: int):
    return await Order.query.where(Order.user_id == user_id).gino.all()

# Вернуть список активных заказов по названию филиала
async def select_active_orders_by_branch(branch: str):
    return await Order.query.where(Order.branch == branch).where(Order.status == 1).gino.all()

# Вернуть список заказов по названию филиала
async def select_orders_by_branch(branch: str):
    return await Order.query.where(Order.branch == branch).gino.all()

# Выбрать заказ по id
async def select_order_by_id(id: int) -> Order:
    return await Order.query.where(Order.id == id).gino.first()

# Получить список всех товаров
async def select_all_items() -> List[Item]:
    list = []
    for i in await Item.query.gino.all():
        list.append(i.id)
    return list

# Обновить список товаров в заказе
async def update_order_items(order_id: int, items: dict):
    await Order.update.values(items=items).where(Order.id == order_id).gino.status()

# Обновить цену заказа
async def update_order_price(order_id: int, price: int, do: str):
    order = await select_order_by_id(order_id)
    order_price = 0
    if do == 'add':
        order_price = order.total_price + price
    elif do == 'remove':
        order_price = order.total_price - price
    await Order.update.values(total_price=order_price).where(Order.id == order_id).gino.status()

# Вывод текста для админки
async def admin_text(order_id: int, lang: str) -> str:
    order = await select_order_by_id(order_id)
    txt = "<b>Заказ №%s</b>\n\n" % order.id
    type = ""
    kok = ""
    if order.type_delivery == 1:  # Если доставка
        type = "Доставка"
        coords = f"{order.lon},{order.lat}"
        # print(coords)
        adress = get_address_from_coords(coords)
        if order.courier_id == 0:
            courier = "Не назначен"
        else:
            courier = await select_user(order.courier_id)
            courier = f'{courier.name} {courier.number}'
        kok = "Адрес: %s\nКурьер %s" % (adress[21:], courier)
    elif order.type_delivery == 2:  # Если самовывоз
        type = "Самовывоз"
        kok = "Филиал: %s" % order.branch

    txt += "Тип : %s\n%s\n" % (type, kok)
    number = await select_number(order.user_id)
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

        name = await select_item_name(int(i), lang)
        # print(name)
        price = await select_item_price(int(i))
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
    return txt

# Получить список id товаров в заказе
async def get_items_in_order(order_id: int) -> List[int]:
    order = await select_order_by_id(order_id)
    items = order.items
    list = []
    for i, q in items.items():
        list.append(int(i))
    return list

# Выбрать id всех курьеров
async def select_all_couriers() -> List[User]:
    list = []
    for i in await User.query.where(User.is_admin == 3).gino.all():
        list.append(i.id)
    return list


# Назначить курьера на заказ
async def set_courier(order_id: int, courier_id: int):
    await Order.update.values(courier_id=courier_id).where(Order.id == order_id).gino.status()


# Добавить 1 к количеству заказов пользователя
async def add_order_to_user(user_id: int):
    user = await select_user(user_id)
    await User.update.values(orders_no=user.orders_no + 1).where(User.id == user_id).gino.status()

# Удалить 1 из количества заказов пользователя
async def remove_order_from_user(user_id: int):
    user = await select_user(user_id)
    await User.update.values(orders_no=user.orders_no - 1).where(User.id == user_id).gino.status()

# Проверить есть ли пользователи с таким номером
async def check_number(number: str) -> bool:
    if await User.query.where(User.number == number).gino.first():
        return True
    else:
        return False

# Установить cashback пользователю
async def set_cashback_to_user(user_id: int, order_id: int):
    user = await select_user(user_id)
    order = await select_order_by_id(order_id)
    await User.update.values(cashback=user.cashback + order.cashback).where(User.id == user_id).gino.status()

# Удалить cashback пользователю
async def remove_cashback_from_user(user_id: int, order_id: int):
    user = await select_user(user_id)
    order = await select_order_by_id(order_id)
    await User.update.values(cashback=user.cashback - order.cashback).where(User.id == user_id).gino.status()


# Выбрать все заказы курьера
async def select_all_orders_courier(courier_id: int):
    return await Order.query.where(Order.courier_id == courier_id).gino.all()





