from os.path import abspath, dirname
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

BASE_DIR = dirname(dirname(abspath(__file__)))

DB_URL = "sqlite:///" + BASE_DIR + "/db.sqlite3"