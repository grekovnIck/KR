from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='>', callback_data='next_transfer_choose_liked')
b2 = InlineKeyboardButton(text='<', callback_data='previous_transfer_choose_liked')
b3 = InlineKeyboardButton(text='Связаться', callback_data='get_contact_transfer_liked')
b4 = InlineKeyboardButton(text='💔', callback_data='dislike_transfer')

kb_choose_transfer_liked = InlineKeyboardMarkup(row_width=2)

kb_choose_transfer_liked.insert(b2).insert(b1).add(b4).insert(b3)
