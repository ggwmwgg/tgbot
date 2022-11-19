import gettext
_ = gettext.gettext

# orders.py

button_o_txt = _("Order №%s from %s") # Заказ №%s от %s
orders_view_txt = _("<b>List of last 10 orders</b>\n\nSelect an order to view:") # <b>Список последних 10 заказов</b>\n\nВыберите заказ для просмотра:
orders_main_menu_txt = _("Main menu") # Главное меню
orders_status_txt = _("\n<i><b>Order status: %s</b></i>") # "\n<i><b>Статус: %s</b></i>"
orders_not_found_txt = _("Order not found") # Заказ не найден
back_eng = _("Back") # Назад
orders_status_1 = _("Awaiting confirmation") # В обработке
orders_status_2 = _("Confirmed") # Подтвержден
orders_status_3 = _("Cooking") # Приготовление
orders_status_4 = _("Delivery") # Доставка
orders_status_5 = _("Delivered") # Доставлен
orders_status_6 = _("Cancelled") # Отменен
