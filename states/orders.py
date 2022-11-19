from aiogram.dispatcher.filters.state import StatesGroup, State


# Создаем группу состояний Order - для заказа.

class Reg(StatesGroup):
    # Создаем состояние в этой группе. Называйте каждое состояние соответственно его назначению.
    # В данном случае Q1 - question 1, то есть первый вопрос. У вас это может быть по-другому
    language = State()
    name = State()
    nn = State()
    code = State()


class Order(StatesGroup):
    d_or_d = State()
    asklocation = State()
    location_drive = State()
    location_drive_another = State()
    location_delivery = State()
    location_delivery_another = State()
    menu = State()
    menu_subcat = State()
    menu_item = State()
    menu_cart = State()
    menu_confirm = State()
    menu_add_comment = State()
    menu_confirm_payment = State()
    menu_confirmed = State()


class Settings(StatesGroup):
    settings = State()
    number = State()
    number_code = State()
    language = State()
    name = State()


class Admin(StatesGroup):
    a_main = State()
    users = State()
    user_info_by_number = State()
    user_info_by_id = State()
    user_main_info = State()
    user_main_info_name = State()
    user_main_info_lang = State()
    user_main_info_number = State()
    user_main_info_cashback = State()
    user_main_info_ban = State()
    user_main_info_rights = State()
    orders = State() # Заказы
    order_by_ID = State() # Заказ по ID
    order_by_ID_action = State() # Действия с заказом
    order_by_num = State() # Список заказов по номеру
    order_a_by_num = State() # Список активных заказов по номеру
    order_a_by_fil = State() # Список активных заказов по филиалу
    order_by_fil = State() # Список заказов по филиалу
    order_add_item = State() # Добавление товара
    order_remove_item = State() # Удаление товара
    order_add_item_quantity = State() # Добавление количества товара
    order_remove_item_quantity = State() # Удаление позиции
    order_set_courier = State() # Установка курьера
    order_call = State() # Обработка коллбеков ID заказа для дальнейшего направления на order_by_ID_action
    cats = State()
    items = State()

