import datetime

from aiogram import types, Dispatcher
from create_bot import dp, bot
import messages_text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqllite_db
from keyboards.client_get_phone_kb import kb_get_phone_number
from keyboards.client_select_type_kb import kb_client_select
from keyboards.transfer_kb import kb_transfer
from keyboards.order_kb import kb_order
from handlers.liked_orders import switch_to_liked_orders
from handlers.liked_transfers import switch_to_liked_transfers


class FSM_registrat_user(StatesGroup):
    name = State()
    phone = State()


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    if not await sqllite_db.sql_check_id_exists(message.from_user.id):
        await FSM_registrat_user.name.set()
        await message.answer(messages_text.GET_NAME)
    else:
        await bot.send_message(message.from_user.id, messages_text.HELLO, reply_markup=kb_client_select)


@dp.message_handler(state=FSM_registrat_user.name)
async def load_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        data['name'] = message.text # TODO: написать обработчик написания имени
    await message.answer(messages_text.GET_PHONE, reply_markup=kb_get_phone_number)
    await FSM_registrat_user.phone.set()


@dp.message_handler(state=FSM_registrat_user.phone)
async def load_phone(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.contact)
        data['phone'] = message.contact['phone_number'] # TODO: написать обработчик написания телефона
        data['id'] = message.contact['user_id']
        data['registrate'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    async with state.proxy() as data:
        s = f'Отлично! Ваши данные записаны:\n' \
            f'   <b>Имя:</b> <i>{data["name"]}</i>\n' \
            f'   <b>Номер телефона:</b> <i>{data["phone"]}</i>'
        await message.answer(s, parse_mode='HTML', reply_markup=kb_client_select)
    output = (str(data['id']), data['name'], data['phone'], data['registrate'])
    await sqllite_db.sql_create_user(output)
    await state.finish()


@dp.message_handler(lambda message: 'Заказать' == message.text)
async def select_role(message: types.Message):
    await message.answer('Меню клиента', reply_markup=kb_order)


@dp.message_handler(lambda message: 'Перевезти' == message.text)
async def select_role(message: types.Message):
    await message.answer('Меню перевозчика', reply_markup=kb_transfer)


@dp.message_handler(lambda message: 'Меню клиента' == message.text)
async def switch_order_menu(message: types.Message):
    await message.answer('Меню клиента', reply_markup=kb_order)


@dp.message_handler(lambda message: 'Меню перевозчика' == message.text)
async def switch_transfer_menu(message: types.Message):
    await message.answer('Меню перевозчика', reply_markup=kb_transfer)


@dp.message_handler(lambda message: '❤️' == message.text)
async def switch_transfer_liked_orders(message: types.Message):
    print(await sqllite_db.sql_get_liked_transfers(message.from_user.id))
    await message.answer('Понравившиеся исполнители', reply_markup=kb_order)
    await switch_to_liked_transfers(message, await sqllite_db.sql_get_liked_transfers(message.from_user.id))


@dp.message_handler(lambda message: '🧡' == message.text)
async def switch_order_liked_transfers(message : types.Message):
    #print(await sqllite_db.sql_get_liked_orders(message.from_user.id))
    await message.answer('Понравившиеся заказы', reply_markup=kb_transfer)
    #liked_orders = await sqllite_db.sql_get_liked_orders(message.from_user.id)
    await switch_to_liked_orders(message, await sqllite_db.sql_get_liked_orders(message.from_user.id))


@dp.message_handler(lambda message: 'Поддержка' == message.text)
async def switch_order_liked_transfers(message : types.Message):    #print(await sqllite_db.sql_get_liked_orders(message.from_user.id))
    await message.answer('По всем вопросам обращайтесь к владельцу группы <code>Grekov Nickolay</code>', parse_mode='HTML',
                         reply_markup=kb_order)


@dp.message_handler(lambda message: 'О проекте' == message.text)
async def switch_order_liked_transfers(message : types.Message):    #print(await sqllite_db.sql_get_liked_orders(message.from_user.id))
    await message.answer('Миссия этого бота помочь найти людям найти попутчиков, которые купили бы и привезли им товар'
                         'из любой точки мира. ', parse_mode='HTML',
                         reply_markup=kb_order)



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(load_phone, content_types=types.ContentTypes.CONTACT, state=FSM_registrat_user.phone)
    dp.register_message_handler(load_name, state=FSM_registrat_user.name)
    dp.register_message_handler(switch_order_menu, lambda message: 'Меню клиента' == message.text)
    dp.register_message_handler(switch_transfer_menu, lambda message: 'Меню перевозчика' == message.text)
    dp.register_message_handler(switch_transfer_liked_orders, lambda message: '🧡' == message.text)
    dp.register_message_handler(switch_order_liked_transfers, lambda message: '❤️' == message.text)






