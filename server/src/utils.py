import datetime

import mysql.connector
from dotenv import load_dotenv, find_dotenv
from os import environ
from imgurpython import ImgurClient, imgur

import jwt
import requests
import json
import time

load_dotenv(find_dotenv())


class MysqlConnection():
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=environ.get('DB_HOST'),
                user=environ.get('DB_USER'),
                passwd=environ.get('DB_PASS'),
                database=environ.get('DB_NAME'),
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


class UploadHandler:

    def __init__(self):
        self.client_id = environ.get('IMGUR_CLIENT_ID')
        self.client_secret = environ.get('IMGUR_CLIENT_SECRET')
        self.client = ImgurClient(self.client_id, self.client_secret)

    def upload_image(self, image_path) -> str:
        config = {'album': None}
        image = self.client.upload_from_path(image_path, config=config, anon=True)
        return image['link']


def list_parser(string):
    return [item.strip("'") for item in eval(string)[0].split(', ')]


class ZoomMeeting:
    def __init__(self):
        self.API_KEY = 'Your API key'
        self.API_SEC = 'Your API secret'
        self.token = ""

    def get_token(self):
        token = jwt.encode(
            # Create a payload of the token containing
            # API Key & expiration time
            {'iss': self.API_KEY, 'exp': time.time() + 5000},
            # Secret used to generate token signature
            self.API_SEC,
            # Specify the hashing alg
            algorithm='HS256'
        )
        print(token)
        print(type(token))
        self.token = token
        return token

    def create_meeting(self, topic: str, duration: int, time: datetime.datetime):
        meetingdetails = {"topic": topic,
                          "type": 2,
                          "start_time": str(time),
                          "duration": str(duration),
                          "timezone": "Asia/Kolkata",
                          "agenda": "test",

                          "recurrence": {"type": 1,
                                         "repeat_interval": 1
                                         },
                          "settings": {"host_video": "true",
                                       "participant_video": "true",
                                       "join_before_host": "False",
                                       "mute_upon_entry": "False",
                                       "watermark": "true",
                                       "audio": "voip",
                                       "auto_recording": "cloud"
                                       }
                          }
        headers = {'authorization': 'Bearer ' + self.get_token(),
                   'content-type': 'application/json'}
        # todo: fix token
        r = requests.post(
            f'https://api.zoom.us/v2/users/me/meetings',
            headers=headers, data=json.dumps(meetingdetails))
        y = json.loads(r.text)
        print(json.dumps(y, indent=4, sort_keys=True))
        join_URL = y["join_url"]
        meetingPassword = y["password"]
        return {"url": join_URL, "password": meetingPassword}