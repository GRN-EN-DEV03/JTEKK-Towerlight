import pyodbc
from pyodbc import Error
from datetime import datetime

class ms_db_connect():

    def __init__(self):
        self.server = r'DEV-03\SQLEXPRESS'  # Replace with your server name
        self.database = 'netcube'  # Replace with your database name
        self.username = 'grn-en'  # Replace with your username
        self.password = 'Banana-Pi00'  # Replace with your password
        self.driver = '{ODBC Driver 17 for SQL Server}'  # Or your appropriate driver
        self.conn_db = None # change here

        self.query_result = None
        self.result = None

    def _connect(self):
        conn = None
        try:
            conn_str = (
                f'DRIVER={self.driver};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password};'
            )
            conn = pyodbc.connect(conn_str)
            print("Database connected")
        except Error as e:
            print(f"Error while connecting to SQL Server: {e}")
        return conn

    def aslist(self):
        return self.query_result

    def __iter__(self):
        return iter(self.aslist())

    def __str__(self):
        return str(self.result)

    def connect_select(self, table=None, condition=None, field='*'):
        try:
            self.conn_db = self._connect() # add connect here
            cursor = self.conn_db.cursor()
            if condition is not None:
                sql_select = f"SELECT {field} FROM {table} WHERE {condition}"
                # print("IF CONDITION")
            else:
                sql_select = f"SELECT {field} FROM {table}"
                # print("ELSE CONDITION")

            cursor.execute(sql_select)
            self.query_result = cursor.fetchall()
            self.result = cursor.rowcount
            self.conn_db.commit()

        except Error as error:
            print(f"Error while selecting from SQL Server: {error}")
            self.result = f"error select message: {error}"

        finally:
            if self.conn_db:
                self.conn_db.close()
                self.conn_db = None # set it to None

    def connect_update(self, table=None, values=None, condition=None):
        row_count = 0
        try:
            self.conn_db = self._connect() # add connect here
            cursor = self.conn_db.cursor()
            sql_update = f"UPDATE {table} SET {values} WHERE {condition}"
            cursor.execute(sql_update)
            self.conn_db.commit()
            row_count = cursor.rowcount
            self.result = f"update successfully in {table}"

        except Error as error:
            print(f"Error while updating in SQL Server: {error}")
            # self.result = f"error update message: {error}"

        finally:
            if self.conn_db:
                self.conn_db.close()
                self.conn_db = None # set it to None
        return row_count

    def connect_delete(self, table=None, condition=None):
        row_count = 0
        try:
            self.conn_db = self._connect() # add connect here
            cursor = self.conn_db.cursor()
            sql_delete = f"DELETE FROM {table} WHERE {condition}"
            cursor.execute(sql_delete)
            self.conn_db.commit()
            row_count = cursor.rowcount
            self.result = f"delete successfully from {table}"

        except Error as error:
            print(f"Error while deleting from SQL Server: {error}")
            self.result = f"error delete message: {error}"

        finally:
            if self.conn_db:
                self.conn_db.close()
                self.conn_db = None # set it to None
        return row_count

    def connect_sql_insert(self, table, values, use_db=None):
        row_count = 0
        try:
            self.conn_db = self._connect() # add connect here
            cursor = self.conn_db.cursor()
            if use_db:
                cursor.execute(f"USE [{use_db}]")
            sql_insert_query = f"INSERT INTO {table} VALUES ({values})"  # Note the parenthesis around values
            cursor.execute(sql_insert_query)
            self.conn_db.commit()
            row_count = cursor.rowcount
            print(f"Record(s) inserted successfully into {table}: {cursor.rowcount}")
            cursor.close()

        except Error as error:
            print(f"Error while inserting into SQL Server: {error}")
            self.result = f"error insert message: {error}"
            if self.conn_db:
                self.conn_db.rollback()  # Rollback on error

        finally:
            if self.conn_db:
                self.conn_db.close()
                self.conn_db = None # set it to None
                print("The SQL Server connection is closed")
        return row_count
    
    def connect_select_join(self, command):
        try:
            self.conn_db = self._connect()
            cursor = self.conn_db.cursor()
            sql_select = command
            cursor.execute(sql_select)
            self.query_result = cursor.fetchall()
            self.result = cursor.rowcount
            self.conn_db.commit()

        except Error as error:
            print(f"Error while executing join query: {error}")
            self.result = f"error select message: {error}"
        finally:
            if cursor:
                cursor.close()
                print("The SQL Server connection is closed")
        return self.query_result
