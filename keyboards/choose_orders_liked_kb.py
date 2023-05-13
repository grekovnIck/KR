from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='>', callback_data='next_order_choose_liked')
b2 = InlineKeyboardButton(text='<', callback_data='previous_order_choose_liked')
b3 = InlineKeyboardButton(text='Связаться', callback_data='get_contact_order_liked')
b4 = InlineKeyboardButton(text='💔', callback_data='dislike_order')

kb_choose_orders_liked = InlineKeyboardMarkup(row_width=2)

kb_choose_orders_liked.insert(b2).insert(b1).add(b4).insert(b3)
