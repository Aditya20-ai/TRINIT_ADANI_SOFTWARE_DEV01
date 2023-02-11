import mysql.connector
from dotenv import load_dotenv, find_dotenv
from os import environ
from imgurpython import ImgurClient, imgur

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

    def update_records(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            self.connection.rollback()

    def select_records(self, query, values):
        try:
            self.cursor.execute(query, values)
            output = self.cursor.fetchall()
            return output[0] if output else None
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None
            
    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close() 
    def raw_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None

class UploadHandler():

    def __init__(self):
        self.client_id = environ.get('IMGUR_CLIENT_ID')
        self.client_secret = environ.get('IMGUR_CLIENT_SECRET')
        self.client = ImgurClient(self.client_id, self.client_secret)
    
    def upload_image(self, image_path)->str:
        config = {'album': None}
        image = self.client.upload_from_path(image_path, config=config, anon=True)
        return image['link']

def list_parser(string):
    return [item.strip("'") for item in eval(string)[0].split(', ')]
