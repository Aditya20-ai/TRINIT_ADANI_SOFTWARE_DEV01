from dotenv import load_dotenv, find_dotenv
from os import environ

from src import app


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    app.run(
        debug=(environ.get("PRODUCTION") != "TRUE"), 
        host=environ.get("HOST"), 
        port=environ.get("PORT")
    )
