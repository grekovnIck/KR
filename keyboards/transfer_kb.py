from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Поддержка')
b2 = KeyboardButton('Разместить перевозку')
b4 = KeyboardButton('Мои перевозки')
b5 = KeyboardButton('Меню клиента')
b6 = KeyboardButton('О проекте')
b7 = KeyboardButton('Найти заказы')
b8 = KeyboardButton('🧡')
b9 = KeyboardButton('Заказы')

kb_transfer = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_transfer.add(b2).insert(b4).add(b8).insert(b9).add(b1).insert(b6).add(b5)
