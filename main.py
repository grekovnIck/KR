import os

from aiogram.utils import executor

import config
from data_base import sqllite_db
from handlers import client, order_state, transfer_state, orders, transfers, liked_transfers, \
    liked_orders, contract_states, client_chosen_orders, client_chosen_transfers
from create_bot import dp, bot


async def on_startup(dp):
    print('Бот вышел в сеть')
    sqllite_db.sql_start()
    #await bot.set_webhook(config.URL)


# async def on_shutdown():
#     await sqllite_db.sql_close()
#     await bot.delete_webhook()


client.register_handlers_client(dp)
order_state.register_handlers_client(dp)
transfer_state.register_handlers_client(dp)
orders.register_handlers_client(dp)
transfers.register_handlers_client(dp)
liked_orders.register_handlers_client(dp)
liked_transfers.register_handlers_client(dp)
contract_states.register_handlers_client(dp)
client_chosen_orders.register_handlers_client(dp)
#client_chosen_transfers.

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# executor.start_webhook(dispatcher=dp,
#                        webhook_path='',
#                        on_startup=on_startup,
#                        on_shutdown=on_shutdown,
#                        skip_updates=True,
#                        host='0.0.0.0',
#                        port=int(os.environ.get('PORT', 5000)))


