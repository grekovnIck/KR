from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Поддержка')
b2 = KeyboardButton('Разместить заказ')
b4 = KeyboardButton('Мои заказы')
b5 = KeyboardButton('Меню перевозчика')
b6 = KeyboardButton('О проекте')
b7 = KeyboardButton('Найти исполнителя')
b8 = KeyboardButton('❤️')
b9 = KeyboardButton('Исполнители')

kb_order = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_order.add(b2).insert(b4).add(b8).insert(b9).add(b1).insert(b6).add(b5)
