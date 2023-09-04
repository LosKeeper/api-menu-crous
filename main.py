from flask import Flask

import os
from dotenv import load_dotenv

from parsing import *

load_dotenv()

app = Flask(__name__)


available_url = {
    "illkirch": "/illkirch",
}


@app.get("/")
def get_root():
    return available_url


@app.get("/illkirch")
def get_illkirch():
    return parser(get_html('https://www.crous-strasbourg.fr/restaurant/resto-u-illkirch/'))


Flask.run(app, host=os.getenv('HOST'), port=5000)
