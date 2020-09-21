from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app.view import api
app.register_blueprint(api)


# Build the database if db does not exist
if not os.path.exists('app.db'):
    db.create_all()