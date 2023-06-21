from flask import Flask

app = Flask(__name__)


from application import database
from application import controllers