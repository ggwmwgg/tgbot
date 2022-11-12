# import csv
# data = ["This", "is", "a", "Test"]
# with open('../img/example.csv', 'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(data)


import asyncio

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from data import config
from utils.db_api import quick_commands
from utils.db_api.db_gino import db
from loader import dp, bot
from typing import List
from data import lang_en

from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User
from utils.db_api.schemas.order import Order
from utils.db_api.schemas.item import Item
from utils.db_api.schemas.cart import Cart


# from aiogram.utils.


async def test():
    await db.set_bind(config.POSTGRES_URI)
    # await db.gino.drop_all()
    # await db.gino.create_all()

    # print("Добавляем пользователей")
    # await quick_commands.add_user(4574, "One", "ru", "123", "one", 1)
    # await quick_commands.add_user(2, "Vasya", "ru", "123", "one", 2)
    # await quick_commands.add_user(3, "1", "ru", "123", "one", 3)
    # print("Готово")
    #
    #
    # print("Добавляем заказы")
    # await quick_commands.add_order(4574, "cash", "1", 100)
    # await quick_commands.add_order(4574, "payme", "2", 250000)
    # await quick_commands.add_order(4574, "payme", "3", 25123)
    # await quick_commands.add_order(4574, "payme", "4", 333333)
    # print("Готово")

    # users = await quick_commands.select_all_users()
    # print(f"Получил всех пользователей: {users}")

    count_users = await quick_commands.count_users()
    print(f"Всего пользователей: {count_users}")

    print("Добавляю товары")  # name_ru, name_uz, name_en, d_ru, d_uz, d_en, price, cat_ru, cat_uz, cat_en, photo
    # Бургеры
    await quick_commands.add_item("Чизбургер", "Чизбургер", "Cheeseburger",
                                  "Пряный горчичный соус, кетчуп, сочные стрипсы в оригинальной панировке, лук, сыр Чеддер, огурцы на пшеничной булочке с кукурузной посыпкой.",
                                  "Жўхори талқони сепилган булочка ичига солинган оригинал панировкага буланган сархил стрипс, пиёз, Чеддер пишлоғи, бодринг, хуштаьм ханталли соус ва кетчуп.",
                                  "Herby mustard sauce, ketchup, juicy chicken strips in original breading, onion, cheddar cheese, pickles on a corn bun.",
                                  15000, "Бургеры", "Сендвичлар", "Burgers", "./data/img/cheeseburger.png")  # Чизбургер
    await quick_commands.add_item("Чизбургер Де Люкс", "Чизбургер Де Люкс", "De Luxe Cheeseburger",
                                  "Пряный горчичный соус, кетчуп, сочное куриное филе в оригинальной панировке, лук, сыр Чеддер, огурцы на пшеничной булочке с кукурузной посыпкой, свежий салат и ломтики помидора.",
                                  "Жўхори талқони сепилган булочка ичига солинган оригинал панировкага буланган сархил гўшт, пиёз, Чеддер пишлоғи, бодринг ва помидор тилимчалари, янги узилган салат барги, хуштаьм ханталли соус ва кетчуп.",
                                  "Herby mustard sauce, ketchup, juicy chicken fillet in original breading, onion, cheddar cheese, pickles on a corn bun with fresh salad and tomatoes.",
                                  18000, "Бургеры", "Сендвичлар", "Burgers",
                                  "./data/img/cheeseburger_dl.png")  # Чизбургер Де Люкс
    await quick_commands.add_item("Шефбургер", "Шефбургер", "Chefburger",
                                  "Попробуйте новый уникальный бургер от шефа! Сочная курица, томаты, свежий салат, соус Цезарь и аппетитная булочка. Такого вы еще не пробовали!",
                                  "Шефнинг шахсан ўзи тайёрлаган янги, ноёб бургерни татиб кўринг! Сархил товуқ гўшти, помидор, янги узилган салат барги, Цезарь соуси ва иштаҳаочар булочка! Бунақасини ҳали татиб кўрмагансиз!",
                                  "Tasty our new unique chef’s burger! Tender creamy sauce, juicy fillet in original breading,  lettuce and tomatoes on a wheat bun with black and white sesame seeds.",
                                  18000, "Бургеры", "Сендвичлар", "Burgers", "./data/img/chefburger.png")  # Шефбургер
    await quick_commands.add_item("Острый Шефбургер", "Аччиқ Шефбургер", "Hot Chefburger",
                                  "Попробуйте новый уникальный бургер от шефа! Острая курочка в панировке Hot&spicy, сочные листья салата, пикантные маринованные огурчики, лук, фирменный соус «Бургер» и булочка с кунжутом. Мммм!",
                                  "Шефнинг шахсан ўзи тайёрлаган янги, ноёб бургерни татиб кўринг! Hot&spicy панировкасига буланган аччиққина товуқ гўшти, янги узилган салат барги, маринадланган ўткир таъмли бодринг, пиёз, фирмали “Бургер” соуси ва кунжутли булочка! ММММ!",
                                  "Tasty our new unique chef’s burger! Hot chicken, fresh salad, onion, sauce Burger, crispy pickles and appetizing bun with black and white sesame seeds.",
                                  18000, "Бургеры", "Сендвичлар", "Burgers",
                                  "./data/img/chefburger_hot.png")  # Шефбургер острый
    await quick_commands.add_item("Биг Сандерс Бургер", "big sanders burger name_uz", "Big Sanders Burger",
                                  "big sanders burger d_ru", "big sanders burger d_uz", "big sanders burger d_en",
                                  34000, "Бургеры", "Сендвичлар", "Burgers",
                                  "./data/img/big_sanders_b.png")  # Биг Сандерс Бургер
    await quick_commands.add_item("Биг Сандерс Бургер острый", "big sanders burger o name_uz", "Hot Big Sanders Burger",
                                  "big sanders burger o d_ru", "big sanders burger o d_uz", "big sanders burger o d_en",
                                  34000, "Бургеры", "Сендвичлар", "Burgers",
                                  "./data/img/big_sanders_b_hot.png")  # Биг Сандерс Бургер острый
    await quick_commands.add_item("Сандерс Бургер", "sanders burger name_uz", "Sanders Burger", "sanders burger d_ru",
                                  "sanders burger d_uz", "sanders burger d_en", 28000, "Бургеры", "Сендвичлар",
                                  "Burgers", "./data/img/sanders_b.png")  # Сандерс Бургер
    await quick_commands.add_item("Сандерс Бургер острый", "sanders burger name_uz", "Hot Sanders Burger",
                                  "sanders burger d_ru", "sanders burger d_uz", "sanders burger d_en", 28000, "Бургеры",
                                  "Сендвичлар", "Burgers",
                                  "./data/img/sanders_b_hot.png")  # Сандерс Бургер острый
    await quick_commands.add_item("Лонгер", "Лонгер", "Longer",
                                  "Сочная курочка, маринованные огурчики и аппетитный соус… мммм! Спешите попробовать!",
                                  "Сархил товуқ гўшти, маринадланган бодринг ва иштаҳаочар соус... мммм! Татиб кўришга шошилинг",
                                  "Juicy chicken, pickles and a tasty sauce... Mmmm! Hurry up to try it!", 12000,
                                  "Бургеры", "Сендвичлар", "Burgers", "./data/img/longer.png")  # Лонгер
    await quick_commands.add_item("Шеф Тауэр", "Шеф Тауэр", "Chief Tower",
                                  "Новинка от Шефа! Нежный сливочный соус Цезарь, сочное филе в оригинальной панировке, румяный хашбраун, ломтик сыра, салат айcберг и помидоры на пшеничной булочке с черно-белым кунжутом.",
                                  "Шефдан янгилик! Ёқимли қаймоқли Цезарь соуси, оригинал толқинда серсув филе, хашбраун, пишлоқ бўлаги, айсберг салати ва помидор, ҳаммаси буғдой булочкаси ичида. ",
                                  "New burger from Chief! Tender creamy sauce Caesar, juicy fillet in original breading, crusty hash brown, slice of cheese, lettuce and tomatoes on a wheat bun with black and white sesame seeds.",
                                  22000, "Бургеры", "Сендвичлар", "Burgers", "./data/img/chief_tower.png")  # Шеф Тауэр
    await quick_commands.add_item("Острый Шеф Тауэр", "Аччиқ Шеф Тауэр", "Hot Cheif Tower",
                                  "Новинка от Шефа! Фирменный соус «Бургер», сочное филе в острой панировке, румяный хашбраун, ломтик сыра, салат айcберг и помидоры на пшеничной булочке с черно-белым кунжутом.",
                                  'Шефдан янгилик! “Бургер” соуси, Hot&spicy толқинда серсув филе, хашбраун, пишлоқ бўлаги, айсберг салати ва помидор, ҳаммаси буғдой булочкаси ичида.',
                                  "New burger from Chief! Sauce Burger, juicy fillet in hot breading, crusty hash brown, slice of cheese, lettuce and tomatoes on a wheat bun with black and white sesame seeds.",
                                  22000, "Бургеры", "Сендвичлар", "Burgers",
                                  "./data/img/chief_tower_hot.png")  # Шеф Тауэр острый

    # Твистеры
    await quick_commands.add_item("Твистер Джуниор", "Твистер Джуниор", "Twister Junior",
                                  "Сырная лепешка, два сочных оригинальных стрипса из куриного филе в панировке, горчица, кетчуп, сыр, маринованные огурчики и лук – идеальный перекус.",
                                  "Пишлоқли кулча, панировкада товуқ лаҳмидан селли оригинал иккита стрипслар, хантал, кетчуп, пишлоқ, маринадланган бодрингчалар ва пиёз - беқиёс тамадди!",
                                  "Cheese tortilla, two juicy chicken strips OR\HS, cheese, mustard, ketchup, pickles and onions – a perfect snack!",
                                  12000, "Твистеры", "Твистерлар", "Twisters",
                                  "./data/img/twister_junior.png")  # Твистер Джуниор
    await quick_commands.add_item("Твистер острый", "Аччиқ Твистер", "Hot Twister",
                                  "Закручен со вкусом! Кусочки нежнейшего куриного филе в хрустящей острой или оригинальной панировке с сочными листьями салата, кусочками помидора и нежным соусом мы завернули в пшеничную лепешку и поджарили в тостере. Тут все и закрутилось!",
                                  "Дид билан ўралган! Биз ўткир, қирсиллама панировкага буланган юмшоқ товуқ гўштини янги узилган салат барги, помидор бўлаклари ва майин соус билан бирга буғдой нонига ўраб, тостерда қизартириб олдик. Ҳамма маза шундан бошланди!",
                                  "Twisted with taste! We wrapped chunks of soft chicken fillet in crispy hot or original coating with luscious lettuce, tomato pieces and tender sauce in wheat tortilla and toasted it. Here’s when the twist stated!",
                                  18000, "Твистеры", "Твистерлар", "Twisters",
                                  "./data/img/twister_hot.png")  # Твистер острый
    await quick_commands.add_item("Твистер оригинальный", "Твистер", "Twister original",
                                  "Закручен со вкусом! Кусочки нежнейшего куриного филе в хрустящей острой или оригинальной панировке с сочными листьями салата, кусочками помидора и нежным соусом мы завернули в пшеничную лепешку и поджарили в тостере. Тут все и закрутилось!",
                                  "Дид билан ўралган! Биз ўткир, қирсиллама панировкага буланган юмшоқ товуқ гўштини янги узилган салат барги, помидор бўлаклари ва майин соус билан бирга буғдой нонига ўраб, тостерда қизартириб олдик. Ҳамма маза шундан бошланди!",
                                  "Twisted with taste! We wrapped chunks of soft chicken fillet in crispy hot or original coating with luscious lettuce, tomato pieces and tender sauce in wheat tortilla and toasted it. Here’s when the twist stated!",
                                  18000, "Твистеры", "Твистерлар", "Twisters",
                                  "./data/img/twister_original.png")  # Твистер оригинал
    await quick_commands.add_item("Твистер Веджи", "Веджи Твистер", "Twister Veggie",
                                  "Закручено со вкусом! Картофельная котлета Хашбраун, ломтик сыра, с сочными листьями салата и кусочками помидора в нежном соусе завернуты в пшеничную лепешку, обжаренную в тостере.",
                                  "Дид билан ўралган! Хашбраун картошка котлетини пишлоқ бўлакчаси, янги узилган салат барги, помидор бўлаклари ва майин соус билан бирга буғдой нонига ўраб, тостерда қизартириб олдик.",
                                  "Twisted with taste! We wrapped hash brown, a slice of cheese with lettuce & fresh tomatoes into tortilla fried at toaster.",
                                  18000, "Твистеры", "Твистерлар", "Twisters",
                                  "./data/img/twister_veggie.png")  # Твистер веджи
    await quick_commands.add_item("Боксмастер", "Боксмастер", "Boxmaster",
                                  "Полная перезагрузка! Мощный заряд энергии в нашем БоксМастере! Сочное куриное филе в оригинальной панировке или острой хрустящей панировке, румяный хашбраун, ломтик сыра, кусочки помидора, салат и нежный соус в горячей лепешке – динамично и со вкусом!",
                                  "Бутунлай янгиланиш! Бизнинг Боксмастерда қудратли қувват учқуни бор! Иссиқ нон ичидаги қип-қизил хашбраун, оригинал ёки ўткир қирсиллама панировкага буланган сархил товуқ гўшти, пишлоқ бўлакчаси, помидор тилимчаси, салат барги ва майин соус – бари жўшқин ихлос билан тайёрланган!",
                                  "Total reload! Heavy energy load in our Boxmaster! Juicy chicken fillet in crispy hot or original coating, crusty hash brown, piece of cheese, tomato chunks, lettuce and tender sauce in hot flat bread — dynamic and tasty!",
                                  23000, "Твистеры", "Твистерлар", "Twisters",
                                  "./data/img/boxmaster.png")  # Боксмастер оригинал
    await quick_commands.add_item("Боксмастер острый", "Аччиқ Боксмастер", "Hot Boxmaster",
                                  "Полная перезагрузка! Мощный заряд энергии в нашем БоксМастере! Сочное куриное филе в оригинальной панировке или острой хрустящей панировке, румяный хашбраун, ломтик сыра, кусочки помидора, салат и нежный соус в горячей лепешке – динамично и со вкусом!",
                                  "Бутунлай янгиланиш! Бизнинг Боксмастерда қудратли қувват учқуни бор! Иссиқ нон ичидаги қип-қизил хашбраун, оригинал ёки ўткир қирсиллама панировкага буланган сархил товуқ гўшти, пишлоқ бўлакчаси, помидор тилимчаси, салат барги ва майин соус – бари жўшқин ихлос билан тайёрланган!",
                                  "Total reload! Heavy energy load in our Boxmaster! Juicy chicken fillet in crispy hot or original coating, crusty hash brown, piece of cheese, tomato chunks, lettuce and tender sauce in hot flat bread — dynamic and tasty!",
                                  23000, "Твистеры", "Твистерлар", "Twisters",
                                  "./data/img/boxmaster_hot.png")  # Боксмастер острый
    await quick_commands.add_item("Сандерс Пита", "Сандерс Питаси", "Sanders Pita",
                                  "Лето уже здесь, а значит, время экспериментировать! Хрустящая пита с травами, свежие овощи, ароматный соус Цезарь и легендарное куриное филе, приготовленное экспертами в курице – эксклюзивно в KFC.",
                                  "Ёз бошланди ва тажриба қилиш учун вақт етиб келди! Товуқ тайёрлаш бўйича мутахассислар томонидан тайёрланган ўтлар, янги сабзавотлар, хушбўй Цезарь соуси ва афсонавий товуқ филесига  бой Сандерс Пита фақат KFC -да.",
                                  "The Summer is here - meaning it's high time you try things out! Crispy pita with herbs, fresh vegetables, fragrant Ceaser sauce and legendary chicken fillet cooked by chicken experts - exclusively in KFC.",
                                  20000, "Твистеры", "Твистерлар", "Twisters",
                                  "./data/img/sanders_pita.png")  # Сандерс Пита

    # Курица
    await quick_commands.add_item("1 Ножка", "1 та оёқ", "1 Drumstick",
                                  'Ножки — самый лакомый кусочек курочки, любимый с самого детства. Теперь у вас есть еще один вкусный повод зайти в KFC: куриные ножки с оригинальным вкусом, приготовленные по секретному рецепту Полковника Сандерса «11 трав и специй». Самая вкусная курочка в КFC!',
                                  'Товуқнинг энг тотли, болаликдан севиб ейиладиган бўлаги унинг оёқларидир. Энди сизда KFCга кириш учун яна битта мазали сабаб бор. Бу – полковник Сандерснинг махфий “11 та гиёҳ ва зиравор” усули бўйича тайёрланган, оригинал таъмли товуқ оёқларидир. Энг мазали товуқ гўшти – KFCда!',
                                  'Drumsticks is the favorite chicken part for everyone since childhood. Now you have one more tasty reason to visit KFC:  new KFC Chicken Drumsticks in original recipe! Enjoy the legendary KFC taste in every bite! Juicy fresh chicken meat hand-breaded and cooked in the restaurant according to Colonel Sanders’ secret recipe of “11 herbs and spices”.',
                                  10000, "Курица", "Товуқ", "Chicken", "./data/img/1_drumstick.png")  # Ножки 1шт
    await quick_commands.add_item("2 Ножки", "2 та оёқ", "2 Drumsticks",
                                  'Ножки — самый лакомый кусочек курочки, любимый с самого детства. Теперь у вас есть еще один вкусный повод зайти в KFC: куриные ножки с оригинальным вкусом, приготовленные по секретному рецепту Полковника Сандерса «11 трав и специй». Самая вкусная курочка в КFC!',
                                  'Товуқнинг энг тотли, болаликдан севиб ейиладиган бўлаги унинг оёқларидир. Энди сизда KFCга кириш учун яна битта мазали сабаб бор. Бу – полковник Сандерснинг махфий “11 та гиёҳ ва зиравор” усули бўйича тайёрланган, оригинал таъмли товуқ оёқларидир. Энг мазали товуқ гўшти – KFCда!',
                                  'Drumsticks is the favorite chicken part for everyone since childhood. Now you have one more tasty reason to visit KFC:  new KFC Chicken Drumsticks in original recipe! Enjoy the legendary KFC taste in every bite! Juicy fresh chicken meat hand-breaded and cooked in the restaurant according to Colonel Sanders’ secret recipe of “11 herbs and spices”.',
                                  18000, "Курица", "Товуқ", "Chicken", "./data/img/2_drumstick.png")  # Ножки 2шт
    await quick_commands.add_item("3 Ножки", "3 та оёқ", "3 Drumsticks",
                                  'Ножки — самый лакомый кусочек курочки, любимый с самого детства. Теперь у вас есть еще один вкусный повод зайти в KFC: куриные ножки с оригинальным вкусом, приготовленные по секретному рецепту Полковника Сандерса «11 трав и специй». Самая вкусная курочка в КFC!',
                                  'Товуқнинг энг тотли, болаликдан севиб ейиладиган бўлаги унинг оёқларидир. Энди сизда KFCга кириш учун яна битта мазали сабаб бор. Бу – полковник Сандерснинг махфий “11 та гиёҳ ва зиравор” усули бўйича тайёрланган, оригинал таъмли товуқ оёқларидир. Энг мазали товуқ гўшти – KFCда!',
                                  'Drumsticks is the favorite chicken part for everyone since childhood. Now you have one more tasty reason to visit KFC:  new KFC Chicken Drumsticks in original recipe! Enjoy the legendary KFC taste in every bite! Juicy fresh chicken meat hand-breaded and cooked in the restaurant according to Colonel Sanders’ secret recipe of “11 herbs and spices”.',
                                  25000, "Курица", "Товуқ", "Chicken", "./data/img/3_drumstick.png")  # Ножки 3шт
    await quick_commands.add_item("Наггетсы 6шт", "Наггетслар 6 та", "Nuggets 6 pcs",
                                  "Попробуйте наггетсы от Сандерса! Это сытно и вкусно! 78 гр",
                                  "Сандерсдан наггетсларни татиб кўринг! Жуда маззали ва тўйимли! 78 гр",
                                  "Try the nuggets from Sanders! It's satisfying and delicious! 78 gr", 10000,
                                  "Курица", "Товуқ", "Chicken", "./data/img/6_nuggets.png")  # Наггетсы 6шт
    await quick_commands.add_item("Наггетсы 8шт", "Наггетслар 8 та", "Nuggets 8 pcs",
                                  "Попробуйте наггетсы от Сандерса! Это сытно и вкусно!",
                                  "Сандерсдан наггетсларни татиб кўринг! Жуда маззали ва тўйимли!",
                                  "Try the nuggets from Sanders! It's satisfying and delicious!", 14000, "Курица",
                                  "Товуқ", "Chicken",
                                  "./data/img/8_nuggets.png")  # Наггетсы 8шт
    await quick_commands.add_item("Наггетсы 18шт", "Наггетслар 18 та", "Nuggets 18 pcs",
                                  "Попробуйте наггетсы от Сандерса! Это сытно и вкусно! Наггетсов хватит на всех!",
                                  "Сандерсдан наггетсларни татиб кўринг! Жуда маззали ва тўйимли! Наггетслар ҳаммага етади.",
                                  "Try the nuggets from Sanders! It's satisfying and delicious! There are enough nuggets for everyone!",
                                  29000, "Курица", "Товуқ", "Chicken", "./data/img/18_nuggets.png")  # Наггетсы 18шт
    await quick_commands.add_item("Байтсы малые", "Кичик байтслар", "Bites small",
                                  "Свежие сочные кусочки курицы в хрустящей панировке. Взрыв вкуса для любителей острых ощущений!",
                                  "Қирсиллайдиган панировкага булаб пиширилган сархил товуқ гўшти бўлаклари. Кучли ҳиссиётларни севадиганларга муносиб, шиддатли таъм!",
                                  "Fresh chicken bites in crispy  breading. Taste explosion  for those who prefer bright sensations.",
                                  11000, "Курица", "Товуқ", "Chicken", "./data/img/bites_small.png")  # Байтсы малые
    await quick_commands.add_item("Байтсы средние", "Ўртача байтслар", "Bites Medium",
                                  "Свежие сочные кусочки курицы в хрустящей панировке. Взрыв вкуса для любителей острых ощущений!",
                                  "Қирсиллайдиган панировкага булаб пиширилган сархил товуқ гўшти бўлаклари. Кучли ҳиссиётларни севадиганларга муносиб, шиддатли таъм!",
                                  "Fresh chicken bites in crispy  breading. Taste explosion  for those who prefer bright sensations.",
                                  17000, "Курица", "Товуқ", "Chicken", "./data/img/bites_medium.png")  # Байтсы средние
    await quick_commands.add_item("Байтсы большие", "Катта байтслар", "Bites",
                                  "Свежие сочные кусочки курицы в хрустящей панировке. Взрыв вкуса для любителей острых ощущений!",
                                  "Қирсиллайдиган панировкага булаб пиширилган сархил товуқ гўшти бўлаклари. Кучли ҳиссиётларни севадиганларга муносиб, шиддатли таъм!",
                                  "Fresh chicken bites in crispy  breading. Taste explosion  for those who prefer bright sensations.",
                                  28000, "Курица", "Товуқ", "Chicken", "./data/img/bites.png")  # Байтсы большие
    await quick_commands.add_item("3 Стрипса оригинальные", "3 та оригинал стрипс", "3 Strips",
                                  "Только любимый вкус – и ничего лишнего. Потрясающе нежное куриное филе мы панируем вручную и готовим в ресторане по уникальному рецепту Полковника Сандерса. Совершенный вкус!",
                                  "Фақат севимли таъм, ортиқча ҳеч нарса йўқ. Биз ҳайратланарли тарзда юмшоқ товуқ гўштини полковник Сандерс яратган ноёб, қўл меҳнатига асосланган усул билан, панировкага булаб, пиширамиз. Мукаммал таъм!",
                                  "Only your favorite taste and nothing else. Extremely soft chicken fillet hand-breaded and cooked in the restaurant according to Colonel Sanders’ unique recipe. Perfect taste!",
                                  15000, "Курица", "Товуқ", "Chicken", "./data/img/3_strips.png")  # 3 Стрипса оригинальные
    await quick_commands.add_item("5 Стрипсов оригинальных", "5 та оригинал стрипс", "5 Strips",
                                  "Только любимый вкус – и ничего лишнего. Потрясающе нежное куриное филе мы панируем вручную и готовим в ресторане по уникальному рецепту Полковника Сандерса. Совершенный вкус!",
                                  "Фақат севимли таъм, ортиқча ҳеч нарса йўқ. Биз ҳайратланарли тарзда юмшоқ товуқ гўштини полковник Сандерс яратган ноёб, қўл меҳнатига асосланган усул билан, панировкага булаб, пиширамиз. Мукаммал таъм!",
                                  "Only your favorite taste and nothing else. Extremely soft chicken fillet hand-breaded and cooked in the restaurant according to Colonel Sanders’ unique recipe. Perfect taste!",
                                  28000, "Курица", "Товуқ", "Chicken", "./data/img/5_strips.png")  # 5 Стрипсов оригинальных
    await quick_commands.add_item("8 Стрипсов оригинальных", "8 та оригинал стрипс", "8 Strips",
                                  "Только любимый вкус – и ничего лишнего. Потрясающе нежное куриное филе мы панируем вручную и готовим в ресторане по уникальному рецепту Полковника Сандерса. Совершенный вкус!",
                                  "Фақат севимли таъм, ортиқча ҳеч нарса йўқ. Биз ҳайратланарли тарзда юмшоқ товуқ гўштини полковник Сандерс яратган ноёб, қўл меҳнатига асосланган усул билан, панировкага булаб, пиширамиз. Мукаммал таъм!",
                                  "Only your favorite taste and nothing else. Extremely soft chicken fillet hand-breaded and cooked in the restaurant according to Colonel Sanders’ unique recipe. Perfect taste!",
                                  38000, "Курица", "Товуқ", "Chicken", "./data/img/8_strips.png")  # 8 Стрипсов оригинальных
    await quick_commands.add_item("3 Стрипса острые", "3 та аччиқ стрипс", "3 Hot Strips",
                                  "Только любимый вкус – и ничего лишнего. Потрясающе нежное куриное филе мы панируем вручную и готовим в ресторане по уникальному рецепту Полковника Сандерса. Совершенный вкус!",
                                  "Фақат севимли таъм, ортиқча ҳеч нарса йўқ. Биз ҳайратланарли тарзда юмшоқ товуқ гўштини полковник Сандерс яратган ноёб, қўл меҳнатига асосланган усул билан, панировкага булаб, пиширамиз. Мукаммал таъм!",
                                  "Only your favorite taste and nothing else. Extremely soft chicken fillet hand-breaded and cooked in the restaurant according to Colonel Sanders’ unique recipe. Perfect taste!",
                                  15000, "Курица", "Товуқ", "Chicken", "./data/img/3_strips.png")  # 3 Стрипса острые
    await quick_commands.add_item("5 Стрипсов острых", "5 та аччиқ стрипс", "5 Hot Strips",
                                  "Только любимый вкус – и ничего лишнего. Потрясающе нежное куриное филе мы панируем вручную и готовим в ресторане по уникальному рецепту Полковника Сандерса. Совершенный вкус!",
                                  "Фақат севимли таъм, ортиқча ҳеч нарса йўқ. Биз ҳайратланарли тарзда юмшоқ товуқ гўштини полковник Сандерс яратган ноёб, қўл меҳнатига асосланган усул билан, панировкага булаб, пиширамиз. Мукаммал таъм!",
                                  "Only your favorite taste and nothing else. Extremely soft chicken fillet hand-breaded and cooked in the restaurant according to Colonel Sanders’ unique recipe. Perfect taste!",
                                  28000, "Курица", "Товуқ", "Chicken", "./data/img/5_strips.png")  # 5 Стрипсов острых
    await quick_commands.add_item("8 Стрипсов острых", "8 та аччиқ стрипс", "8 Hot Strip",
                                  "Только любимый вкус – и ничего лишнего. Потрясающе нежное куриное филе мы панируем вручную и готовим в ресторане по уникальному рецепту Полковника Сандерса. Совершенный вкус!",
                                  "Фақат севимли таъм, ортиқча ҳеч нарса йўқ. Биз ҳайратланарли тарзда юмшоқ товуқ гўштини полковник Сандерс яратган ноёб, қўл меҳнатига асосланган усул билан, панировкага булаб, пиширамиз. Мукаммал таъм!",
                                  "Only your favorite taste and nothing else. Extremely soft chicken fillet hand-breaded and cooked in the restaurant according to Colonel Sanders’ unique recipe. Perfect taste!",
                                  38000, "Курица", "Товуқ", "Chicken", "./data/img/8_strips.png")  # Стрипсы острые 8шт
    await quick_commands.add_item("3 Крыла", "3 та қанот", "Wings 3",
                                  "Огонь внутри! Далеко не ангельские крылышки*! Наши острые куриные крылышки в хрустящей панировке со жгучими специями – настоящий огонь!\n\n*Крыло — однофаланговая часть на одной или двух костях.",
                                  "Ичида олов бор! Тафти ёндиради! Биздаги ёндирувчи зираворлар қўшилган қирсиллама панировкага буланган аччиққина товуқ қанотлари – ҳақиқий олов!\n\n*Қанот – битта ёки иккита суякли, бир фалангали қисм.",
                                  "Fire inside! Far from angels’ wings*! Our hot chicken wings in crispy coating with spices — the true fire!\n\n*Wings could be with one or two bones.",
                                  16000, "Курица", "Товуқ", "Chicken", "./data/img/3_wings.png")  # Крылья 3шт
    await quick_commands.add_item("5 Крыльев", "5 та қанот", "Wings 5",
                                  "Огонь внутри! Далеко не ангельские крылышки*! Наши острые куриные крылышки в хрустящей панировке со жгучими специями – настоящий огонь!\n\n*Крыло — однофаланговая часть на одной или двух костях.",
                                  "Ичида олов бор! Тафти ёндиради! Биздаги ёндирувчи зираворлар қўшилган қирсиллама панировкага буланган аччиққина товуқ қанотлари – ҳақиқий олов!\n\n*Қанот – битта ёки иккита суякли, бир фалангали қисм.",
                                  "Fire inside! Far from angels’ wings*! Our hot chicken wings in crispy coating with spices — the true fire!\n\n*Wings could be with one or two bones.",
                                  26000, "Курица", "Товуқ", "Chicken", "./data/img/5_wings.png")  # Крылья 5шт
    await quick_commands.add_item("8 Крыльев", "8 та қанот", "Wings 8",
                                  "Огонь внутри! Далеко не ангельские крылышки*! Наши острые куриные крылышки в хрустящей панировке со жгучими специями – настоящий огонь!\n\n*Крыло — однофаланговая часть на одной или двух костях.",
                                  "Ичида олов бор! Тафти ёндиради! Биздаги ёндирувчи зираворлар қўшилган қирсиллама панировкага буланган аччиққина товуқ қанотлари – ҳақиқий олов!\n\n*Қанот – битта ёки иккита суякли, бир фалангали қисм.",
                                  "Fire inside! Far from angels’ wings*! Our hot chicken wings in crispy coating with spices — the true fire!\n\n* Wings could be with one or two bones.",
                                  39000, "Курица", "Товуқ", "Chicken", "./data/img/8_wings.png")  # Крылья 8шт

    # Ланчбоксы
    await quick_commands.add_item("5 за 25 000", "25 000 сўмга 5 та", "5 pc. – 25 000",
                                  "Лонгер, Картофель фри малый, Напиток 0,3, Соус на выбор, Байтсы 60 гр.",
                                  "Лонгер, байтслар 60 гр., кичик фри картошкаси, ичимлик 0.3 хоҳишингизга кўра, соус хоҳишингизга кўра.",
                                  "Longer, bites 60g, fries small box, 0.3l Drink (any), sauce (any)", 25000,
                                  "Ланчбоксы", "Ланчбокслар", "LunchBox", "./data/img/5_25000.png")  # 5 за 25000
    await quick_commands.add_item("5 за 25 000", "25 000 сўмга 5 та", "5 for 25 000 JR",
                                  "Твистер Джуниор, байтсы 60 гр., фри малый, напиток 0,3 л на выбор, соус на выбор.",
                                  "Твистер Джуниор, байтслар 60 гр., кичик фри картошкаси, ичимлик 0,3 л хоҳишингизга кўра, соус хоҳишингизга кўра.",
                                  "Twister Junior, bites 60g, small fries, Coca-Cola 0.3l, a choice of sauce.", 25000,
                                  "Ланчбоксы", "Ланчбокслар", "LunchBox", "./data/img/5_25000_JR.png")  # 5 за 25000 JR
    await quick_commands.add_item("5 за 30 000", "30 000 сўмга 5 та", "5 pc. – 30 000",
                                  "Чизбургер, Картофель фри малый, Напиток 0,4, Соус на выбор, 2 крыла",
                                  "Чизбургер, Кичик фри картошкаси, ичимлик 0.4 хоҳишингизга кўра, 2 аччиқ қанот, соус хоҳишингизга кўра",
                                  "Cheeseburger, 2 wings, fries small box, sauce (any), 0.4l Drink (any)", 30000,
                                  "Ланчбоксы", "Ланчбокслар", "LunchBox", "./data/img/5_30000.png")  # 5 за 30000
    await quick_commands.add_item("5 за 35 000", "35 000 сўмга 5 та", "5 pc. – 35,000",
                                  "Твистер, картофель фри малый, Напиток 0,5, Соус на выбор, 2 крыла",
                                  "Твистер, кичик фри картошкаси, ичимлик 0.5 хоҳишингизга кўра, 2 аччиқ қанот, соус хоҳишингизга кўра.",
                                  "Twister original/ spicy, 2 wings, fries small box, sauce (any), 0.5l Drink (any)",
                                  35000, "Ланчбоксы", "Ланчбокслар", "LunchBox", "./data/img/5_35000.png")  # 5 за 35000
    await quick_commands.add_item("5 за 40 000", "40 000 сўмга 5 та", "5 pc. – 40 000",
                                  "Боксмастер оригинальный/острый, байтсы 60 гр., картофель фри малый, напиток 0,5 л на выбор, соус на выбор.",
                                  "Боксмастер оригинал/ аччиқ, байтслар 60 гр., кичик фри картошкаси, ичимлик 0,5 л хоҳишингизга кўра, соус хоҳишингизга кўра.",
                                  "Boxmaster original/ spicy, bites 60g, fries small box, sauce (any), 0.5l Coca-Cola",
                                  40000, "Ланчбоксы", "Ланчбокслар", "LunchBox", "./data/img/5_40000.png")  # 5 за 40000

    # Баскеты
    await quick_commands.add_item("Френдс Бокс Ассорти", "Френдс Бокс Ассорти", "Friends Box!",
                                  "В составе каждого бокса: 5 сочных ножек, 10 хрустящих крылышек, 5 стрипсов, 270 грамм аппетитных байтсов и целый баскет золотистой фри. Такого бокса точно хватит, чтобы вкусно перекусить с близкими.",
                                  "Ҳар бир бокс таркибида: 5 та маззали оёқча, 10 та карсилдоқ қанотча, 5 та стрипс, 270 грамм иштаҳаочар байтслар ва бир баскет тўла тилларанг фри бор. Яқинлар даврасида мазали тамадди учун аниқ етади.",
                                  "Friends Box! When it’s enough for everyone! 5 drumsticks, 5 strips, 10 wings, 270 g bites, basket fries.",
                                  150000, "Баскеты", "Баскетлар", "Buckets",
                                  "./data/img/friends_box.png")  # Френдс бокс ассорти
    await quick_commands.add_item("Сандерс Баскет", "Сандерс Баскет", "Sanders Bucket",
                                  "1 Ножка, 2 острых крыла, 2 стрипса, 4 острых байтса",
                                  "1 та оёқ, 2 та аччиқ канот, 2 та стрипс, 4 та байтс",
                                  "Bucket from Colonel Sanders! 1 drumstick, 2 wings, 2 strips, 4 bites", 35000,
                                  "Баскеты", "Баскетлар", "Buckets", "./data/img/sanders_bucket.png")  # Сандерс баскет
    await quick_commands.add_item("Баскет 10 ножек", "Баскет 10 оёқча", "Bucket 10 drumsticks",
                                  "Баскетов много не бывает. Встречайте новинку! Баскет 10 ножек, 1 картофеля фри стандартный",
                                  "Баскетнинг кўпи бўлмайди. Янгиликни кўтиб олинг! 10 та оёқчали баскет, 1 стандарт фри картошкаси.",
                                  "Buckets are never enough. Meet the new one! Bucket 10 drumsticks, 1 french fries standart",
                                  90000, "Баскеты", "Баскетлар", "Buckets", "./data/img/10_bucket.png")  # Баскет 10 ножек
    await quick_commands.add_item("Баскет S (12 острых крыльев)", "Баскет S (12 аччиқ қанот)", "Basket S",
                                  "12 куриных крылышек в острой панировке",
                                  "Аччиқ панировкадаги 12 та товуқ қанотчалари", "12 hot&spicy chicken wings", 55000,
                                  "Баскеты", "Баскетлар", "Buckets",
                                  "./data/img/s_bucket.png")  # Баскет S (12 острых крыльев)
    await quick_commands.add_item("Баскет M (18 острых крыла)", "Баскет М (18 аччиқ қанот)", "Basket M",
                                  "18 куриных крылышка в острой панировке",
                                  "Аччиқ панировкадаги 18 та товуқ қанотчалари", "18 hot&spicy chicken wings", 80000,
                                  "Баскеты", "Баскетлар", "Buckets",
                                  "./data/img/m_bucket.png")  # Баскет M (18 острых крыла)
    await quick_commands.add_item("Баскет L (26 острых крыльев)", "Баскет L (26 аччиқ қанот)", "Bucket L",
                                  "26 куриных крылышек в острой панировке",
                                  "Аччиқ панировкадаги 26 та товуқ қанотчалари", "26 hot&spicy chicken wings", 100000,
                                  "Баскеты", "Баскетлар", "Buckets",
                                  "./data/img/l_bucket.png")  # Баскет L (26 острых крыльев)
    await quick_commands.add_item("Баскет Дуэт оригинальный", "Дуэт оригинал баскети",
                                  "Duet bucket with original stripes",
                                  "Всемирно известные хиты от KFC в нашем Баскете! Для вас мы собрали отличную компанию – сочные кусочки курицы, обжигающе острые крылышки, нежнейшие стрипсы и картофель фри. Много не бывает! В состав баскета входят: 2 ножки, 4 куриных крылышка*, 4 стрипса в оригинальной панировке, 2 картофеля фри 60г.\n\n*Крыло — однофаланговая часть на одной или двух костях.",
                                  "KFCнинг дунёга машҳур таомлари бизнинг Баскетда! Сиз учун ажойиб улфатларни – сархил товуқ гўшти, жизиллатувчи, аччиққина қанотларни, майин стрипсларни ва картошка-фрини тўпладик. Кўплик қилмайди! Баскет таркибига қуйидагилар киради: 2 та оёқ, 4 та товуқ қаноти*, оригинал панировкага буланган 2 та стрипс, 2 та картошка-фри.\n\n*Қанот – битта ёки иккита суякли, бир фалангали қисм.",
                                  "Large scale attitude! World famous KFC hits in our Bucket! We gathered a great company for you – juicy chicken nuggets, spicy hot wings*, tender strips and French fries. As good as it gets!\n\n*Wings could be with one or two bones.",
                                  65000, "Баскеты", "Баскетлар", "Buckets",
                                  "./data/img/d_bucket.png")  # Баскет Дуэт оригинальный
    await quick_commands.add_item("Баскет Дуэт острый", "Аччиқ Дуэт баскети", "Duet bucket with hot stripes",
                                  "Всемирно известные хиты от KFC в нашем Баскете! Для вас мы собрали отличную компанию – сочные кусочки курицы, обжигающе острые крылышки, нежнейшие стрипсы и картофель фри. Много не бывает! В состав баскета входят: 2 ножки, 4 куриных крылышка*, 4 стрипса в панировке Hot and spicy, 2 картофеля фри 60г.\n\n*Крыло — однофаланговая часть на одной или двух костях.",
                                  "KFCнинг дунёга машҳур таомлари бизнинг Баскетда! Сиз учун ажойиб улфатларни – сархил товуқ гўшти, жизиллатувчи, аччиққина қанотларни, майин стрипсларни ва картошка-фрини тўпладик. Кўплик қилмайди! Баскет таркибига қуйидагилар киради: 2 та оёқ, 4 та товуқ қаноти*, Hot and spicy панировкасига буланган 4 та стрипс, 60 г лик 2 та картошка-фри.\n\n*Қанот – битта ёки иккита суякли, бир фалангали қисм.",
                                  "Large scale attitude! World famous KFC hits in our Bucket! We gathered a great company for you – juicy chicken nuggets, spicy hot wings, tender strips and French fries. As good as it gets!",
                                  65000, "Баскеты", "Баскетлар", "Buckets", "./data/img/d_bucket.png")  # Баскет Дуэт острый
    await quick_commands.add_item("Наггетс Бокс", "Наггетс Бокс", "Nuggets Box",
                                  "5 оригинальных наггетсов и хрустящий картофель фри с аппетитной хрустящей корочкой и мягкой, рассыпчатой серединкой - бокс выбирают настоящие любители  курочки! 75 гр/100 гр",
                                  "5 оригинал наггетслар ва сирти қарсиллайдиган, ичи юмшоқ мазали фри картошкаси - ҳақиқий товуқ ихлосмандларининг асл танлови! 75 гр/100 гр",
                                  "5 original nuggets and crispy french fries with delicious crispy crust and soft, crumbly middle part — it is the box chosen by real chicken lovers! 75 gr/100 gr",
                                  17000, "Баскеты", "Баскетлар", "Buckets", "./data/img/nuggets_bucket.png")  # Наггетс Бокс
    await quick_commands.add_item("Микс Бокс", "Микс Бокс", "Mix box",
                                  "5 оригинальных наггетсов и байтсы стандартные! Микс  бокс - выбирают настоящие любители сочной курочки! 75/ 101 гр",
                                  "5та ҳақиқий наггетслар ва стандарт байтслар! Сарҳил товуқнинг чинакам ишқивозлари микс боксни танлайди! 75/101 гр",
                                  "5 original nuggets and standard bytes! Mix box — is the choice of real lovers of juicy chicken! 75/101 gr",
                                  18000, "Баскеты", "Баскетлар", "Buckets", "./data/img/mix_bucket.png")  # Микс Бокс
    await quick_commands.add_item("Пати баскет", "Пати баскети", "Party Bucket",
                                  "Попробуй супермегазаводной  «Пати Баскет» в KFC. Хрустящий аппетитный картофель, 6 кусочков байтс  и сырный соус — тебе понравится!",
                                  'KFCда супер, мега шодлик улашувчи “Пати Баскети”ни татиб кўринг. Қирсилловчи иштаҳаочар картошка, 6 та байтс бўлаги ва пишлоқли соус. Сизга ёқиб қолади',
                                  'Try supermegacool "Party Bucket" in KFC! Golden crispy French fries with 6 bites and cheese sauce — so good that you want it again and again!',
                                  17000, "Баскеты", "Баскетлар", "Buckets", "./data/img/party_bucket.png")  # Пати Бокс

    # Картошка и снеки
    await quick_commands.add_item("Хашбраун", "Хашбраун", "Hash brown", "Хашбраун", "Хашбраун", "Hash brown", 4000,
                                  "Снэки", "Снэклар", "Snacks", "./data/img/hash_brown.png")  # Хашбраун
    await quick_commands.add_item("Булочка", "Булочка", "Bun", "Булочка", "Булочка", "Bun", 4000, "Снэки", "Снэклар",
                                  "Snacks", "./data/img/bun.png")  # Булочка
    await quick_commands.add_item("Картофель фри малый", "Кичик фри картошкаси", "Fries small",
                                  "Еще больше вкуса! В наших крупных ломтиках мы сохранили еще больше вкуса твоего любимого картофеля фри. Он получается именно таким, как ты любишь – с аппетитной хрустящей корочкой и мягкой, рассыпчатой серединкой.\nЛюбимое удовольствие!",
                                  "Янаям мазали! Биз каттагина картошка тилимчаларида сиз ёқтирган фри таъмини янада кўп сақлаб қола олдик. У сиз ёқтиргандек – сирти карсиллайдиган, ичи юмшоқ ва уваланадиган бўлиб пишяпти.\nБу сиз севган лаззатдир!",
                                  "Even more taste! Our big chunks have kept even more of the way your favorite French fries taste. It is just the way you like — with tasty crispy crust and soft crumby inside.\nThe most favorite pleasure!",
                                  8000, "Снэки", "Снэклар", "Snacks", "./data/img/s_fries.png")  # Фри малый
    await quick_commands.add_item("Картофель фри стандартный", "Стандарт фри картошкаси", "Fries medium",
                                  "Еще больше вкуса! В наших крупных ломтиках мы сохранили еще больше вкуса твоего любимого картофеля фри. Он получается именно таким, как ты любишь – с аппетитной хрустящей корочкой и мягкой, рассыпчатой серединкой.\nЛюбимое удовольствие!",
                                  "Янаям мазали! Биз каттагина картошка тилимчаларида сиз ёқтирган фри таъмини янада кўп сақлаб қола олдик. У сиз ёқтиргандек – сирти карсиллайдиган, ичи юмшоқ ва уваланадиган бўлиб пишяпти.\nБу сиз севган лаззатдир!",
                                  "Even more taste! Our big chunks have kept even more of the way your favorite French fries taste. It is just the way you like — with tasty crispy crust and soft crumby inside.\nThe most favorite pleasure!",
                                  11000, "Снэки", "Снэклар", "Snacks", "./data/img/m_fries.png")  # Фри стандартный
    await quick_commands.add_item("Баскет фри", "Баскет фри", "Bucket Fries",
                                  "Еще больше вкуса! В наших крупных ломтиках мы сохранили еще больше вкуса твоего любимого картофеля фри. Он получается именно таким, как ты любишь – с аппетитной хрустящей корочкой и мягкой, рассыпчатой серединкой.\nЛюбимое удовольствие!",
                                  "Янаям мазали! Биз каттагина картошка тилимчаларида сиз ёқтирган фри таъмини янада кўп сақлаб қола олдик. У сиз ёқтиргандек – сирти карсиллайдиган, ичи юмшоқ ва уваланадиган бўлиб пишяпти.\nБу сиз севган лаззатдир!",
                                  "Even more taste! Our big chunks have kept even more of the way your favorite French fries taste. It is just the way you like — with tasty c  rispy crust and soft crumby inside.\nThe most favorite pleasure!",
                                  17000, "Снэки", "Снэклар", "Snacks", "./data/img/b_fries.png")  # Баскет фри
    await quick_commands.add_item("Сандерс картофель фри", "Сандерс Фри картошкаси", "Sanders Fries",
                                  "Сандерс картофель фри d_ru", "Сандерс Фри картошкаси d_uz", "Sanders Fries d_en",
                                  16000, "Снэки", "Снэклар", "Snacks", "./data/img/s_s_fries.png")  # Сандерс картофель фри
    await quick_commands.add_item("Картофель по-деревенски малый", "Қишлоқ рецепти бўйича картошка",
                                  "Potato wedges small",
                                  "Рассыпчатый и хрустящий картофель по-деревенски – любимый вкус теперь в KFC!",
                                  "Дона-дона ва қарсиллаб турадиган қишлоқ рецепти бўйича тайёрланган картошка  - KFCда энди севимли таъм!",
                                  "This so crispy, tasty and beloved flavor is now in KFC!", 8000, "Снэки", "Снэклар",
                                  "Snacks", "./data/img/s_wedges.png")  # Картофель по-деревенски малый
    await quick_commands.add_item("Картофель по-деревенски станд.", "Қишлоқ рецепти бўйича картошка станд.",
                                  "Potato wedges",
                                  "Рассыпчатый и хрустящий картофель по-деревенски – любимый вкус теперь в KFC!",
                                  "Дона-дона ва қарсиллаб турадиган қишлоқ рецепти бўйича тайёрланган картошка  - KFCда энди севимли таъм!",
                                  "This so crispy, tasty and beloved flavor is now in KFC!", 12000, "Снэки", "Снэклар",
                                  "Snacks", "./data/img/wedges.png")  # Картофель по-деревенски станд.

    # Десерты
    await quick_commands.add_item("Пирожок вишневый", "Олчали Пирогча", "Cherry pie",
                                  "Пирожок с вишневой начинкой, 85 грамм",
                                  "Олчали джем билан тўлдирилган пирогча, 85 грамм.",
                                  "Pie with cherry filling, 85 grams", 10000, "Десерты", "Десертлар", "Desserts",
                                  "./data/img/cherry_pie.png")  # Пирожок Вишневый
    await quick_commands.add_item("Донат карамельный", "Карамелли Донат", "Caramel donut",
                                  "Донат с карамельной глазурью и карамельной начинкой, 67 грамм.",
                                  "Карамел билан қопланган ва карамел билан тўлдирилган донат, 67 грамм.",
                                  "Donut with caramel glaze and caramel filling, 67 grams.", 12000, "Десерты",
                                  "Десертлар", "Desserts", "./data/img/caramel_donut.png")  # Донат Карамельный
    await quick_commands.add_item("Донат Яблоко-корица", "Донат Олма-долчин", "Donut Apple-Cinnamon",
                                  "Попробуй новинку: нежнейший пончик с яблочной начинкой и корицей!",
                                  "Янгиликни татиб кўр: олма ва долчин қўшилган юмшоққина пончик!",
                                  "Try a new dessert: Delicate donut with apple and cinnamon filling!", 12000,
                                  "Десерты", "Десертлар", "Desserts", "./data/img/apple_donut.png")  # Донат Яблоко-корица
    await quick_commands.add_item("Донат клубничный", "Қулупнайли донат", "Donut Strawberry",
                                  "Клубничный донат с начинкой из мягкого клубничного джема.",
                                  "Ичига майин қулупнай мураббоси қўшилган қулупнайли донат.",
                                  "Strawberry Donut with soft strawberry jam.", 12000, "Десерты", "Десертлар",
                                  "Desserts", "./data/img/strawberry_donut.png")  # Донат Клубничный
    await quick_commands.add_item("Донат ореховый", "Ёнғоқли донат", "Nutty donut",
                                  "Нежнейший донат с ореховой начинкой украшен дробленным орехом. Донатов много не бывает, попробуй и ты новинку!  71 гр.",
                                  "Ёнғоқ билан тўлдирилган ва қопланган нозик донат. Янгиликни таътаб кўринг! 71 гр.",
                                  "Delicate donut with a nut filling is decorated with crushed nuts. It is time to try it! 71 gr.",
                                  12000, "Десерты", "Десертлар", "Desserts", "./data/img/nutty_donut.png")  # Донат Ореховый
    await quick_commands.add_item("Маффин Шоколад", "Маффин шоколадли", "Chocolate muffin",
                                  "Маффин с двойным шоколадом - выбор истинного гурмана. 104 гр.",
                                  "Иккита шоколадли маффин – ҳақиқий гурманлар танлови. 104 гр.",
                                  "A double chocolate muffin is the choice of a true gourmet. 104  gr.", 14000,
                                  "Десерты", "Десертлар", "Desserts", "./data/img/choco_muffin.png")  # Маффин шоколад
    await quick_commands.add_item("Маффин Черника", "Маффин Черникали", "Blueberry Muffin",
                                  "Маффин с черникой, отличное дополнение для кофе. 100 гр.",
                                  "Черника билан маффин, қаҳва учун ажойиб жуфтлик. 100 гр.",
                                  "Blueberry muffin, a great addition to your coffee. 100 gr.", 14000, "Десерты",
                                  "Десертлар", "Desserts", "./data/img/blueberry_muffin.png")  # Маффин черника

    # Соусы
    await quick_commands.add_item("Кетчуп томатный", "Томатли кетчуп", "Ketchup tomato", "Кетчуп томатный",
                                  "Томатли кетчуп", "Ketchup tomato", 3000, "Соусы", "Соуслар", "Sauces",
                                  "./data/img/ketchup_tomato.png")  # Томатный
    await quick_commands.add_item("Соус кисло-сладкий Чили", "Чили нордон-ширин соуси", "Sweet N’ Sour sauce",
                                  "Соус кисло-сладкий Чили", "Чили нордон-ширин соуси", "Sweet N’ Sour sauce", 3000,
                                  "Соусы", "Соуслар", "Sauces", "./data/img/sweet_sour.png")  # Кисло-сладкий
    await quick_commands.add_item("Соус Чесночный", "Саримсоқли соус", "Garlic sauce", "Соус Чесночный",
                                  "Саримсоқли соус", "Garlic sauce", 3000, "Соусы", "Соуслар", "Sauces",
                                  "./data/img/garlic_sauce.png")  # Чесночный
    await quick_commands.add_item("Соус Сырный оригинальный", "Пишлоқли, оригинал соус", "Cheese sauce",
                                  "Соус Сырный оригинальный", "Пишлоқли, оригинал соус", "Cheese sauce", 3000, "Соусы",
                                  "Соуслар", "Sauces", "../img/cheese_sauce.png")  # Сырный оригинальный
    await quick_commands.add_item("Соус Терияки", "Терияки соуси", "Teriyaki sauce", "Соус Терияки", "Терияки соуси",
                                  "Teriyaki sauce", 3000, "Соусы", "Соуслар", "Sauces",
                                  "./data/img/teriyaki_sauce.png")  # Соус Терияки

    # Напитки
    await quick_commands.add_item("Coca-cola 0,5л", "Coca-cola 0,5л", "Coca-cola 0,5l", "Coca-cola 0,5l",
                                  "Coca-cola 0,5л", "Coca-cola 0,5l", 7000, "Прохладительные напитки",
                                  "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/cola_05.png")  # Coca-Cola 0.5
    await quick_commands.add_item("Fanta 0,5л", "Fanta 0,5л", "Fanta 0,5l", "Fanta 0,5л", "Fanta 0,5л", "Fanta 0,5l",
                                  7000, "Прохладительные напитки", "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/fanta_05.png")  # Fanta 0.5
    await quick_commands.add_item("Sprite 0.5л", "Sprite 0.5л", "Sprite 0.5l", "Sprite 0.5л", "Sprite 0.5л",
                                  "Sprite 0.5l", 7000, "Прохладительные напитки", "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/sprite_05.png")  # Sprite 0.5
    await quick_commands.add_item("Fuse Tea Лимон 0.5л", "Fuse Tea Limon 0.5л", "Fuse Tea Lemon 0.5l",
                                  "Fuse Tea Лимон 0.5л", "Fuse Tea Limon 0.5л", "Fuse Tea Lemon 0.5l", 5000,
                                  "Прохладительные напитки", "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/fuse_lemon.png")  # Fuse Tea Lemon 0.5
    await quick_commands.add_item("Fuse Tea Персик 0.5л", "Fuse Tea Shaftoli 0.5л", "Fuse Tea Peach 0.5l",
                                  "Fuse Tea Персик 0.5л", "Fuse Tea Shaftoli 0.5л", "Fuse Tea Peach 0.5l", 5000,
                                  "Прохладительные напитки", "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/fuse_peach.png")  # Fuse Tea Peach 0.5
    await quick_commands.add_item("Fuse Tea Манго-Ананас 0.5л", "Fuse Tea Mango Ananas 0.5л",
                                  "Fuse Tea Mango-Pineapple 0.5l", "Fuse Tea Манго-Ананас 0.5л",
                                  "Fuse Tea Mango Ananas 0.5л", "Fuse Tea Mango-Pineapple 0.5l", 5000,
                                  "Прохладительные напитки", "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/fuse_mango.png")  # Fuse Tea Mango-Pineapple 0.5
    await quick_commands.add_item("Сок яблочный 0,2л", "Олмали шарбат 0,2л", "Juice Apple 0,2l", "Сок яблочный 0,2л",
                                  "Олмали шарбат 0,2л", "Juice Apple 0,2l", 3000, "Прохладительные напитки",
                                  "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/bliss_apple.png")  # Сок Bliss Apple
    await quick_commands.add_item("Сок персиковый 0,2л", "Шафтоли шарбати 0,2л", "Juice Peach 0,2l",
                                  "Сок персиковый 0,2л", "Шафтоли шарбати 0,2л", "Juice Peach 0,2l", 3000,
                                  "Прохладительные напитки", "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/bliss_peach.png")  # Сок Bliss Peach
    await quick_commands.add_item("Сок апельсиновый 0,2л", "Апелсинли шарбат 0,2л", "Juice Orange 0,2l",
                                  "Сок апельсиновый 0,2л", "Апелсинли шарбат 0,2л", "Juice Orange 0,2l", 3000,
                                  "Прохладительные напитки", "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/bliss_orange.png")  # Сок Bliss Orange
    await quick_commands.add_item("Сок вишневый 0,2л", "Олчали шарбат 0,2л", "Juice Cherry 0,2l", "Сок вишневый 0,2л",
                                  "Олчали шарбат 0,2л", "Juice Cherry 0,2l", 3000, "Прохладительные напитки",
                                  "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/bliss_cherry.png")  # Сок Bliss Cherry
    await quick_commands.add_item("BonAqua вода не газированная 0,5л", "BonAqua газланмаган сув 0,5л", "BonAqua 0,5l",
                                  "BonAqua вода питьевая не газированная 0,5л", "BonAqua газламанган ичимлик суви 0,5л",
                                  "BonAqua 0,5l", 3000, "Прохладительные напитки", "Sovuq ichimliklar", "Cold drinks",
                                  "./data/img/water.png")  # Вода не газированная BONAQUA
    await quick_commands.add_item("Вода BonAqua газированная 0,5л", "Газли сув BonAqua 0,5л", "BonAqua sparkling 0,5l",
                                  "Вода питьевая BonAqua газированная 0,5л", "BonAqua газли ичимлик суви 0,5л",
                                  "BonAqua sparkling 0,5l", 3000, "Прохладительные напитки", "Sovuq ichimliklar",
                                  "Cold drinks",
                                  "./data/img/water_sp.png")  # Вода газированная BONAQUA
    await quick_commands.add_item("Кофе Капучино 0,2", "Капучино қаҳваси 0,2", "Cappuccino 0,2",
                                  "Кофе Капучино 0,2 зерновой", "донли Капучино қахваси 0,2", "Cappuccino 0,2", 11000,
                                  "Горячие напитки", "Issiq ichimliklar", "Hot drinks",
                                  "./data/img/cappuccino_02.png")  # Кофе капучино 0.2
    await quick_commands.add_item("Кофе Капучино 0,3", "Капучино қаҳваси 0,3", "Cappuccino 0,3",
                                  "Кофе Капучино 0,3 зерновой", "донли Капучино қахваси 0,3", "Cappuccino 0,3", 13000,
                                  "Горячие напитки", "Issiq ichimliklar", "Hot drinks",
                                  "./data/img/cappuccino_03.png")  # Кофе капучино 0.3
    await quick_commands.add_item("Кофе Капучино 0,4", "Капучино қаҳваси 0,4", "Cappuccino 0,4",
                                  "Кофе Капучино 0,4 зерновой", "донли Капучино қахваси 0,4", "Cappuccino 0,4", 15000,
                                  "Горячие напитки", "Issiq ichimliklar", "Hot drinks",
                                  "./data/img/cappuccino_04.png")  # Кофе капучино 0.4
    await quick_commands.add_item("Кофе Латте 0,2", "Латте қаҳваси 0,2", "Latte 0,2", "Кофе Латте 0,2",
                                  "Латте қаҳваси 0,2", "Latte 0,2", 11000, "Горячие напитки", "Issiq ichimliklar",
                                  "Hot drinks",
                                  "./data/img/latte_02.png")  # Кофе латте 0.2
    await quick_commands.add_item("Кофе Латте 0,3", "Латте қаҳваси 0,3", "Latte 0,3", "Кофе Латте 0,3",
                                  "Латте қаҳваси 0,3", "Latte 0,3", 13000, "Горячие напитки", "Issiq ichimliklar",
                                  "Hot drinks",
                                  "./data/img/latte_03.png")  # Кофе латте 0.3
    await quick_commands.add_item("Кофе Латте 0,4", "Латте қаҳваси 0,4", "Latte 0,4", "Кофе Латте 0,4",
                                  "Латте қаҳваси 0,4", "Latte 0,4", 15000, "Горячие напитки", "Issiq ichimliklar",
                                  "Hot drinks",
                                  "./data/img/latte_04.png")  # Кофе латте 0.4
    await quick_commands.add_item("Кофе Американо 0,2", "Американо қаҳваси 0,2", "Americano 0,2",
                                  "Кофе Американо 0,2 зерновой", "Донли Американо қаҳваси 0,2 ", "Americano 0,2", 10000,
                                  "Горячие напитки", "Issiq ichimliklar", "Hot drinks",
                                  "./data/img/americano.png")  # Кофе американо 0.2
    await quick_commands.add_item("Кофе Американо 0,3", "Американо қаҳваси 0,3", "Americano 0,3",
                                  "Кофе Американо 0,3 зерновой", "Донли Американо қаҳваси 0,3 ", "Americano 0,3", 12000,
                                  "Горячие напитки", "Issiq ichimliklar", "Hot drinks",
                                  "./data/img/americano.png")  # Кофе американо 0.3
    await quick_commands.add_item("Кофе Двойной Эспрессо 0,1", "Икки ҳисса Эспрессо қаҳваси 0,1", "Double Espresso 0,1",
                                  "Кофе Двойной Эспрессо 0,1 зерновой", "Донли икки ҳисса Эспрессо қахваси 0,1",
                                  "Double Espresso 0,1", 10000, "Горячие напитки", "Issiq ichimliklar", "Hot drinks",
                                  "./data/img/double.png")  # Кофе двойной эспрессо 0.1
    await quick_commands.add_item("Чай зеленый 0.3л", "Кўк чой 0.3л", "Green Tea 0,3l", "Чай зеленый 0.3л",
                                  "Кўк чой 0.3л", "Green Tea 0,3l", 4000, "Горячие напитки", "Issiq ichimliklar",
                                  "Hot drinks", "./data/img/tea.png")  # Чай зеленый 0.3л
    await quick_commands.add_item("Чай зеленый 0.4л", "Кўк чой 0.4л", "Green Tea 0,4l", "Чай зеленый 0.4л",
                                  "Кўк чой 0.4л", "Green Tea 0,4l", 5000, "Горячие напитки", "Issiq ichimliklar",
                                  "Hot drinks", "./data/img/tea.png")  # Чай зеленый 0.4л
    await quick_commands.add_item("Чай черный 0.3л", "Қора чой 0.3л", "Black Tea 0,3l", "Чай черный 0.3л",
                                  "Қора чой 0.3л", "Black Tea 0,3l", 4000, "Горячие напитки", "Issiq ichimliklar",
                                  "Hot drinks", "./data/img/tea.png")  # Чай черный 0.3л
    await quick_commands.add_item("Чай черный 0.4л", "Қора чой 0.4л", "Black Tea 0,4l", "Чай черный 0.4л",
                                  "Қора чой 0.4л", "Black Tea 0,4l", 5000, "Горячие напитки", "Issiq ichimliklar",
                                  "Hot drinks", "./data/img/tea.png")  # Чай черный 0.4л

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



loop = asyncio.get_event_loop()
loop.run_until_complete(test())
