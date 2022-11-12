from aiogram.dispatcher.filters.state import StatesGroup, State


# Создаем группу состояний Order - для заказа.

class Reg(StatesGroup):
    # Создаем состояние в этой группе. Называйте каждое состояние соответственно его назначению.
    # В данном случае Q1 - question 1, то есть первый вопрос. У вас это может быть по-другому
    language = State()
    name = State()
    nn = State()
    code = State()




