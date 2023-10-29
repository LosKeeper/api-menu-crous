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
    return illkirch


@app.get("/cronenbourg")
def get_cronenbourg():
    return cronenbourg


@app.get("/paul-appell")
def get_paulappell():
    return paulappell


def fill_menu():
    global illkirch
    global cronenbourg
    global paulappell

    while True:
        illkirch = str(parserIllkirch(get_html(os.getenv('ILLKIRCH')))).replace(
            "'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}
        cronenbourg = str(parserCronenbourg(get_html(os.getenv('CRONENBOURG')))).replace(
            "'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}
        paulappell = str(parserPaulAppell(get_html(os.getenv('PAUL_APPELL')))).replace(
            "'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}

        print("Menu updated")

        # Wait 10 minutes
        time.sleep(600)
        illkirch = ""
        cronenbourg = ""
        paulappell = ""


if __name__ == "__main__":
    # Global variable to store the menu
    illkirch = ""
    cronenbourg = ""
    paulappell = ""

    # Run the app in a separate thread
    threading.Thread(target=app.run, kwargs={
        'host': os.getenv('HOST'),
        'port': 5000,
        'debug': False
    }).start()

    # Run an another thread which parse the menu every 10 minutes into global variable
    threading.Thread(target=fill_menu).start()
