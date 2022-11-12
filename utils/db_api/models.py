class User:
    users = {}

    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.allowed = True

    @classmethod
    def get(cls, telegram_id):
        return cls.users.get(telegram_id)

    @classmethod
    def create(cls, telegram_id):
        user = User(telegram_id)
        cls.users[telegram_id] = user
        return user

    @classmethod
    def get_or_create(cls, telegram_id):
        user = cls.get(telegram_id)
        if user is None:
            user = cls.create(telegram_id)
        return user

    def block(self):
        self.allowed = False

    def allow(self):
        self.allowed = True


class Order:
    orders = {}

    def __init__(self, order_id):
        self.order_id = order_id
        self.allowed = True

    @classmethod
    def get(cls, order_id):
        return cls.orders.get(order_id)

    @classmethod
    def create(cls, order_id):
        order = Order(order_id)
        cls.orders[order_id] = order
        return order

    @classmethod
    def get_or_create(cls, order_id):
        order = cls.get(order_id)
        if order is None:
            order = cls.create(order_id)
        return order

class Item:
    items = {}

    def __init__(self, item_id):
        self.item_id = item_id
        self.allowed = True

    @classmethod
    def get(cls, item_id):
        return cls.items.get(item_id)

    @classmethod
    def create(cls, item_id):
        item = Item(item_id)
        cls.items[item_id] = item
        return item

    @classmethod
    def get_or_create(cls, item_id):
        item = cls.get(item_id)
        if item is None:
            item = cls.create(item_id)
        return item


class Cart:
    carts = {}

    def __init__(self, cart_id):
        self.cart_id = cart_id
        self.allowed = True

    @classmethod
    def get(cls, cart_id):
        return cls.carts.get(cart_id)

    @classmethod
    def create(cls, cart_id):
        cart = Cart(cart_id)
        cls.carts[cart_id] = cart
        return cart

    @classmethod
    def get_or_create(cls, cart_id):
        cart = cls.get(cart_id)
        if cart is None:
            cart = cls.create(cart_id)
        return cart

class Branch:
    branches = {}

    def __init__(self, branch_id):
        self.branch_id = branch_id
        self.allowed = True

    @classmethod
    def get(cls, branch_id):
        return cls.branches.get(branch_id)

    @classmethod
    def create(cls, branch_id):
        branch = Branch(branch_id)
        cls.branches[branch_id] = branch
        return branch

    @classmethod
    def get_or_create(cls, branch_id):
        branch = cls.get(branch_id)
        if branch is None:
            branch = cls.create(branch_id)
        return branch