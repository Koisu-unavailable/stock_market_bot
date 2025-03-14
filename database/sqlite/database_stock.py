import sqlite3

import logging

from database.stock_obj import Stock
logger = logging.getLogger("Sqlite Database")





def _create_session():
    conn = sqlite3.connect("stock_prices.db")
    session = conn.cursor()
    return conn, session

def get_all_stocks():
    conn, cursor = _create_session()
    stocks = cursor.execute(f"SELECT * FROM {Stock.__tablename__}").fetchall()
    conn.close()
    return stocks

def add_stock_or_edit(stock: Stock) -> None:
    conn, cursor = _create_session()
    with conn:
        query = f"INSERT OR REPLACE INTO {Stock.__tablename__} (symbol, price, market) VALUES ('{stock.symbol}', {stock.price}, '{stock.exchange}')" # TODO: ADD DISPLAY NAME
        logging.debug(query)
        cursor.execute(query)
    return

def is_duplicate_stock(target_stock: any): # TODO: ADD STOCK TYPE!!!!!
    conn, cursor = _create_session()
    with conn:
        all_stocks = cursor.execute(f"SELECT * FROM {Stock.__tablename__}").fetchall()
    for stock in all_stocks:
        if stock[0] == target_stock[0]:
            return True
    return False
