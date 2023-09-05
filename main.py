from flask import Flask, Response

import os
from dotenv import load_dotenv

import threading
import time

from parsing import *

load_dotenv()

app = Flask(__name__)


available_url = {
    "illkirch": "/illkirch",
    "cronenbourg": "/cronenbourg",
    "paul-appell": "/paul-appell"
}


@app.get("/")
def get_root():
    return available_url


@app.get("/illkirch")
def get_illkirch():
    return str(parserIllkirch(get_html(os.getenv('ILLKIRCH')))).replace("'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.get("/cronenbourg")
def get_cronenbourg():
    return str(parserCronenbourg(get_html(os.getenv('CRONENBOURG')))).replace("'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.get("/paul-appell")
def get_paulappell():
    return str(parserPaulAppell(get_html(os.getenv('PAUL_APPELL')))).replace("'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == "__main__":
    # Run the app in a separate thread
    threading.Thread(target=app.run, kwargs={
        'host': os.getenv('HOST'),
        'port': 5000,
        'debug': False
    }).start()

    # Run an another thread which parse the menu every 10 minutes into global variable
