from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqllite_db
import telegram
from keyboards.transfer_kb import kb_transfer
from keyboards.choose_orders_liked_kb import kb_choose_orders_liked


id_liked_order = 0
all_liked_orders = []



async def switch_to_liked_orders(message: types.Message, order_test_message):
    global id_liked_order
    global all_liked_orders
    all_liked_orders = order_test_message
    print(all_liked_orders)
    id_liked_order = 0
    if len(all_liked_orders) == 0:
        await message.answer('К сожалению, у вас еще нет понравившихся заказов', parse_mode=telegram.ParseMode.HTML,
                             reply_markup=kb_transfer)
        return
    message_text = f'<b>------------------№ {all_liked_orders[id_liked_order][3]}------------------</b>\n' \
                   f'<b>{all_liked_orders[id_liked_order][1]}</b>\n' \
                   f'<b>Товар:</b> <i>{all_liked_orders[id_liked_order][4]}</i>\n' \
                   f'<b>Ссылка:</b> <i>{all_liked_orders[id_liked_order][5]}</i>\n' \
                   f'<b>Стоимость:</b> <i>{all_liked_orders[id_liked_order][6]}</i>\n' \
                   f'<b>Сумма вознаграждения:</b> <i>{all_liked_orders[id_liked_order][7]}</i>\n' \
                   f'<b>Откуда:</b> <i>{all_liked_orders[id_liked_order][9]}, ' \
                   f'{all_liked_orders[id_liked_order][8]}</i>\n' \
                   f'<b>Куда:</b> <i>{all_liked_orders[id_liked_order][10]}, ' \
                   f'{all_liked_orders[id_liked_order][11]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{all_liked_orders[id_liked_order][12]}</i>\n \n' \
                   f'<b>Пожаловаться</b> <i>report_{all_liked_orders[id_liked_order][0]}</i>'
                   #f'<a href="tg://msg?text={urllib.parse.quote("report_")}"> Пожаловаться </a>'


    await message.answer(message_text, parse_mode=telegram.ParseMode.HTML, reply_markup=kb_choose_orders_liked)

#next_order_choose_liked
@dp.callback_query_handler(lambda c: c.data == 'next_order_choose_liked')
#async def previous_transfer_choose_message(callback_query: types.CallbackQuery):
async def next_to_liked_orders(callback_query: types.CallbackQuery):
    global id_liked_order
    global all_liked_orders
    print(id_liked_order)
    print(all_liked_orders)
    print(len(all_liked_orders))
    if len(all_liked_orders) == id_liked_order:
        return
    id_liked_order +=1
    message_text = f'<b>------------------№ {all_liked_orders[id_liked_order][3]}------------------</b>\n' \
                   f'<b>{all_liked_orders[id_liked_order][1]}</b>\n' \
                   f'<b>Товар:</b> <i>{all_liked_orders[id_liked_order][4]}</i>\n' \
                   f'<b>Ссылка:</b> <i>{all_liked_orders[id_liked_order][5]}</i>\n' \
                   f'<b>Стоимость:</b> <i>{all_liked_orders[id_liked_order][6]}</i>\n' \
                   f'<b>Сумма вознаграждения:</b> <i>{all_liked_orders[id_liked_order][7]}</i>\n' \
                   f'<b>Откуда:</b> <i>{all_liked_orders[id_liked_order][9]}, ' \
                   f'{all_liked_orders[id_liked_order][8]}</i>\n' \
                   f'<b>Куда:</b> <i>{all_liked_orders[id_liked_order][10]}, ' \
                   f'{all_liked_orders[id_liked_order][11]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{all_liked_orders[id_liked_order][12]}</i>\n \n' \
                   f'<b>Пожаловаться</b> <i>report_{all_liked_orders[id_liked_order][0]}</i>'


    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                          text=message_text, reply_markup=kb_choose_orders_liked, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'previous_order_choose_liked')
async def previous_to_liked_orders(callback_query: types.CallbackQuery):
    global id_liked_order
    global all_liked_orders
    if len(all_liked_orders) - 1 == 0:
        return
    id_liked_order -= 1
    message_text = f'<b>------------------№ {all_liked_orders[id_liked_order][3]}------------------</b>\n' \
                   f'<b>{all_liked_orders[id_liked_order][1]}</b>\n' \
                   f'<b>Товар:</b> <i>{all_liked_orders[id_liked_order][4]}</i>\n' \
                   f'<b>Ссылка:</b> <i>{all_liked_orders[id_liked_order][5]}</i>\n' \
                   f'<b>Стоимость:</b> <i>{all_liked_orders[id_liked_order][6]}</i>\n' \
                   f'<b>Сумма вознаграждения:</b> <i>{all_liked_orders[id_liked_order][7]}</i>\n' \
                   f'<b>Откуда:</b> <i>{all_liked_orders[id_liked_order][9]}, ' \
                   f'{all_liked_orders[id_liked_order][8]}</i>\n' \
                   f'<b>Куда:</b> <i>{all_liked_orders[id_liked_order][10]}, ' \
                   f'{all_liked_orders[id_liked_order][11]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{all_liked_orders[id_liked_order][12]}</i>\n \n' \
                   f'<b>Пожаловаться</b> <i>report_{all_liked_orders[id_liked_order][0]}</i>'
    #f'<a href="tg://resolve?domain=brandsforfriends_bott&text=report_{all_liked_orders[id_liked_order][0]}> Пожаловаться </a>'

    #await message.answer(message_text, parse_mode=ParseMode.HTML, reply_markup=kb_choose_orders_liked)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                          text=message_text, reply_markup=kb_choose_orders_liked, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'dislike_order')
async def dislike_orders(callback_query: types.CallbackQuery):
    global id_liked_order
    global all_liked_orders
    # client_order_id, client_transfer_id, order_id
    await sqllite_db.sql_delete_liked_order(callback_query.from_user.id, all_liked_orders[id_liked_order][0],
                                               all_liked_orders[id_liked_order][3])

    all_liked_transfers = await sqllite_db.sql_get_liked_orders(callback_query.from_user.id)
    print(all_liked_transfers)
    if len(all_liked_transfers) == 0:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await callback_query.message.answer('У вас больше нет понравившихся исполнителей!')
        return
    if id_liked_order == 0:
        id_liked_order = -1
        await next_to_liked_orders(callback_query)
        return
    #d_liked_transfer += 1
    await previous_to_liked_orders(callback_query)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(next_to_liked_orders, lambda c: c.data == 'next_order_choose_liked')
    dp.register_callback_query_handler(previous_to_liked_orders, lambda c: c.data == 'previous_order_choose_liked')




