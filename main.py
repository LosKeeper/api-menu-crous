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
    "paul-appell": "/paul-appell",
    "esplanade": "/esplanade",
    "gallia": "/gallia",
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


@app.get("/esplanade")
def get_esplanade():
    return esplanade


@app.get("/gallia")
def get_gallia():
    return gallia


def fill_menu():
    global illkirch
    global cronenbourg
    global paulappell
    global esplanade
    global gallia

    while True:
        illkirch = str(parse_menu(get_html(os.getenv('ILLKIRCH')), "Illkirch")).replace(
            "'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}
        cronenbourg = str(parse_menu(get_html(os.getenv('CRONENBOURG')), "Cronenbourg")).replace(
            "'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}
        paulappell = str(parse_menu(get_html(os.getenv('PAUL_APPELL')), "Paul-Appell")).replace(
            "'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}
        esplanade = str(parse_menu(get_html(os.getenv('ESPLANADE')), "Esplanade")).replace(
            "'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}
        gallia = str(parse_menu(get_html(os.getenv('GALLIA')), "Gallia")).replace(
            "'", "\""), 200, {'Content-Type': 'application/json; charset=utf-8'}

        # Wait 10 minutes
        time.sleep(600)
        illkirch = ""
        cronenbourg = ""
        paulappell = ""
        esplanade = ""
        gallia = ""


if __name__ == "__main__":
    # Global variable to store the menu
    illkirch = ""
    cronenbourg = ""
    paulappell = ""
    esplanade = ""
    gallia = ""

    # Run the app in a separate thread
    threading.Thread(target=app.run, kwargs={
        'host': os.getenv('HOST'),
        'port': 5000,
        'debug': False
    }).start()

    # Run an another thread which parse the menu every 10 minutes into global variable
    threading.Thread(target=fill_menu).start()
