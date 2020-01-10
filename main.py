from old import database_operations
import json

from flask import Flask, request, Response
from routes import api_routes


app = Flask(__name__)
app.register_blueprint(api_routes)
