'''
Please note:

The first file that you should run in this level is tests.py for database creation, with all tests passing.
Remember that running the hack.py will change the state of the database, causing some tests inside tests.py
to fail.

If you like to return to the initial state of the database, please delete the database (level-4.db) and run 
the tests.py again to recreate it.
'''

import sqlite3
import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    DB_CRUD_ops().get_stock_info(request.args["input"])
    DB_CRUD_ops().get_stock_price(request.args["input"])
    DB_CRUD_ops().update_stock_price(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

# Characters that should not exist in user-supplied input
RESTRICTED_CHARS = ";%&^!#-"
BAD_QUERY_MESSAGE = "Error, your query was not run because your input parameters seem badly formatted"

class Connect(object):

    # helper function creating database with the connection
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        return connection

class Create(object):

    def __init__(self):
        con = Connect()
        try:
            # creates a dummy database inside the folder of this challenge
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            # checks if tables already exist, which will happen when re-running code
            table_fetch = cur.execute(
                '''
                SELECT name 
                FROM sqlite_master 
                WHERE type='table'AND name='stocks';
                ''').fetchall()

            # if tables do not exist, create them and insert dummy data
            if table_fetch == []:
                cur.execute(
                    '''
                    CREATE TABLE stocks
                    (date text, symbol text, price real)
                    ''')

                # inserts dummy data to the 'stocks' table, representing average price on date
                cur.execute(
                    "INSERT INTO stocks VALUES ('2022-01-06', 'MSFT', 300.00)")
                db_con.commit()

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

class DB_CRUD_ops(object):

    @staticmethod
    def _user_input_okay(user_input: str) -> bool:
        """
        Two simple checks of user input to see if input is 
        potentially malicous. 

        Boolean returned, with True meaning user input **seems** okay.
        """
        if any([char in user_input for char in RESTRICTED_CHARS]):
            return False
        
        # checks if input contains extra quotes to fight against SQL injection
        if (user_input.count("'") != 0) or (user_input.count('"') != 0):
            return False
        
        return True


    def get_stock_info(self, stock_symbol:str) -> str:
        """
        retrieves all info about a stock symbol from the stocks table
        Example: get_stock_info('MSFT') will result into executing
        SELECT * FROM stocks WHERE symbol = 'MSFT'
        """
        # building database from scratch as it is more suitable for the purpose of the lab
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()


            if not self._user_input_okay(stock_symbol):
                return BAD_QUERY_MESSAGE
            
            # if looks okay, run the query, but use a parameterized statement
            res = "[METHOD EXECUTED] get_stock_info\n"
            cur.execute("SELECT * FROM stocks WHERE symbol = ?", (stock_symbol,))
            query = "SELECT * FROM stocks WHERE symbol = '" + stock_symbol + "'"
            res += "[QUERY] " + query + "\n"

            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + str(result)

            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()


    def get_stock_price(self, stock_symbol:str) -> str:
        """
        retrieves the price of a stock symbol from the stocks table
        Example: get_stock_price('MSFT') will result into executing
        SELECT price FROM stocks WHERE symbol = 'MSFT'
        """
        # building database from scratch as it is more suitable for the purpose of the lab
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            if not self._user_input_okay(stock_symbol):
                return BAD_QUERY_MESSAGE

            # if looks okay, run the query, but use a parameterized statement
            res = "[METHOD EXECUTED] get_stock_price\n"
            cur.execute("SELECT price FROM stocks WHERE symbol = ?", (stock_symbol,))
            query = "SELECT price FROM stocks WHERE symbol = '" + stock_symbol + "'"
            res += "[QUERY] " + query + "\n"

            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + str(result) + "\n"

            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    
    def update_stock_price(self, stock_symbol:str, price:float) -> str:
        """
        Updates a given stocks price
        """
        # building database from scratch as it is more suitable for the purpose of the lab
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            if not isinstance(price, float):
                raise Exception("ERROR: stock price provided is not a float")
            
            if not self._user_input_okay(stock_symbol):
                return BAD_QUERY_MESSAGE

            # if looks okay, run the query, but use a parameterized statement
            res = "[METHOD EXECUTED] update_stock_price\n"
             # UPDATE stocks SET price = 310.0 WHERE symbol = 'MSFT'
            cur.execute("UPDATE stocks SET price = ? WHERE symbol = ?", (price, stock_symbol,))
            query = f"UPDATE stocks SET price = '{price}' WHERE symbol = '{stock_symbol}'"
            res += "[QUERY] " + query + "\n"

            cur.execute(query)
            db_con.commit()
            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + result
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()
