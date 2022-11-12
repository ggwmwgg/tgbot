from typing import List

from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User





# Добавить пользователя
async def add_user(id: int, name: str, lang_user: str, number: str, username: str, referral: int):
    try:
        user = User(id=id, name=name, lang_user=lang_user, number=number, username=username, referral=referral)
        await user.create()

    except UniqueViolationError:
        pass


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


# Выбрать пользователя по номеру
async def select_user_by_number(number: str):
    user = await User.query.where(User.number == number).gino.first()
    return user


# Установить права админа (1 = админ, 2 = оператор, 3 = доставка)
async def set_rights(id: int, is_admin: int):
    user = await User.get(id)
    await user.update(is_admin=is_admin).apply()

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



