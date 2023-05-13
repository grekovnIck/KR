from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='>', callback_data='next_transfer_choose')
b2 = InlineKeyboardButton(text='<', callback_data='previous_transfer_choose')
b3 = InlineKeyboardButton(text='Связаться', callback_data='get_contact_transfer')
b4 = InlineKeyboardButton(text='❤️', callback_data='like_transfer')

kb_choose_transfer = InlineKeyboardMarkup(row_width=2)

kb_choose_transfer.insert(b2).insert(b1).add(b3).insert(b4)
