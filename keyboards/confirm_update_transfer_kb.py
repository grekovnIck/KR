from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Внести изменения')
b2 = KeyboardButton('Обновить данные о поездке')
b3 = KeyboardButton('Вернуться в меню')

kb_confirm_transfer_update = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_confirm_transfer_update.add(b2).add(b1).add(b3)
