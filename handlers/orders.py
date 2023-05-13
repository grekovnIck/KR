from aiogram import types, Dispatcher
from create_bot import dp, bot
import messages_text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqllite_db
import telegram
from keyboards.confirm_update_order import kb_confirm_order
from keyboards.back_delete_kb import kb_back_or_delete
from keyboards.order_kb import kb_order
from keyboards.back_kb import kb_back
from datetime import datetime
from keyboards.view_orders_kb import kb_view_order
from keyboards.choose_transfer_kb import kb_choose_transfer
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from objects.Status import Status


class FSMUpdateOrder(StatesGroup):
    name_product = State()
    link = State()
    price = State()
    remuneration = State()
    from_place_country = State()
    from_place_city = State()
    to_place_country = State()
    to_place_city = State()
    comment = State()
    final = State()


order_id_to_update = -1
order_id_to_update_tmp = -1
current_order_id = 1
all_orders = []
transfers = []
current_transfer_id = -1

@dp.message_handler(lambda message: 'Мои заказы' == message.text)
async def switch_transfer_menu(message : types.Message):
    global current_order_id
    global all_orders
    global order_id_to_update_tmp
    all_orders = await sqllite_db.sql_get_all_orders(message)
    if len(all_orders) == 0:
        await message.answer('У вас еще нет заказов', parse_mode=telegram.ParseMode.HTML, reply_markup=kb_order)
        return
    first_order = all_orders[0]
    order_id_to_update_tmp = first_order[0]
    contact = await sqllite_db.sql_check_transfer_exists(message.from_user.id, first_order[0])
    #print(contact)
    current_order_id = 1
    contact_info = ''
    first_order[0]
    order_id_to_update_tmp = first_order[0]
    if contact is None:
        contact_info = 'Перевозчик еще не найден'
    else:
        contact_info = f'<b>Ваш перевозчик:</b> <i>{contact[0][0]}</i>\n' \
                       f'<b>Номер телефона:</b> <i>{contact[0][1]}</i>\n' \
                       f'<b>Статус:</b> ' # TODO написать логику для статуса

    first_order_str = f'<b>------------- Заказ № {current_order_id} ---------------</b> \n' \
                      f'<b>Название товара:</b> <i>{first_order[1]}</i>\n' \
                      f'<b>Ссылка на товар:</b> <i>{first_order[2]}</i>\n' \
                      f'<b>Стоимость товара:</b> <i>{first_order[3]}</i>\n' \
                      f'<b>Сумма вознагрождения:</b> <i>{first_order[4]}</i>\n' \
                      f'<b>Страна покупки:</b> <i>{first_order[5]}</i>\n' \
                      f'<b>Город покупки:</b> <i>{first_order[6]}</i>\n' \
                      f'<b>Страна назначения:</b> <i>{first_order[7]}</i>\n' \
                      f'<b>Город назначения:</b> <i>{first_order[8]}</i>\n' \
                      f'<b>Комментарий:</b> <i>{first_order[9]}</i>\n' \
                      f'{contact_info}\n'
    await message.answer(f"У вас {len(all_orders)} заказов", parse_mode=telegram.ParseMode.HTML, reply_markup=kb_order)
    await message.answer(first_order_str, parse_mode=telegram.ParseMode.HTML, reply_markup=kb_view_order)



@dp.callback_query_handler(lambda c: c.data == 'previous')
async def previous_order_message(callback_query: types.CallbackQuery):
    global current_order_id
    global all_orders
    global order_id_to_update_tmp
    if current_order_id == 1:
        return

    current_order_id -= 1
    first_order = all_orders[current_order_id - 1]
    contact = await sqllite_db.sql_check_transfer_exists(callback_query.from_user.id, first_order[0])
    contact_info = ''
    if contact is None:
        contact_info = 'Перевозчик еще не найден'
    else:
        contact_info = f'<b>Ваш перевозчик:</b> <i>{contact[0][0]}</i>\n' \
                       f'<b>Номер телефона:</b> <i>{contact[0][1]}</i>\n' \
                       f'<b>Статус:</b> '  # TODO написать логику для статуса

    first_order_str =  f'<b>------------- Заказ № {current_order_id} ---------------</b> \n' \
                      f'<b>Название товара:</b> <i>{first_order[1]}</i>\n' \
                      f'<b>Ссылка на товар:</b> <i>{first_order[2]}</i>\n' \
                      f'<b>Стоимость товара:</b> <i>{first_order[3]}</i>\n' \
                      f'<b>Сумма вознагрождения:</b> <i>{first_order[4]}</i>\n' \
                      f'<b>Страна покупки:</b> <i>{first_order[5]}</i>\n' \
                      f'<b>Город покупки:</b> <i>{first_order[6]}</i>\n' \
                      f'<b>Страна назначения:</b> <i>{first_order[7]}</i>\n' \
                      f'<b>Город назначения:</b> <i>{first_order[8]}</i>\n' \
                      f'<b>Комментарий:</b> <i>{first_order[9]}</i>\n' \
                      f'{contact_info}\n'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=first_order_str, reply_markup=kb_view_order, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'next')
async def next_order_message(callback_query: types.CallbackQuery):
    global current_order_id
    global all_orders
    global order_id_to_update_tmp
    if current_order_id == len(all_orders):
        return

    current_order_id += 1
    first_order = all_orders[current_order_id - 1]
    order_id_to_update_tmp = first_order[0]
    contact = await sqllite_db.sql_check_transfer_exists(callback_query.from_user.id, first_order[0])
    contact_info = ''
    if contact is None:
        contact_info = 'Перевозчик еще не найден'
    else:
        contact_info = f'<b>Ваш перевозчик:</b> <i>{contact[0][0]}</i>\n' \
                       f'<b>Номер телефона:</b> <i>{contact[0][1]}</i>' \
                       f'<b>Статус:</b> '  # TODO написать логику для статуса

    first_order_str =  f'<b>------------- Заказ № {current_order_id} --------------</b> \n' \
                      f'<b>Название товара:</b> <i>{first_order[1]}</i>\n' \
                      f'<b>Ссылка на товар:</b> <i>{first_order[2]}</i>\n' \
                      f'<b>Стоимость товара:</b> <i>{first_order[3]}</i>\n' \
                      f'<b>Сумма вознагрождения:</b> <i>{first_order[4]}</i>\n' \
                      f'<b>Страна покупки:</b> <i>{first_order[5]}</i>\n' \
                      f'<b>Город покупки:</b> <i>{first_order[6]}</i>\n' \
                      f'<b>Страна назначения:</b> <i>{first_order[7]}</i>\n' \
                      f'<b>Город назначения:</b> <i>{first_order[8]}</i>\n' \
                      f'<b>Комментарий:</b> <i>{first_order[9]}</i>\n' \
                      f'{contact_info}\n'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=first_order_str, reply_markup=kb_view_order, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'edit')
async def edit_order_message(callback_query: types.CallbackQuery):
    global order_id_to_update
    global order_id_to_update_tmp
    global all_orders
    order_id_to_update = order_id_to_update_tmp
    await FSMUpdateOrder.name_product.set()
    await callback_query.message.answer(f'Введите название товара для заказа № {current_order_id}',
                                        reply_markup=kb_back_or_delete)


async def edit_order_message_again(message: types.Message):
    await FSMUpdateOrder.name_product.set()
    await message.answer(messages_text.GET_PRODUCT_NAME, reply_markup=kb_back)


async def load_product_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_order)
            await sqllite_db.sql_delete_order(order_id_to_update)
            await state.finish()
            return
        data['name'] = message.text  # TODO: написать обработчик написания названия товара
    await message.answer(messages_text.GET_PRODUCT_LINK)  # , reply_markup=get_phone_number)
    await FSMUpdateOrder.link.set()


#@dp.message_handler(state=FSMOrder.link)
async def load_product_link(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_order)
            await sqllite_db.sql_delete_order(order_id_to_update)
            await state.finish()
            return
        data['link'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_PRICE)  # , reply_markup=get_phone_number)
    await FSMUpdateOrder.price.set()


#@dp.message_handler(state=FSMOrder.price)
async def load_product_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_order)
            await sqllite_db.sql_delete_order(order_id_to_update)
            await state.finish()
            return
        data['price'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_GIFT)  # , reply_markup=get_phone_number)
    await FSMUpdateOrder.remuneration.set()


@dp.message_handler(state=FSMUpdateOrder.remuneration)
async def load_product_remuneration(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_order)
            await sqllite_db.sql_delete_order(order_id_to_update)
            await state.finish()
            return
        data['remuneration'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_FROM_COUNTRY)  # , reply_markup=get_phone_number)
    await FSMUpdateOrder.from_place_country.set()


#@dp.message_handler(state=FSMOrder.from_place_country)
async def load_product_from_place_country(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_order)
            await sqllite_db.sql_delete_order(order_id_to_update)
            await state.finish()
            return
        data['from_place_country'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_FROM_CITY)  # , reply_markup=get_phone_number)
    await FSMUpdateOrder.from_place_city.set()


#@dp.message_handler(state=FSMOrder.from_place_city)
async def load_product_from_place_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_order)
            await sqllite_db.sql_delete_order(order_id_to_update)
            await state.finish()
            return
        data['from_place_city'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_TO_COUNTRY)  # , reply_markup=get_phone_number)
    await FSMUpdateOrder.to_place_country.set()


#@dp.message_handler(state=FSMOrder.to_place_country)
async def load_product_to_place_country(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_order)
            await sqllite_db.sql_delete_order(order_id_to_update)
            await state.finish()
            return
        data['to_place_country'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_TO_CITY)  # , reply_markup=get_phone_number)
    await FSMUpdateOrder.to_place_city.set()


#@dp.message_handler(state=FSMOrder.to_place_city)
async def load_product_to_place_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
        elif message.text == 'Удалить':
            await message.answer(f"Заказ удален", reply_markup=kb_order)
            await sqllite_db.sql_delete_order(order_id_to_update)
            await state.finish()
            return
        data['to_place_city'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_COMMENT)  # , reply_markup=get_phone_number)
    await FSMUpdateOrder.comment.set()


#@dp.message_handler(state=FSMOrder.comment)
async def load_product_comment(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        data['comment'] = message.text  # TODO: написать обработчик корректности ссылки
    async with state.proxy() as data: #
        s = f'Отлично! Ваши данные записаны:\n' \
            f'<b>Название товара </b> <i>{data["name"]}</i>\n' \
            f'<b>Ссылка на товар:</b> <i>{data["link"]}</i>\n' \
            f'<b>Цена товара:</b> <i>{data["price"]}</i>\n' \
            f'<b>Сумма вознагрождения </b> <i>{data["remuneration"]}</i>\n' \
            f'<b>Страна отбытия:</b> <i>{data["from_place_country"]}</i>\n' \
            f'<b>Город покупки:</b> <i>{data["from_place_city"]}</i>\n' \
            f'<b>Страна назначения: </b> <i>{data["to_place_country"]}</i>\n' \
            f'<b>Город назначения:</b> <i>{data["to_place_city"]}</i>\n' \
            f'<b>Комментарий:</b> <i>{data["comment"]}</i>\n'
        await message.answer(s, parse_mode=telegram.ParseMode.HTML, reply_markup=kb_confirm_order)
        await FSMUpdateOrder.final.set()


#@dp.message_handler(state=FSMOrder.final)
async def load_product_final(message: types.Message, state=FSMContext):
    global transfer_id_to_update
    async with state.proxy() as data:
        if message.text == 'Обновить заказ':
            name = data["name"]
            link = data["link"]
            price = data["price"]
            remuneration = data["remuneration"]
            from_place_country = data["from_place_country"]
            from_place_city = data["from_place_city"]
            to_place_country = data["to_place_country"]
            to_place_city = data["to_place_city"]
            comment = data["comment"]
            user_id = message.from_user.id
            date = datetime.now()
            await sqllite_db.sql_update_order(order_id_to_update, [name, link, price, remuneration, from_place_country,
                                                                   from_place_city, to_place_country, to_place_city,
                                                                   comment, 1, user_id, date])
            await message.answer("Заказ обнавлен", reply_markup=kb_order)
            await state.finish()
        elif message.text == 'Внести изменения':
            await state.finish()
            await edit_order_message_again(message)
        elif message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()



@dp.callback_query_handler(lambda c: c.data == 'find_transfer')
async def find_transfers_message(callback_query: types.CallbackQuery):
    global current_order_id
    global all_orders
    global order_id_to_update_tmp
    global transfers
    global current_transfer_id

    current_transfer_id = 0

    from_country = all_orders[current_order_id - 1][5]
    from_city = all_orders[current_order_id - 1][6]
    to_city = all_orders[current_order_id - 1][8]
    to_country = all_orders[current_order_id - 1][7]
    transfers = await sqllite_db.sql_get_transfers_by_city(callback_query.from_user.id, from_country, from_city,
                                                           to_country, to_city)
    if len(transfers) != 0:
        await callback_query.message.answer(f"Найдено {len(transfers)} исполнителей!")
        message_text = f'<b>----------- Исполнитель № {transfers[current_transfer_id][3]} ------------</b>\n' \
                       f'<b>{transfers[current_transfer_id][1]}</b>\n' \
                       f'<b>Откуда:</b> <i>{transfers[current_transfer_id][5]}, {transfers[current_transfer_id][4]}\n</i>' \
                       f'<b>Куда:</b> <i>{transfers[current_transfer_id][6]}, {transfers[current_transfer_id][7]}</i>\n' \
                       f'<b>Дата:</b> <i>{transfers[current_transfer_id][8]}</i>\n' \
                       f'<b>Комментарий:</b> <i>{transfers[current_transfer_id][9]}</i>\n\n' \
                       f'<b>Пожаловаться</b> <i>report_{transfers[current_transfer_id][0]}</i>'
        await callback_query.message.answer(message_text, parse_mode=telegram.ParseMode.HTML,
                                            reply_markup=kb_choose_transfer)
    else:
        transfers = await sqllite_db.sql_get_transfers_by_country(callback_query.from_user.id, from_country, to_country,
                                                                  to_city)
        if len(transfers) == 0:
            await callback_query.message.answer("К сожалению, на ваш заказ нет актуальных исполнителей")
            return
        await callback_query.message.answer(
            "К сожалению, на ваш заказ нет актуальных исполнителей из указанного города")
        await callback_query.message.answer(f"Найдено {len(transfers)} исполнителей!")
        message_text = f'<b>----------- Исполнитель № {transfers[current_transfer_id][3]} ------------</b>\n' \
                       f'<b>{transfers[current_transfer_id][1]}</b>\n' \
                       f'<b>Откуда:</b> <i>{transfers[current_transfer_id][5]}, {transfers[current_transfer_id][4]}\n</i>' \
                       f'<b>Куда:</b> <i>{transfers[current_transfer_id][6]}, {transfers[current_transfer_id][7]}</i>\n' \
                       f'<b>Дата:</b> <i>{transfers[current_transfer_id][8]}</i>\n' \
                       f'<b>Комментарий:</b> <i>{transfers[current_transfer_id][9]}</i>\n\n' \
                       f'<b>Пожаловаться</b> <i>report_{transfers[current_transfer_id][0]}</i>'
        await callback_query.message.answer(message_text, parse_mode=telegram.ParseMode.HTML,
                                            reply_markup=kb_choose_transfer)


@dp.callback_query_handler(lambda c: c.data == 'next_transfer_choose')
async def next_transfer_choose_message(callback_query: types.CallbackQuery):
    global transfers
    global current_transfer_id
    if current_transfer_id == len(transfers) - 1:
        return
    current_transfer_id += 1
    message_text = f'<b>----------- Исполнитель № {transfers[current_transfer_id][3]} ------------</b>\n' \
                   f'<b>{transfers[current_transfer_id][1]}</b>\n' \
                   f'<b>Откуда:</b> <i>{transfers[current_transfer_id][5]}, {transfers[current_transfer_id][4]}\n</i>' \
                   f'<b>Куда:</b> <i>{transfers[current_transfer_id][6]}, {transfers[current_transfer_id][7]}</i>\n' \
                   f'<b>Дата:</b> <i>{transfers[current_transfer_id][8]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{transfers[current_transfer_id][9]}</i>\n\n' \
                   f'<b>Пожаловаться</b> <i>report_{transfers[current_transfer_id][0]}</i>'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=message_text, reply_markup=kb_choose_transfer, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'previous_transfer_choose')
async def previous_transfer_choose_message(callback_query: types.CallbackQuery):
    global current_order_id
    global all_orders
    global order_id_to_update_tmp
    global transfers
    global current_transfer_id
    if current_transfer_id == 0:
        return
    current_transfer_id -= 1
    message_text = f'<b>----------- Исполнитель № {transfers[current_transfer_id][3]} ------------</b>\n' \
                   f'<b>{transfers[current_transfer_id][1]}</b>\n' \
                   f'<b>Откуда:</b> <i>{transfers[current_transfer_id][5]}, {transfers[current_transfer_id][4]}\n</i>' \
                   f'<b>Куда:</b> <i>{transfers[current_transfer_id][6]}, {transfers[current_transfer_id][7]}</i>\n' \
                   f'<b>Дата:</b> <i>{transfers[current_transfer_id][8]}</i>\n' \
                   f'<b>Комментарий:</b> <i>{transfers[current_transfer_id][9]}</i>\n\n' \
                   f'<b>Пожаловаться</b> <i>report_{transfers[current_transfer_id][0]}</i>'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=message_text, reply_markup=kb_choose_transfer, parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'like_transfer')
async def like_transfer_choose_message(callback_query: types.CallbackQuery):
    global transfers
    global current_transfer_id
    client_order_id = callback_query.from_user.id
    print(transfers[current_transfer_id])
    client_transfer_id = transfers[current_transfer_id][0]
    transfer_id = transfers[current_transfer_id][3]
    await sqllite_db.sql_like_transfer([client_order_id, client_transfer_id, transfer_id, datetime.now()])
    await callback_query.message.answer(f'<b>Исполнитель № {transfers[current_transfer_id][3]} {transfers[current_transfer_id][1]} добавлен в Понравившиеся ❤️</b>', parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'get_contact_transfer')
async def get_contact_transfer_message(callback_query: types.CallbackQuery):
    global current_order_id
    global all_orders
    global transfers
    global current_transfer_id
    is_requests = await sqllite_db.sql_check_zero_status(all_orders[current_order_id - 1][11], transfers[current_transfer_id][0],
                                                        all_orders[current_order_id - 1][0], transfers[current_transfer_id][3],
                                                        0)
    if not is_requests:
        await callback_query.message.answer(f'Исполнитель уже получил от вас запрос')
        return

    await sqllite_db.sql_update_contract(all_orders[current_order_id - 1][11], transfers[current_transfer_id][0],
                                            all_orders[current_order_id - 1][0], transfers[current_transfer_id][3])
    await callback_query.message.answer(f'<b>Ура! Ваша анкета отправлена пользователю <code>{transfers[current_transfer_id][1]}</code>!</b>\n\n'
                                        f'<b>Как только он ее подтвердит, вы увидите его в разделе <code>Заказы</code></b>', parse_mode=telegram.ParseMode.HTML)

    print(transfers[current_transfer_id])
    await bot.send_message(chat_id=transfers[current_transfer_id][0], text='<b>Ура! У вас новый заказ!</b>',
                           parse_mode=telegram.ParseMode.HTML)
    contract_id = await sqllite_db.sql_get_contract_id(all_orders[current_order_id - 1][11], transfers[current_transfer_id][0],
                                                        all_orders[current_order_id - 1][0], transfers[current_transfer_id][3])
    await sqllite_db.sql_update_contract_status(contract_id, Status.REQUEST)
    order_contact_info = await sqllite_db.sql_get_contract_order_info(contract_id[0])
    first_order = all_orders[current_order_id - 1]
    print(first_order)
    first_order_str = f'<b>------------- Заказ № {transfers[current_transfer_id][3]} ---------------</b> \n' \
                      f'<a href="tg://user?id={order_contact_info[0]}" >{order_contact_info[1]}</a>\n' \
                      f'<b>Название товара:</b> <i>{first_order[1]}</i>\n' \
                      f'<b>Ссылка на товар:</b> <i>{first_order[2]}</i>\n' \
                      f'<b>Стоимость товара:</b> <i>{first_order[3]}</i>\n' \
                      f'<b>Сумма вознагрождения:</b> <i>{first_order[4]}</i>\n' \
                      f'<b>Откуда:</b> <i>{first_order[5]}, {first_order[6]}</i>\n' \
                      f'<b>Куда:</b> <i>{first_order[7]}, {first_order[8]}</i>\n' \
                      f'<b>Комментарий:</b> <i>{first_order[9]}</i>\n\n' \
                      f'<b>Пожаловаться</b> <i>report_{order_contact_info[0]}</i>'

    print(all_orders[current_order_id - 1])
    print(transfers[current_transfer_id])

    print(contract_id)
    print('bly')
    b1 = InlineKeyboardButton(text='Отклонить', callback_data=f'reject_contact_transfer_{contract_id[0]}')
    b2 = InlineKeyboardButton(text='Связаться', callback_data=f'give_contact_transfer_{contract_id[0]}')

    kb_confirm_new_transfer = InlineKeyboardMarkup(row_width=2)

    kb_confirm_new_transfer.add(b2).add(b1)

    await bot.send_message(chat_id=transfers[current_transfer_id][0], text=first_order_str,
                           parse_mode=telegram.ParseMode.HTML, reply_markup=kb_confirm_new_transfer)



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(switch_transfer_menu, lambda message: 'Мои заказы' == message.text)
    dp.register_callback_query_handler(previous_order_message, lambda c: c.data == 'previous')
    dp.register_callback_query_handler(next_order_message, lambda c: c.data == 'next')
    dp.register_callback_query_handler(edit_order_message, lambda c: c.data == 'edit')
    dp.register_message_handler(load_product_name, state=FSMUpdateOrder.name_product)
    dp.register_message_handler(load_product_link, state=FSMUpdateOrder.link)
    dp.register_message_handler(load_product_price, state=FSMUpdateOrder.price)
    dp.register_message_handler(load_product_remuneration, state=FSMUpdateOrder.remuneration)
    dp.register_message_handler(load_product_from_place_country, state=FSMUpdateOrder.from_place_country)
    dp.register_message_handler(load_product_from_place_city, state=FSMUpdateOrder.from_place_city)
    dp.register_message_handler(load_product_to_place_country, state=FSMUpdateOrder.to_place_country)
    dp.register_message_handler(load_product_to_place_city, state=FSMUpdateOrder.to_place_city)
    dp.register_message_handler(load_product_comment, state=FSMUpdateOrder.comment)
    dp.register_message_handler(load_product_final, state=FSMUpdateOrder.final)
    dp.callback_query_handler(find_transfers_message, lambda c: c.data == 'find_transfer')
    dp.callback_query_handler(next_transfer_choose_message, lambda c: c.data == 'next_transfer_choose')
    dp.callback_query_handler(previous_transfer_choose_message, lambda c: c.data == 'previous_transfer_choose')



