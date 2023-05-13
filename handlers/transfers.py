from aiogram import types, Dispatcher
from create_bot import dp, bot
import messages_text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqllite_db
import telegram
from keyboards.back_delete_kb import kb_back_or_delete
from keyboards.back_kb import kb_back
from datetime import datetime
from keyboards.view_transfer_kb import kb_view_order
from keyboards.transfer_kb import kb_transfer
from keyboards.confirm_update_transfer_kb import kb_confirm_transfer_update
from keyboards.choose_orders_kb import kb_choose_orders
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FSMUpdateTransfer(StatesGroup):
    from_place_country = State()
    from_place_city = State()
    to_place_country = State()
    to_place_city = State()
    date_transfer = State()
    comment = State()
    final = State()


transfer_id_to_update = -1
transfer_id_to_update_tmp = -1
current_transfer_id = 1
all_transfers = []
orders = []
current_order_id = 0

@dp.message_handler(lambda message: 'Мои перевозки' == message.text)
async def switch_transfer_menu(message: types.Message):
    global current_transfer_id
    global all_transfers
    global transfer_id_to_update_tmp
    all_transfers = await sqllite_db.sql_get_all_transfers(message)
    if len(all_transfers) == 0:
        await message.answer('У вас еще нет поездок', parse_mode=telegram.ParseMode.HTML, reply_markup=kb_transfer)
        return
    first_order = all_transfers[0]
    transfer_id_to_update_tmp = first_order[0]
    contact = await sqllite_db.sql_check_transfer_exists(message.from_user.id, first_order[0])
    # print(contact)
    current_transfer_id = 1
    contact_info = ''
    transfer_id_to_update_tmp = first_order[0]
    if contact is None:
        contact_info = 'Заказчик еще не найден'
    else:
        contact_info = f'<b>Ваш перевозчик:</b> <i>{contact[0][0]}</i>\n' \
                       f'<b>Номер телефона:</b> <i>{contact[0][1]}</i>\n' \
                       f'<b>Статус:</b> '  # TODO написать логику для статуса

    first_order_str = f'<b>------------- Поездка № {current_transfer_id} --------------</b> \n' \
                        f'<b>Страна отбытия:</b> <i>{first_order[1]}</i>\n' \
                        f'<b>Город отбытия:</b> <i>{first_order[2]}</i>\n' \
                        f'<b>Страна назначения: </b> <i>{first_order[3]}</i>\n' \
                        f'<b>Город назначения:</b> <i>{first_order[4]}</i>\n' \
                        f'<b>Дата отбытия:</b> <i>{first_order[5]}</i>\n' \
                        f'<b>Комментарий:</b> <i>{first_order[6]}</i>\n'\
                        f'{contact_info}\n'
    await message.answer(first_order_str, parse_mode=telegram.ParseMode.HTML, reply_markup=kb_view_order)
    await message.answer(f"У вас размещенных поездок - <b>{len(all_transfers)}</b>", parse_mode=telegram.ParseMode.HTML,
                         reply_markup=kb_transfer)


# обработчик для inline-кнопки
@dp.callback_query_handler(lambda c: c.data == 'previous_transfer')
#@dp.callback_query_handler(lambda message: 'previous' == message.text)
async def previous_transfer_message(callback_query: types.CallbackQuery):
    global current_transfer_id
    global all_transfers
    global transfer_id_to_update_tmp
    if current_transfer_id == 1:
        return

    current_transfer_id -= 1
    first_order = all_transfers[current_transfer_id - 1]
    contact = await sqllite_db.sql_check_transfer_exists(callback_query.from_user.id, first_order[0])
    contact_info = ''
    if contact is None:
        contact_info = 'Перевозчик еще не найден'
    else:
        contact_info = f'<b>Ваш перевозчик:</b> <i>{contact[0][0]}</i>\n' \
                       f'<b>Номер телефона:</b> <i>{contact[0][1]}</i>\n' \
                       f'<b>Статус:</b> '  # TODO написать логику для статуса

    first_order_str = f'<b>------------- Поездка № {current_transfer_id} -------------</b> \n' \
                        f'<b>Страна отбытия:</b> <i>{first_order[1]}</i>\n' \
                        f'<b>Город отбытия:</b> <i>{first_order[2]}</i>\n' \
                        f'<b>Страна назначения: </b> <i>{first_order[3]}</i>\n' \
                        f'<b>Город назначения:</b> <i>{first_order[4]}</i>\n' \
                        f'<b>Дата отбытия:</b> <i>{first_order[5]}</i>\n' \
                        f'<b>Комментарий:</b> <i>{first_order[6]}</i>\n'\
                        f'{contact_info}\n'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=first_order_str, reply_markup=kb_view_order, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'next_transfer')
#@dp.callback_query_handler(lambda message: 'next' == message.text)
async def next_order_message(callback_query: types.CallbackQuery):
    global current_transfer_id
    global all_transfers
    global transfer_id_to_update_tmp
    if current_transfer_id == len(all_transfers):
        return

    current_transfer_id += 1
    first_order = all_transfers[current_transfer_id - 1]
    #print(first_order[0])
    #print('gfjkgfjlg')
    transfer_id_to_update_tmp = first_order[0]
    contact = await sqllite_db.sql_check_transfer_exists(callback_query.from_user.id, first_order[0])
    contact_info = ''
    if contact is None:
        contact_info = 'Перевозчик еще не найден'
    else:
        contact_info = f'<b>Ваш перевозчик:</b> <i>{contact[0][0]}</i>\n' \
                       f'<b>Номер телефона:</b> <i>{contact[0][1]}</i>' \
                       f'<b>Статус:</b> '  # TODO написать логику для статуса

    first_order_str = f'<b>------------- Поездка № {current_transfer_id} -------------</b> \n' \
                        f'<b>Страна отбытия:</b> <i>{first_order[1]}</i>\n' \
                        f'<b>Город отбытия:</b> <i>{first_order[2]}</i>\n' \
                        f'<b>Страна назначения: </b> <i>{first_order[3]}</i>\n' \
                        f'<b>Город назначения:</b> <i>{first_order[4]}</i>\n' \
                        f'<b>Дата отбытия:</b> <i>{first_order[5]}</i>\n' \
                        f'<b>Комментарий:</b> <i>{first_order[6]}</i>\n'\
                        f'{contact_info}\n'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=first_order_str, reply_markup=kb_view_order, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'edit_transfer')
#@dp.callback_query_handler(lambda message: 'next' == message.text)
async def edit_transfer_message(callback_query: types.CallbackQuery):
    global transfer_id_to_update
    global transfer_id_to_update_tmp
    transfer_id_to_update = transfer_id_to_update_tmp
    await FSMUpdateTransfer.from_place_country.set()
    await callback_query.message.answer(f'Введите город отбытия для поездки № {current_transfer_id}', reply_markup=kb_back_or_delete)


async def edit_transfer_message_again(message: types.Message):
    await FSMUpdateTransfer.from_place_country.set()
    await message.answer(messages_text.GET_TRANSFER_FROM_COUNTRY, reply_markup=kb_back)


@dp.message_handler(state=FSMUpdateTransfer.from_place_country)
async def load_transfer_from_place_country(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await sqllite_db.sql_delete_transfer(transfer_id_to_update)
            await message.answer(f"Заказ удален", reply_markup=kb_transfer)
            await state.finish()
            return
        data['from_place_country'] = message.text  # TODO: написать обработчик написания названия товара
    await message.answer(messages_text.GET_TRANSFER_FROM_CITY)  # , reply_markup=get_phone_number)
    await FSMUpdateTransfer.from_place_city.set()


@dp.message_handler(state=FSMUpdateTransfer.from_place_city)
async def load_transfer_from_place_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_transfer)
            await sqllite_db.sql_delete_transfer(transfer_id_to_update)
            await state.finish()
            return
        data['from_place_city'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_TRANSFER_TO_COUNTRY)  # , reply_markup=get_phone_number)
    await FSMUpdateTransfer.to_place_country.set()


@dp.message_handler(state=FSMUpdateTransfer.to_place_country)
async def load_transfer_to_place_country(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await sqllite_db.sql_delete_transfer(transfer_id_to_update)
            await state.finish()
            return
        data['to_place_country'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_TRANSFER_TO_CITY)  # , reply_markup=get_phone_number)
    await FSMUpdateTransfer.to_place_city.set()


@dp.message_handler(state=FSMUpdateTransfer.to_place_city)
async def load_transfer_to_place_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await sqllite_db.sql_delete_transfer(transfer_id_to_update)
            await message.answer(f"Заказ удален", reply_markup=kb_transfer)
            await state.finish()
            return
        data['to_place_city'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_TRANSFER_DATE)  # , reply_markup=get_phone_number)
    await FSMUpdateTransfer.date_transfer.set()


@dp.message_handler(state=FSMUpdateTransfer.date_transfer)
async def load_transfer_date_transfer(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_transfer)
            await sqllite_db.sql_delete_transfer(transfer_id_to_update)
            await state.finish()
            return
        data['date_transfer'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_TRANSFER_COMMENT)  # , reply_markup=get_phone_number)
    await FSMUpdateTransfer.comment.set()


@dp.message_handler(state=FSMUpdateTransfer.comment)
async def load_transfer_comment(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        data['comment'] = message.text  # TODO: написать обработчик корректности ссылки
    async with state.proxy() as data: #
        s = f'Отлично! Ваши данные записаны:\n' \
            f'<b>Страна отбытия:</b> <i>{data["from_place_country"]}</i>\n' \
            f'<b>Город отбытия:</b> <i>{data["from_place_city"]}</i>\n' \
            f'<b>Страна назначения: </b> <i>{data["to_place_country"]}</i>\n' \
            f'<b>Город назначения:</b> <i>{data["to_place_city"]}</i>\n' \
            f'<b>Дата отбытия:</b> <i>{data["date_transfer"]}</i>\n' \
            f'<b>Комментарий:</b> <i>{data["comment"]}</i>\n'
        await message.answer(s, parse_mode=telegram.ParseMode.HTML, reply_markup=kb_confirm_transfer_update)
    await FSMUpdateTransfer.final.set()


@dp.message_handler(state=FSMUpdateTransfer.final)
async def load_transfer_final(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if message.text == 'Обновить данные о поездке':
            from_place_country = data["from_place_country"]
            from_place_city = data["from_place_city"]
            to_place_country = data["to_place_country"]
            to_place_city = data["to_place_city"]
            comment = data["comment"]
            date_transfer = data["date_transfer"]
            user_id = message.from_user.id
            date = datetime.now()
            await sqllite_db.sql_update_transfer(transfer_id_to_update, [from_place_country, from_place_city,
                                               to_place_country, to_place_city, comment, date_transfer, 1, user_id,
                                               date])
            await message.answer("Ура! Транзит размещен", reply_markup=kb_transfer)
            await state.finish()
        elif message.text == 'Внести изменения':
            await state.finish()
            await edit_transfer_message_again(message)
        elif message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()






@dp.callback_query_handler(lambda c: c.data == 'find_orders')
#@dp.callback_query_handler(lambda message: 'previous' == message.text)
async def find_orders_message(callback_query: types.CallbackQuery):
    global all_transfers
    global current_order_id
    global current_transfer_id
    global orders
    global current_order_id
    print(all_transfers)
    print(transfer_id_to_update_tmp)
    # from_country = all_transfers[transfer_id_to_update_tmp - 1][1]
    # from_city = all_transfers[transfer_id_to_update_tmp - 1][2]
    # to_country = all_transfers[transfer_id_to_update_tmp - 1][3]
    # to_city = all_transfers[transfer_id_to_update_tmp - 1][4]
    from_country = all_transfers[current_transfer_id - 1][1]
    from_city = all_transfers[current_transfer_id - 1][2]
    to_country = all_transfers[current_transfer_id - 1][3]
    to_city = all_transfers[current_transfer_id - 1][4]

    current_order_id = 0
    orders = await sqllite_db.sql_get_orders_by_city(callback_query.from_user.id, from_country, from_city, to_country,
                                                     to_city)
    if len(orders) != 0:
        await callback_query.message.answer(f"Найдено {len(orders)} исполнителей!")
        message_text = f'<b>-------------- Заказ № {orders[current_order_id][3]}-------------</b>\n' \
                       f'<b>{orders[current_order_id][1]}</b>\n' \
                       f'<b>Товар:</b> <i>{orders[current_order_id][4]}</i>\n' \
                       f'<b>Ссылка:</b> <i>{orders[current_order_id][5]}</i>\n' \
                       f'<b>Стоимость:</b> <i>{orders[current_order_id][6]}</i>\n' \
                       f'<b>Сумма вознаграждения:</b> <i>{orders[current_order_id][7]}</i>\n' \
                       f'<b>Откуда:</b> <i>{orders[current_order_id][9]}, {orders[current_order_id][8]}</i>\n' \
                       f'<b>Куда:</b> <i>{orders[current_order_id][10]}, {orders[current_order_id][11]}</i>\n' \
                       f'<b>Комментарий:</b> <i>{orders[current_order_id][12]}</i>\n \n' \
                       f'<b>Пожаловаться</b> <i>report_{orders[current_order_id][0]}</i>'

        await callback_query.message.answer(message_text, parse_mode=telegram.ParseMode.HTML,
                                            reply_markup=kb_choose_orders)
    else:
        await callback_query.message.answer(
            "К сожалению, на вашу поездку нет актуальных исполнителей из указанного города")

        orders = await sqllite_db.sql_get_orders_by_country(callback_query.from_user.id, from_country, to_country,
                                                          to_city)
        print(orders[0])
        if len(orders) == 0:
            await callback_query.message.answer("К сожалению, на ваш заказ нет актуальных заказов")
            return


        await callback_query.message.answer(f"Найдено {len(orders)} заказов!")

        message_text = f'<b>-------------- Заказ № {orders[current_order_id][3]}-------------</b>\n' \
                       f'<b>{orders[current_order_id][1]}</b>\n'\
                       f'<b>Товар:</b> <i>{orders[current_order_id][4]}</i>\n' \
                       f'<b>Ссылка:</b> <i>{orders[current_order_id][5]}</i>\n' \
                       f'<b>Стоимость:</b> <i>{orders[current_order_id][6]}</i>\n' \
                       f'<b>Сумма вознаграждения:</b> <i>{orders[current_order_id][7]}</i>\n' \
                       f'<b>Откуда:</b> <i>{orders[current_order_id][9]}, {orders[current_order_id][8]}</i>\n' \
                       f'<b>Куда:</b> <i>{orders[current_order_id][10]}, {orders[current_order_id][11]}</i>\n' \
                       f'<b>Комментарий:</b> <i>{orders[current_order_id][12]}</i>\n \n' \
                       f'<b>Пожаловаться</b> <i>report_{orders[current_order_id][0]}</i>'
        await callback_query.message.answer(message_text, parse_mode=telegram.ParseMode.HTML,
                                            reply_markup=kb_choose_orders)


@dp.callback_query_handler(lambda c: c.data == 'next_order_choose')
async def next_order_choose_message(callback_query: types.CallbackQuery):
    global current_order_id
    global orders
    #global current_transfer_id
    print(current_transfer_id)
    print(len(orders) - 1)
    if current_order_id == len(orders) - 1:
        return
    current_order_id += 1
    message_text = f'<b>-------------- Заказ № {orders[current_order_id][3]}-------------</b>\n' \
                   f'<b>{orders[current_order_id][1]}</b>\n' \
                   f'<b>Товар:</b> <i>{orders[current_order_id][4]}</i>\n' \
                   f'<b>Ссылка:</b> <i>{orders[current_order_id][5]}</i>\n' \
                   f'<b>Стоимость:</b> <i>{orders[current_order_id][6]}</i>\n' \
                   f'<b>Сумма вознаграждения:</b> <i>{orders[current_order_id][7]}</i>\n' \
                   f'<b>Откуда:</b> <i>{orders[current_order_id][9]}, {orders[current_order_id][8]}</i>\n' \
                   f'<b>Куда:</b> <i>{orders[current_order_id][10]}, {orders[current_order_id][11]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{orders[current_order_id][12]}</i>\n \n' \
                   f'<b>Пожаловаться</b> <i>report_{orders[current_order_id][0]}</i>'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=message_text, reply_markup=kb_choose_orders, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'previous_order_choose')
async def previous_order_choose_message(callback_query: types.CallbackQuery):
    global orders
    global current_order_id
    if current_order_id == 0:
        return
    current_order_id -= 1
    print(orders[current_order_id])
    message_text = f'<b>-------------- Заказ № {orders[current_order_id][3]}-------------</b>\n' \
                   f'<b>{orders[current_order_id][1]}</b>\n' \
                   f'<b>Товар:</b> <i>{orders[current_order_id][4]}</i>\n' \
                   f'<b>Ссылка:</b> <i>{orders[current_order_id][5]}</i>\n' \
                   f'<b>Стоимость:</b> <i>{orders[current_order_id][6]}</i>\n' \
                   f'<b>Сумма вознаграждения:</b> <i>{orders[0][7]}</i>\n' \
                   f'<b>Откуда:</b> <i>{orders[current_order_id][9]}, {orders[current_order_id][8]}</i>\n' \
                   f'<b>Куда:</b> <i>{orders[current_order_id][10]}, {orders[current_order_id][11]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{orders[current_order_id][12]}</i>\n \n' \
                   f'<b>Пожаловаться</b> <i>report_{orders[current_order_id][0]}</i>'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=message_text, reply_markup=kb_choose_orders, parse_mode=telegram.ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data == 'like_order')
async def like_order_choose_message(callback_query: types.CallbackQuery):
    global current_order_id
    global orders
    global current_transfer_id
    client_transfer_id = callback_query.from_user.id
    client_order_id = orders[current_order_id][0]
    order_id = orders[current_order_id][3]
    await sqllite_db.sql_like_order([client_order_id, client_transfer_id, order_id, datetime.now()])
    await callback_query.message.answer(f'<b>Заказ № {orders[current_order_id][3]} {orders[current_order_id][1]} добавлен в Понравившиеся ❤️</b>', parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'get_contact_order')
async def like_transfer_choose_message(callback_query: types.CallbackQuery):
    global current_transfer_id
    global current_order_id
    global all_transfers
    global orders
    print(all_transfers)
    print(current_transfer_id)
    print(orders)
    print(current_order_id)
    # client_order_id, client_transfer_id, transfer_id, order_id, status: Status
    is_requests = await sqllite_db.sql_check_zero_status(orders[current_order_id][0], all_transfers[current_transfer_id - 1][8],
                                        orders[current_order_id][3], all_transfers[current_transfer_id - 1][0], 0)
    if not is_requests:
        await callback_query.message.answer(f'Заказчик уже получил от вас запрос')
        return
    await sqllite_db.sql_update_contract(orders[current_order_id][0], all_transfers[current_transfer_id - 1][8],
                                        orders[current_order_id][3], all_transfers[current_transfer_id - 1][0])
    await callback_query.message.answer(f'<b>Ура! Ваша анкета отправлена пользователю <code>{orders[current_order_id][1]}</code>!</b>\n\n'
                                        f'<b>Как только он ее подтвердит, вы увидите его в разделе <code>Поездки</code></b>', parse_mode=telegram.ParseMode.HTML)
    #print(all_transfers[current_order_id])
    await bot.send_message(chat_id=orders[current_order_id][0], text='<b>Ура! Откликнулся новый исполнитель!</b>',
                           parse_mode=telegram.ParseMode.HTML)

    print(all_transfers[current_transfer_id - 1])
    contract_id = await sqllite_db.sql_get_contract_id(orders[current_order_id][0], all_transfers[current_transfer_id - 1][8],
                                        orders[current_order_id][3], all_transfers[current_transfer_id - 1][0])
    print(contract_id)
    transfer_contact_info = await sqllite_db.sql_get_contract_transfer_info(contract_id[0])
    # TODO  и встевить ее сюда
    message_text = f'<b>----------- Поездка № {transfer_contact_info[2]} ------------</b>\n' \
                   f'<a href="tg://user?id={transfer_contact_info[0]}" >{transfer_contact_info[1]}</a>\n' \
                   f'<b>Откуда:</b> <i>{all_transfers[current_transfer_id - 1][1]}, {all_transfers[current_transfer_id - 1][2]}\n</i>' \
                   f'<b>Куда:</b> <i>{all_transfers[current_transfer_id - 1][3]}, {all_transfers[current_transfer_id - 1][4]}</i>\n' \
                   f'<b>Дата:</b> <i>{all_transfers[current_transfer_id - 1][5]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{all_transfers[current_transfer_id - 1][6]}</i>\n\n' \
                   f'<b>Пожаловаться</b> <i>report_{transfer_contact_info[0]}</i>'


    print(contract_id)
    print('bly')
    b1 = InlineKeyboardButton(text='Отклонить', callback_data=f'reject_contact_order_{contract_id[0]}')
    b2 = InlineKeyboardButton(text='Связаться', callback_data=f'give_contact_order_{contract_id[0]}')

    kb_confirm_new_order = InlineKeyboardMarkup(row_width=2)

    kb_confirm_new_order.add(b2).add(b1)

    await bot.send_message(chat_id=orders[current_order_id][0], text=message_text,
                           parse_mode=telegram.ParseMode.HTML, reply_markup=kb_confirm_new_order)


def register_handlers_client(dp: Dispatcher):
    dp.callback_query_handler(edit_transfer_message, lambda message: 'Разместить перевозку' == message.text)
    dp.register_message_handler(load_transfer_from_place_country, state=FSMUpdateTransfer.from_place_country)
    dp.register_message_handler(load_transfer_from_place_city, state=FSMUpdateTransfer.from_place_city)
    dp.register_message_handler(load_transfer_to_place_country, state=FSMUpdateTransfer.to_place_country)
    dp.register_message_handler(load_transfer_to_place_city, state=FSMUpdateTransfer.to_place_city)
    dp.register_message_handler(load_transfer_date_transfer, state=FSMUpdateTransfer.date_transfer)
    dp.register_message_handler(load_transfer_comment, state=FSMUpdateTransfer.comment)
    dp.register_message_handler(load_transfer_final, state=FSMUpdateTransfer.final)
    dp.callback_query_handler(find_orders_message, lambda c: c.data == 'find_orders')
    dp.callback_query_handler(next_order_choose_message, lambda c: c.data == 'next_order_choose')
    dp.callback_query_handler(previous_order_choose_message, lambda c: c.data == 'previous_order_choose')
