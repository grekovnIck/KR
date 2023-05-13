import datetime

from aiogram import types, Dispatcher
from create_bot import dp, bot
import messages_text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqllite_db
#from telegram import ParseMode
from keyboards.client_get_phone_kb import kb_get_phone_number
from keyboards.client_select_type_kb import kb_client_select
from keyboards.transfer_kb import kb_transfer
from keyboards.order_kb import kb_order
from keyboards.choose_orders_liked_kb import kb_choose_orders_liked
from keyboards.choose_transfer_liked_kb import kb_choose_transfer_liked
from handlers.liked_orders import switch_to_liked_orders
from handlers.liked_transfers import switch_to_liked_transfers


@dp.message_handler(lambda message: 'Заказы' == message.text)
async def switch_chosen_order_menu(message: types.Message):
    print(message.from_user.id)
    chosen_orders = await sqllite_db.sql_get_chosen_orders(message.from_user.id)
    print(chosen_orders)


def register_handlers_client(dp: Dispatcher):
    dp.message_handler(switch_chosen_order_menu, lambda message: 'Заказы' == message.text)
