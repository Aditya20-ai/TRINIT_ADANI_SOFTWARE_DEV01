import mysql.connector
from dotenv import load_dotenv, find_dotenv
from os import environ
load_dotenv(find_dotenv())   
class MysqlConnection():
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=environ.get('DB_HOST'),
                user=environ.get('DB_USER'),
                passwd = environ.get('DB_PASS'),
                database=environ.get('DB_NAME'),
                connect_timeout=5
            )
        except mysql.connector.Error as e:
            # TODO: Replace print statement with loggers
            print(f"Error: {e}")
            self.connection = None

        if self.connection:
            self.cursor = self.connection.cursor()
    
    
    def insert_records(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            self.connection.rollback()

    def select_records(self, query, return_list=False):
        try:
            self.cursor.execute(query)
            return list(self.cursor.fetchall()[0]) if return_list else self.cursor.fetchall()[0]
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None
            
    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close() 

def list_parser(string):
    return [item.strip("'") for item in eval(string)[0].split(', ')]
