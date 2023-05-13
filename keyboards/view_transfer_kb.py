from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='>', callback_data='next_transfer')
b2 = InlineKeyboardButton(text='<', callback_data='previous_transfer')
b3 = InlineKeyboardButton(text='Редактировать', callback_data='edit_transfer')
b4 = InlineKeyboardButton(text='Найти заказы', callback_data='find_orders')

kb_view_order = InlineKeyboardMarkup(row_width=2)

kb_view_order.insert(b2).insert(b1).add(b3).insert(b4)
