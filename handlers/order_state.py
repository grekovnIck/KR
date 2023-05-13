from aiogram import types, Dispatcher
from create_bot import dp
import messages_text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqllite_db
import telegram
from keyboards.confirm_order_kb import kb_confirm_order
from keyboards.order_kb import kb_order
from keyboards.back_kb import kb_back
from datetime import datetime


class FSMOrder(StatesGroup):
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


@dp.message_handler(lambda message: 'Разместить заказ' == message.text)
async def start_create_order(message: types.Message):
    await FSMOrder.name_product.set()
    await message.answer(messages_text.GET_PRODUCT_NAME, reply_markup=kb_back)


@dp.message_handler(state=FSMOrder.name_product)
async def load_product_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        data['name'] = message.text  # TODO: написать обработчик написания названия товара
    await message.answer(messages_text.GET_PRODUCT_LINK)  # , reply_markup=get_phone_number)
    await FSMOrder.link.set()


@dp.message_handler(state=FSMOrder.link)
async def load_product_link(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        data['link'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_PRICE)  # , reply_markup=get_phone_number)
    await FSMOrder.price.set()


@dp.message_handler(state=FSMOrder.price)
async def load_product_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        data['price'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_GIFT)  # , reply_markup=get_phone_number)
    await FSMOrder.remuneration.set()


@dp.message_handler(state=FSMOrder.remuneration)
async def load_product_remuneration(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        data['remuneration'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_FROM_COUNTRY)  # , reply_markup=get_phone_number)
    await FSMOrder.from_place_country.set()


@dp.message_handler(state=FSMOrder.from_place_country)
async def load_product_from_place_country(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        data['from_place_country'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_FROM_CITY)  # , reply_markup=get_phone_number)
    await FSMOrder.from_place_city.set()


@dp.message_handler(state=FSMOrder.from_place_city)
async def load_product_from_place_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        data['from_place_city'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_TO_COUNTRY)  # , reply_markup=get_phone_number)
    await FSMOrder.to_place_country.set()


@dp.message_handler(state=FSMOrder.to_place_country)
async def load_product_to_place_country(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        data['to_place_country'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_TO_CITY)  # , reply_markup=get_phone_number)
    await FSMOrder.to_place_city.set()


@dp.message_handler(state=FSMOrder.to_place_city)
async def load_product_to_place_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
        data['to_place_city'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_PRODUCT_COMMENT)  # , reply_markup=get_phone_number)
    await FSMOrder.comment.set()


@dp.message_handler(state=FSMOrder.comment)
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
        await FSMOrder.final.set()

    # output = [data['id'], data['name'], data['phone']]
    # await sqllite.sql_add_commands(output)
    # await state.finish()


@dp.message_handler(state=FSMOrder.final)
async def load_product_final(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if message.text == 'Разместить заказ':
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
            await sqllite_db.sql_add_order([name, link, price, remuneration, from_place_country, from_place_city,
                                   to_place_country, to_place_city, comment, 1, user_id, date])
            await message.answer("Ура! Заказ размещен", reply_markup=kb_order)
            await state.finish()
        elif message.text == 'Внести изменения':
            await state.finish()
            await start_create_order(message)
        elif message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_create_order, lambda message: 'Разместить заказ' == message.text)
    dp.register_message_handler(load_product_name, state=FSMOrder.name_product)
    dp.register_message_handler(load_product_link, state=FSMOrder.link)
    dp.register_message_handler(load_product_price, state=FSMOrder.price)
    dp.register_message_handler(load_product_remuneration, state=FSMOrder.remuneration)
    dp.register_message_handler(load_product_from_place_country, state=FSMOrder.from_place_country)
    dp.register_message_handler(load_product_from_place_city, state=FSMOrder.from_place_city)
    dp.register_message_handler(load_product_to_place_country, state=FSMOrder.to_place_country)
    dp.register_message_handler(load_product_to_place_city, state=FSMOrder.to_place_city)
    dp.register_message_handler(load_product_comment, state=FSMOrder.comment)
    dp.register_message_handler(load_product_final, state=FSMOrder.final)

