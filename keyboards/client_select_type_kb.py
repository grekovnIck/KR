from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Заказать')
b2 = KeyboardButton('Перевезти')

kb_client_select = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client_select.insert(b1).insert(b2)
