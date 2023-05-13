import datetime

from aiogram import types, Dispatcher
from create_bot import dp, bot
import messages_text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqllite_db
import telegram
from keyboards.client_get_phone_kb import kb_get_phone_number
from keyboards.client_select_type_kb import kb_client_select
from keyboards.transfer_kb import kb_transfer
from keyboards.order_kb import kb_order
from keyboards.choose_orders_liked_kb import kb_choose_orders_liked
from keyboards.choose_transfer_liked_kb import kb_choose_transfer_liked


id_liked_transfer = 0
all_liked_transfers = []


async def switch_to_liked_transfers(message: types.Message, transfer_test_message):
    global id_liked_transfer
    global all_liked_transfers
    all_liked_transfers = transfer_test_message
    #print(all_liked_transfers)
    id_liked_transfer = 0
    if len(all_liked_transfers) == 0:
        await message.answer('К сожалению, у вас еще нет понравившихся заказов', parse_mode=telegram.ParseMode.HTML,
                             reply_markup=kb_transfer)
        return
    message_text = f'<b>------------------№ {all_liked_transfers[id_liked_transfer][3]}------------------</b>\n' \
                   f'<b>{all_liked_transfers[id_liked_transfer][1]}</b>\n' \
                   f'<b>Откуда:</b> <i>{all_liked_transfers[id_liked_transfer][5]}, {all_liked_transfers[id_liked_transfer][4]}\n</i>' \
                   f'<b>Куда:</b> <i>{all_liked_transfers[id_liked_transfer][6]}, {all_liked_transfers[id_liked_transfer][7]}</i>\n' \
                   f'<b>Дата:</b> <i>{all_liked_transfers[id_liked_transfer][8]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{all_liked_transfers[id_liked_transfer][9]}</i>\n\n' \
                   f'<b>Пожаловаться</b> <i>report_{all_liked_transfers[id_liked_transfer][0]}</i>'
    await message.answer(message_text, parse_mode=telegram.ParseMode.HTML, reply_markup=kb_choose_transfer_liked)


@dp.callback_query_handler(lambda c: c.data == 'next_transfer_choose_liked')
async def next_to_liked_transfers(callback_query: types.CallbackQuery):
    global id_liked_transfer
    global all_liked_transfers
    if len(all_liked_transfers) - 1 == id_liked_transfer:
        return
    id_liked_transfer +=1
    message_text = f'<b>------------------№ {all_liked_transfers[id_liked_transfer][3]}------------------</b>\n' \
                   f'<b>{all_liked_transfers[id_liked_transfer][1]}</b>\n' \
                   f'<b>Откуда:</b> <i>{all_liked_transfers[id_liked_transfer][5]}, {all_liked_transfers[id_liked_transfer][4]}\n</i>' \
                   f'<b>Куда:</b> <i>{all_liked_transfers[id_liked_transfer][6]}, {all_liked_transfers[id_liked_transfer][7]}</i>\n' \
                   f'<b>Дата:</b> <i>{all_liked_transfers[id_liked_transfer][8]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{all_liked_transfers[id_liked_transfer][9]}</i>\n\n' \
                   f'<b>Пожаловаться</b> <i>report_{all_liked_transfers[id_liked_transfer][0]}</i>'

    #await message.answer(message_text, parse_mode=ParseMode.HTML, reply_markup=kb_choose_orders_liked)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                          text=message_text, reply_markup=kb_choose_transfer_liked, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'previous_transfer_choose_liked')
async def previous_to_liked_transfers(callback_query: types.CallbackQuery):
    global id_liked_transfer
    global all_liked_transfers
    if id_liked_transfer == 0:
        print('fdjkfhd')
        return
    id_liked_transfer -= 1
    message_text = f'<b>------------------№ {all_liked_transfers[id_liked_transfer][3]}------------------</b>\n' \
                   f'<b>{all_liked_transfers[id_liked_transfer][1]}</b>\n' \
                   f'<b>Откуда:</b> <i>{all_liked_transfers[id_liked_transfer][5]}, {all_liked_transfers[id_liked_transfer][4]}\n</i>' \
                   f'<b>Куда:</b> <i>{all_liked_transfers[id_liked_transfer][6]}, {all_liked_transfers[id_liked_transfer][7]}</i>\n' \
                   f'<b>Дата:</b> <i>{all_liked_transfers[id_liked_transfer][8]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{all_liked_transfers[id_liked_transfer][9]}</i>\n\n' \
                   f'<b>Пожаловаться</b> <i>report_{all_liked_transfers[id_liked_transfer][0]}</i>'

    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                          text=message_text, reply_markup=kb_choose_transfer_liked, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'dislike_transfer')
async def dislike_transfers(callback_query: types.CallbackQuery):
    global id_liked_transfer
    global all_liked_transfers
    await sqllite_db.sql_delete_liked_transfer(callback_query.from_user.id, all_liked_transfers[id_liked_transfer][0],
                                               all_liked_transfers[id_liked_transfer][3])

    all_liked_transfers = await sqllite_db.sql_get_liked_transfers(callback_query.from_user.id)
    print(all_liked_transfers)
    if len(all_liked_transfers) == 0:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await callback_query.message.answer('У вас больше нет понравившихся исполнителей!')
        return
    if id_liked_transfer == 0:
        id_liked_transfer = -1
        await next_to_liked_transfers(callback_query)
        return
    await previous_to_liked_transfers(callback_query)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(next_to_liked_transfers, lambda c: c.data == 'next_transfer_choose_liked')
    dp.register_callback_query_handler(previous_to_liked_transfers, lambda c: c.data == 'previous_transfer_choose_liked')
