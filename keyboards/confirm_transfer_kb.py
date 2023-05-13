from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Внести изменения')
b2 = KeyboardButton('Разместить перевозку')
b3 = KeyboardButton('Вернуться в меню')

kb_confirm_transfer = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_confirm_transfer.add(b2).add(b1).add(b3)
