from flask import Flask
from flaskwebgui import FlaskUI

app = Flask(__name__)
ui = FlaskUI(app=app, server="flask", width=1200, height=600)

from app import routes

ui.run()