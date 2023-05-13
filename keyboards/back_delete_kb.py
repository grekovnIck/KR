from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Вернуться в меню')
b2 = KeyboardButton('Удалить')

kb_back_or_delete = ReplyKeyboardMarkup(resize_keyboard=True)

kb_back_or_delete.insert(b1).add(b2)
