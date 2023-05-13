from aiogram import types, Dispatcher
from create_bot import dp, bot
import messages_text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqllite_db
from keyboards.order_kb import kb_order
from keyboards.back_kb import kb_back
from datetime import datetime

class FSMReport(StatesGroup):
    description = State()


@dp.message_handler(lambda message: 'report_' in message.text)
async def start_create_transit(message: types.Message):
    global user_id
    user_id = message.text.split('_')[1]
    if not await sqllite_db.sql_check_id_exists(user_id):
        return
    await FSMReport.description.set()
    await message.answer(messages_text.GET_REVIEW_OF_REPORT, reply_markup=kb_back)


@dp.message_handler(state=FSMReport.description)
async def load_transfer_from_place_country(message: types.Message, state=FSMContext):
    global user_id
    async with state.proxy() as data:
        print(message.text)
        if message.text == 'Вернуться в меню':
            await message.answer("Меню", reply_markup=kb_order)
            await state.finish()
            return
        data['description'] = message.text
    await message.answer(messages_text.GET_TRANSFER_FROM_CITY)  # , reply_markup=get_phone_number)
    await sqllite_db.sql_create_report(message.from_user.id, user_id, data['description'], datetime.now())
    await state.finish()

