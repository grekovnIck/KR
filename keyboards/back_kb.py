from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Вернуться в меню')

kb_back = ReplyKeyboardMarkup(resize_keyboard=True)

kb_back.insert(b1)
