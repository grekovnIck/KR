from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqllite_db
import telegram


@dp.callback_query_handler(lambda c: 'reject_contact_transfer' in c.data)
async def reject_contact_transfer_message(callback_query: types.CallbackQuery):
    print(callback_query.data)
    data = str(callback_query.data).split('_')
    contract_id = data[-1]
    await sqllite_db.sql_update_contract_status(contract_id, -1)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: 'give_contact_transfer' in c.data)
async def give_contact_transfer_message(callback_query: types.CallbackQuery):
    print(callback_query.data)
    data = str(callback_query.data).split('_')
    contract_id = data[-1]
    await sqllite_db.sql_update_contract_status(contract_id, 1)
    contract_data = await sqllite_db.sql_get_contract(contract_id)
    print(contract_data)
    await callback_query.message.answer(
        '<b>Отлично! Вы можете посмотреть контакт исполнителя в разделе <i>"Исполнители"</i> </b>',
        parse_mode=telegram.ParseMode.HTML)

    name = await sqllite_db.sql_get_user_name(contract_data[0][1])
    await bot.send_message(chat_id=contract_data[0][1],
                           text=f'<b>Ура! Пользователь </b> <a href="tg://user?id={contract_data[0][1]}" >{name[0][0]}</a> '
                                f'<b> откликнулся на вашу поездку № {contract_data[0][2]}</b>',
                           parse_mode=telegram.ParseMode.HTML)


@dp.callback_query_handler(lambda c: 'reject_contact_order' in c.data)
async def reject_contact_order_message(callback_query: types.CallbackQuery):
    print(callback_query.data)
    data = str(callback_query.data).split('_')
    contract_id = data[-1]
    await sqllite_db.sql_update_contract_status(contract_id, -1)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: 'give_contact_order' in c.data)
async def give_contact_order_message(callback_query: types.CallbackQuery):
    print(callback_query.data)
    data = str(callback_query.data).split('_')
    contract_id = data[-1]
    await sqllite_db.sql_update_contract_status(contract_id, 1)
    contract_data = await sqllite_db.sql_get_contract(contract_id)
    print(contract_data)
    await callback_query.message.answer('<b>Отлично! Вы можете посмотреть контакт исполнителя в разделе <i>"Исполнители"</i> </b>',
                                        parse_mode=telegram.ParseMode.HTML)
    name = await sqllite_db.sql_get_user_name(contract_data[0][1])
    await bot.send_message(chat_id=contract_data[0][4],
                           text=f'<b>Ура! Пользователь </b> <a href="tg://user?id={contract_data[0][1]}" >{name[0][0]}</a> '
                                f'<b>откликнулся на ваш заказ № {contract_data[0][2]}</b>',
                           parse_mode=telegram.ParseMode.HTML)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(reject_contact_transfer_message, lambda c: 'reject_contact_transfer' in c.data)
    dp.register_callback_query_handler(give_contact_transfer_message, lambda c: 'give_contact_transfer' in c.data)
    dp.register_callback_query_handler(reject_contact_order_message, lambda c: 'reject_contact_order' in c.data)
    dp.register_callback_query_handler(give_contact_order_message, lambda c: 'give_contact_order' in c.data)
