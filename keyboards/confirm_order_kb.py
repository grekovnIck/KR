from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Внести изменения')
b2 = KeyboardButton('Разместить заказ')
b3 = KeyboardButton('Вернуться в меню')

kb_confirm_order = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_confirm_order.add(b2).add(b1).add(b3)
