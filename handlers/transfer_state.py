from aiogram import types, Dispatcher
from create_bot import dp, bot
import messages_text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqllite_db
import telegram
from keyboards import kb_back
from keyboards.confirm_transfer_kb import kb_confirm_transfer
from keyboards.transfer_kb import kb_transfer
from datetime import datetime


class FSMTransfer(StatesGroup):
    from_place_country = State()
    from_place_city = State()
    to_place_country = State()
    to_place_city = State()
    date_transfer = State()
    comment = State()
    final = State()


#async def get_back(message: types.Message, state=FSMContext):


@dp.message_handler(lambda message: 'Разместить перевозку' == message.text)
async def start_create_transit(message: types.Message):
    await FSMTransfer.from_place_country.set()
    await message.answer(messages_text.GET_TRANSFER_FROM_COUNTRY, reply_markup=kb_back)


@dp.message_handler(state=FSMTransfer.from_place_country)
async def load_transfer_from_place_country(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        data['from_place_country'] = message.text  # TODO: написать обработчик написания названия товара
    await message.answer(messages_text.GET_TRANSFER_FROM_CITY)  # , reply_markup=get_phone_number)
    await FSMTransfer.from_place_city.set()


@dp.message_handler(state=FSMTransfer.from_place_city)
async def load_transfer_from_place_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        data['from_place_city'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_TRANSFER_TO_COUNTRY)  # , reply_markup=get_phone_number)
    await FSMTransfer.to_place_country.set()


@dp.message_handler(state=FSMTransfer.to_place_country)
async def load_transfer_to_place_country(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        data['to_place_country'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_TRANSFER_TO_CITY)  # , reply_markup=get_phone_number)
    await FSMTransfer.to_place_city.set()


@dp.message_handler(state=FSMTransfer.to_place_city)
async def load_transfer_to_place_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        data['to_place_city'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_TRANSFER_DATE)  # , reply_markup=get_phone_number)
    await FSMTransfer.date_transfer.set()


@dp.message_handler(state=FSMTransfer.date_transfer)
async def load_transfer_date_transfer(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()
            return
        data['date_transfer'] = message.text  # TODO: написать обработчик корректности ссылки
    await message.answer(messages_text.GET_TRANSFER_COMMENT)  # , reply_markup=get_phone_number)
    await FSMTransfer.comment.set()


@dp.message_handler(state=FSMTransfer.comment)
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
        await message.answer(s, parse_mode=telegram.ParseMode.HTML, reply_markup=kb_confirm_transfer)
    await FSMTransfer.final.set()


@dp.message_handler(state=FSMTransfer.final)
async def load_transfer_final(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if message.text == 'Разместить перевозку':
            from_place_country = data["from_place_country"]
            from_place_city = data["from_place_city"]
            to_place_country = data["to_place_country"]
            to_place_city = data["to_place_city"]
            comment = data["comment"]
            date_transfer = data["date_transfer"]
            user_id = message.from_user.id
            date = datetime.now()
            await sqllite_db.sql_add_transfer([from_place_country, from_place_city,
                                            to_place_country, to_place_city, comment, date_transfer, 1, user_id, date])
            await message.answer("Ура! Транзит размещен", reply_markup=kb_transfer)
            await state.finish()
        elif message.text == 'Внести изменения':
            await state.finish()
            await start_create_transit(message)
        elif message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_transfer)
            await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_create_transit, lambda message: 'Разместить перевозку' == message.text)
    dp.register_message_handler(load_transfer_from_place_country, state=FSMTransfer.from_place_country)
    dp.register_message_handler(load_transfer_from_place_city, state=FSMTransfer.from_place_city)
    dp.register_message_handler(load_transfer_to_place_country, state=FSMTransfer.to_place_country)
    dp.register_message_handler(load_transfer_to_place_city, state=FSMTransfer.to_place_city)
    dp.register_message_handler(load_transfer_date_transfer, state=FSMTransfer.date_transfer)
    dp.register_message_handler(load_transfer_comment, state=FSMTransfer.comment)
    dp.register_message_handler(load_transfer_final, state=FSMTransfer.final)
