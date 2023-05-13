from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Предоставить номер телефона', request_contact=True)


kb_get_phone_number = ReplyKeyboardMarkup(resize_keyboard=True)

kb_get_phone_number.insert(b1)
