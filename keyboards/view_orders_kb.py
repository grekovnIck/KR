from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='>', callback_data='next')
b2 = InlineKeyboardButton(text='<', callback_data='previous')
b3 = InlineKeyboardButton(text='Редактировать', callback_data='edit')
b4 = InlineKeyboardButton(text='Найти исполнителя', callback_data='find_transfer')

kb_view_order = InlineKeyboardMarkup(row_width=2)

kb_view_order.insert(b2).insert(b1).add(b3).insert(b4)
