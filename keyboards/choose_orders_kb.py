from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='>', callback_data='next_order_choose')
b2 = InlineKeyboardButton(text='<', callback_data='previous_order_choose')
b3 = InlineKeyboardButton(text='Связаться', callback_data='get_contact_order')
b4 = InlineKeyboardButton(text='❤️', callback_data='like_order')

kb_choose_orders = InlineKeyboardMarkup(row_width=2)

kb_choose_orders.insert(b2).insert(b1).add(b3).insert(b4)
