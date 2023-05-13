from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='Отклонить', callback_data='reject_contact_order')
b2 = InlineKeyboardButton(text='Связаться', callback_data='give_contact_order')

kb_confirm_new_order = InlineKeyboardMarkup(row_width=2)

kb_confirm_new_order.add(b2).add(b1)
