import sqlite3 as sq
from aiogram import types


def sql_start():
    global base, cur
    base = sq.connect('bfd_db.db')
    cur = base.cursor()
    if base:
        print('data connected OK')
    else:
        print('data connected ERROR')
    base.execute('CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, name TEXT, phone TEXT, registrate TIMESTAMP WITH TIME ZONE, '
                 'is_ban INT)')

    base.execute('CREATE TABLE IF NOT EXISTS orders(id SERIAL PRIMARY KEY, name TEXT, link TEXT,'
                 'price TEXT, remuneration TEXT,  from_place_country TEXT, from_place_city TEXT, to_place_country TEXT, '
                 'to_place_city TEXT, comment TEXT, is_active INT, client_id TEXT, client_transfer_id TEXT, '
                 'date_placed TIMESTAMP WITH TIME ZONE, date_confirm TIMESTAMP WITH TIME ZONE, date_paid TIMESTAMP WITH TIME ZONE, delivired TIMESTAMP WITHOUT TIME ZONE)')

    base.execute('CREATE TABLE IF NOT EXISTS transfers(id SERIAL PRIMARY KEY, from_place_country TEXT, '
                 'from_place_city TEXT, to_place_country TEXT, to_place_city TEXT, date_transfer TIMESTAMP WITH TIME ZONE, comment TEXT, '
                 'is_active INT, client_id TEXT,  date_placed TIMESTAMP WITH TIME ZONE)')

    base.execute('CREATE TABLE IF NOT EXISTS contract(id SERIAL PRIMARY KEY, order_client_id TEXT, '
                 'order_id INTEGER, transfer_id INTEGER, transfer_client_id TEXT, status_id INT, confirm_date TIMESTAMP WITH TIME ZONE,'
                 'is_paid INT, paid_date TIMESTAMP WITH TIME ZONE, delivered_date TIMESTAMP WITH TIME ZONE)')

    base.execute('CREATE TABLE IF NOT EXISTS liked_order(client_order_id TEXT, client_transfer_id TEXT,'
                 'order_id INTEGER, date_time TIMESTAMP WITH TIME ZONE)')

    base.execute('CREATE TABLE IF NOT EXISTS liked_transfer(client_order_id TEXT, client_transfer_id TEXT,'
                 'transfer_id INTEGER, date_time TIMESTAMP WITH TIME ZONE)')

    base.execute('CREATE TABLE IF NOT EXISTS report(from_client_id TEXT, to_client_id TEXT,'
                 'description TEXT, date_time TIMESTAMP WITH TIME ZONE)')

    base.execute('CREATE TABLE IF NOT EXISTS comment(from_client_id TEXT, to_client_id TEXT,'
                 'description TEXT, stars INT, deliverd_on_time INT, date_time TIMESTAMP WITHOUT TIME ZONE)')

    base.commit()


async def sql_close():
    cur.close()
    base.close()

async def sql_create_user(data):
    print(data)
    cur.execute('INSERT INTO users (id , name, phone, registrate) VALUES (?, ?, ?, ?)', data)
    base.commit()


async def sql_add_order(data):
    cur.execute('INSERT INTO orders(name, link, price, remuneration,  from_place_country, from_place_city, '
                'to_place_country, to_place_city, comment, is_active, client_id,  date_placed) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    base.commit()


async def sql_add_transfer(data):
    cur.execute('INSERT INTO transfers(from_place_country, from_place_city,'
                'to_place_country, to_place_city, comment, date_transfer, is_active, client_id,  date_placed) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    base.commit()


async def sql_check_id_exists(user_id: str):
    try:
        if len(cur.execute(f'SELECT * FROM users WHERE id = {user_id}').fetchall()) == 0:
            return False
        else:
            return True
    except Exception:
        return False


async def sql_get_all_orders(message: types.Message):
    return cur.execute(f'SELECT * FROM orders WHERE client_id = {message.from_user.id} AND is_active = 1').fetchall()


async def sql_get_all_transfers(message: types.Message):
    return cur.execute(f'SELECT * FROM transfers WHERE client_id = {message.from_user.id} AND is_active = 1').fetchall()


async def sql_check_transfer_exists(user_id, order_id):
    transfer_id = cur.execute(f'SELECT contract.transfer_client_id FROM users '
                           f'INNER JOIN contract ON contract.order_client_id = users.id '
                           f'INNER JOIN transfers ON transfers.client_id = contract.transfer_client_id '
                           f'WHERE contract.order_client_id = {user_id} AND '
                           f'contract.order_id = {order_id}').fetchall()
    if len(transfer_id) == 0:
        return None
    contacts = cur.execute(f'SELECT name, phone FROM users '
                           f'WHERE id = {transfer_id[0][0]}')
    contacts = contacts.fetchall()
    if len(contacts) != 0:
        return contacts
    else:
        return None


async def sql_check_transfer_exists(user_id, order_id):
    transfer_id = cur.execute(f'SELECT contract.transfer_client_id FROM users '
                           f'INNER JOIN contract ON contract.order_client_id = users.id '
                           f'INNER JOIN orders ON orders.client_id = contract.order_client_id '
                           f'WHERE contract.transfer_client_id = {user_id} AND '
                           f'contract.order_id = {order_id}').fetchall()
    if len(transfer_id) == 0:
        return None
    contacts = cur.execute(f'SELECT name, phone FROM users '
                           f'WHERE id = {transfer_id[0][0]}')
    contacts = contacts.fetchall()
    if len(contacts) != 0:
        return contacts
    else:
        return None


async def sql_check_order_exists(user_id, order_id):
    transfer_id = cur.execute(f'SELECT contract.transfer_client_id FROM users '
                           f'INNER JOIN contract ON contract.order_client_id = users.id '
                           f'INNER JOIN transfers ON transfers.client_id = contract.transfer_client_id '
                           f'WHERE contract.order_client_id = {user_id} AND '
                           f'contract.order_id = {order_id}').fetchall()
    if len(transfer_id) == 0:
        return None
    contacts = cur.execute(f'SELECT name, phone FROM users '
                           f'WHERE id = {transfer_id[0][0]}')
    contacts = contacts.fetchall()
    if len(contacts) != 0:
        return contacts
    else:
        return None


async def sql_update_order(order_id, data):
    cur.execute(f'UPDATE orders SET name = "{data[0]}", link = "{data[1]}", price = "{data[2]}", remuneration = "{data[3]}",'
                f'from_place_country = "{data[4]}", from_place_city = "{data[5]}", to_place_country = "{data[6]}", '
                f'to_place_city = "{data[7]}", comment = "{data[8]}" '
                f'WHERE id = "{order_id}"')
    base.commit()


async def sql_update_transfer(order_id, data):
    cur.execute(f'UPDATE transfers SET from_place_country = "{data[0]}", from_place_city  = "{data[1]}", '
                f'to_place_country = "{data[2]}", to_place_city = "{data[3]}", comment = "{data[4]}", '
                f'date_transfer = "{data[5]}" '
                f'WHERE id = "{order_id}"')
    base.commit()


async def sql_delete_order(order_id):
    cur.execute(
        f'UPDATE orders SET is_active = 0 '
        f'WHERE id = "{order_id}"')
    base.commit()


async def sql_delete_transfer(transfer_id):
    cur.execute(
        f'UPDATE transfers SET is_active = 0 '
        f'WHERE id = "{transfer_id}"')
    base.commit()


async def sql_get_orders_by_country(user_id, from_country, to_country, to_city):
    return cur.execute('SELECT users.id, users.name, users.phone, orders.id, orders.name, orders.link, orders.price, '
                       'orders.remuneration, orders.from_place_city, orders.from_place_country, orders.to_place_country,'
                       ' orders.to_place_city, orders.comment, orders.client_id  FROM orders '
                       'INNER JOIN users ON orders.client_id = users.id '
                       f'WHERE from_place_country = "{from_country}" '
                       f'AND to_place_country = "{to_country}" '
                       f'AND to_place_city = "{to_city}"'
                       #f'AND users.id <> "{user_id}"'
                       f'AND is_active = 1').fetchall()


async def sql_get_orders_by_city(user_id, from_country, from_city, to_country, to_city):
    print(from_country)
    print(from_city)
    print(to_country)
    print(to_city)
    return cur.execute('SELECT users.id, users.name, users.phone, orders.id, orders.name, orders.link, orders.price, '
                       'orders.remuneration, orders.from_place_city, orders.from_place_country, orders.to_place_country,'
                       ' orders.to_place_city, orders.comment, orders.client_id  FROM orders '
                       'INNER JOIN users ON orders.client_id = users.id '
                       f'WHERE from_place_country = "{from_country}" '
                       f'AND from_place_city = "{from_city}" '
                       f'AND to_place_country = "{to_country}" '
                       f'AND to_place_city = "{to_city}"'
                       #f'AND users.id <> "{user_id}"'
                       f'AND is_active = 1').fetchall()


async def sql_get_transfers_by_city(user_id, from_country, from_city, to_country, to_city):

    return cur.execute('SELECT users.id, users.name, users.phone, transfers.id, transfers.from_place_city, '
                       'transfers.from_place_country, transfers.to_place_country, transfers.to_place_city, '
                       'transfers.date_transfer, transfers.comment, transfers.client_id  FROM transfers '
                       'INNER JOIN users ON transfers.client_id = users.id '
                       f'WHERE from_place_country = "{from_country}" '
                       f'AND from_place_city = "{from_city}" '
                       f'AND to_place_country = "{to_country}" '
                       f'AND to_place_city = "{to_city}"'
                       #f'AND users.id <> "{user_id}"'
                       f'AND is_active = 1').fetchall()


async def sql_get_transfers_by_country(user_id, from_country, to_country, to_city):
    return cur.execute('SELECT users.id, users.name, users.phone, transfers.id, transfers.from_place_city, '
                       'transfers.from_place_country, transfers.to_place_country, transfers.to_place_city, '
                       'transfers.date_transfer, transfers.comment, transfers.client_id  FROM transfers '
                       'INNER JOIN users ON transfers.client_id = users.id '
                       f'WHERE from_place_country = "{from_country}" '
                       f'AND to_place_country = "{to_country}" '
                       f'AND to_place_city = "{to_city}"'
                       #f'AND users.id <> "{user_id}"'
                       f'AND is_active = 1').fetchall()


async def sql_like_transfer(data):
    print(data[0])
    tmp = cur.execute('SELECT *  FROM liked_transfer '
                f'WHERE client_order_id = "{data[0]}" '
                f'AND client_transfer_id = "{data[1]}" '
                f'AND transfer_id = "{data[2]}"').fetchall()
    if len(tmp) != 0:
        return
    cur.execute('INSERT INTO liked_transfer(client_order_id, client_transfer_id, transfer_id, date_time) '
                'VALUES (?, ?, ?, ?)', data)
    base.commit()


async def sql_like_order(data):

    tmp = cur.execute('SELECT *  FROM liked_transfer '
                f'WHERE client_order_id = "{data[0]}" '
                f'AND client_transfer_id = "{data[1]}" '
                f'AND transfer_id = "{data[2]}"').fetchall()
    if len(tmp) != 0:
        return
    cur.execute('INSERT INTO liked_order(client_order_id, client_transfer_id, order_id, date_time) '
                'VALUES (?, ?, ?, ?)', data)
    base.commit()


async def sql_get_liked_orders(user_id):
    return cur.execute('SELECT users.id, users.name, users.phone, orders.id, orders.name, orders.link, orders.price, '
                       'orders.remuneration, orders.from_place_city, orders.from_place_country, orders.to_place_country,'
                       ' orders.to_place_city, orders.comment, orders.client_id FROM users '
                       'INNER JOIN liked_order ON liked_order.client_order_id = users.id '
                       'INNER JOIN orders ON liked_order.order_id = orders.id '
                       'AND orders.is_active = 1 '
                       f'AND liked_order.client_transfer_id = {user_id}').fetchall()


async def sql_get_liked_transfers(user_id):
    return cur.execute('SELECT users.id, users.name, users.phone, transfers.id, transfers.from_place_city, '
                       'transfers.from_place_country, transfers.to_place_country, transfers.to_place_city, '
                       'transfers.date_transfer, transfers.comment, transfers.client_id FROM users '
                       'INNER JOIN liked_transfer ON liked_transfer.client_transfer_id = users.id '
                       'INNER JOIN transfers ON liked_transfer.transfer_id = transfers.id '
                       'AND transfers.is_active = 1 '
                       f'AND liked_transfer.client_order_id = {user_id}').fetchall()


async def sql_delete_liked_order(client_order_id, client_transfer_id, order_id):
    cur.execute(f'DELETE FROM liked_order '
                f'WHERE client_order_id="{client_order_id}" '
                f'AND client_transfer_id="{client_transfer_id}" '
                f'AND order_id="{order_id}"')
    base.commit()


async def sql_delete_liked_transfer(client_order_id, client_transfer_id, transfer_id):
    cur.execute(f'DELETE FROM liked_transfer '
                f'WHERE client_order_id="{client_order_id}" '
                f'AND client_transfer_id="{client_transfer_id}" '
                f'AND transfer_id="{transfer_id}"')
    base.commit()


async def sql_update_contract(client_order_id, client_transfer_id, transfer_id, order_id):
    response = cur.execute(f'SELECT * FROM contract WHERE order_client_id = "{client_order_id}" '
                       f'AND transfer_client_id = "{client_transfer_id}" '
                       f'AND transfer_id = "{transfer_id}" '
                       f'AND order_id = "{order_id}" ').fetchall()
    print(len(response))
    if len(response) != 0:
        return

    cur.execute('INSERT INTO contract(order_client_id, transfer_client_id,'
                'transfer_id, order_id, status_id) '
                'VALUES (?, ?, ?, ?, ?)', [client_order_id, client_transfer_id, transfer_id, order_id, 0])
    base.commit()


async def sql_check_zero_status(client_order_id, client_transfer_id, transfer_id, order_id, status):
    response = cur.execute(f'SELECT * FROM contract WHERE order_client_id = "{client_order_id}" '
                       f'AND transfer_client_id = "{client_transfer_id}" '
                       f'AND transfer_id = "{transfer_id}" '
                       f'AND order_id = "{order_id}" '
                       f'AND status_id = {status} ').fetchall()
    print(len(response))
    if len(response) == 0:
        return True
    return False

async def sql_get_contract_id(client_order_id, client_transfer_id, transfer_id, order_id):
    return cur.execute(f'SELECT id FROM contract WHERE order_client_id = "{client_order_id}" '
                       f'AND transfer_client_id = "{client_transfer_id}" '
                       f'AND transfer_id = "{transfer_id}" '
                       f'AND order_id = "{order_id}" ').fetchall()[0]


async def sql_update_contract_status(contract_id, status):
    cur.execute(
        f'UPDATE contract SET status_id = "{status}" '
        f'WHERE id = "{contract_id}"')
    base.commit()


async def sql_get_contract(contract_id):
    return cur.execute(f'SELECT * FROM contract WHERE id = "{contract_id}" ').fetchall()


async def sql_get_contract_transfer_info(contract_id):
    return cur.execute(f'SELECT users.id, users.name, contract.transfer_id FROM contract '
                       f'INNER JOIN users ON contract.transfer_client_id = users.id '
                       f'WHERE contract.id = "{contract_id}" ').fetchall()[0]


async def sql_get_contract_order_info(contract_id):
    return cur.execute(f'SELECT users.id, users.name, contract.order_id FROM contract '
                       f'INNER JOIN users ON contract.order_client_id = users.id '
                       f'WHERE contract.id = "{contract_id}" ').fetchall()[0]


async def sql_get_chosen_orders(client_id):
    return cur.execute(f'SELECT * FROM  users '
                       f'INNER JOIN contract ON contract.transfer_client_id = users.id '
                       f'INNER JOIN orders ON orders.id = contract.order_id '
                       f'WHERE users.id = "{client_id}" '
                       f'AND contract.status_id = 1').fetchall()


async def sql_get_chosen_transfer(client_id):
    return cur.execute(f'SELECT * FROM  users '
                       f'INNER JOIN contract ON contract.order_client_id = users.id '
                       f'INNER JOIN transfers ON transfers.id = contract.transfers_id '
                       f'WHERE users.id = "{client_id}" '
                       f'AND contract.status_id = 1').fetchall()


async def sql_get_user_name(id):
    return cur.execute(f'SELECT name FROM  users '
                       f'WHERE id = "{id}" ').fetchall()


async def sql_create_report(from_user, to_user, description, date):
    cur.execute('INSERT INTO report(ofrom_client_id , to_client_id, description , date_time) '
                'VALUES (?, ?, ?, ?, ?)', [from_user, to_user, description, date])
    base.commit()
