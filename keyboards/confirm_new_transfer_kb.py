from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='Отклонить', callback_data='reject_contact_transfer')
b2 = InlineKeyboardButton(text='Связаться', callback_data='give_contact_transfer' )


kb_confirm_new_transfer = InlineKeyboardMarkup(row_width=2)

kb_confirm_new_transfer.add(b2).add(b1)
