from flask import Flask
from utils.extensions import db, DB_URL
from apps.routes import routers
from telebot import TeleBot
from decouple import config


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    db.init_app(app)
    app.register_blueprint(routers)

    return app

# Создание БД и таблиц
def create_database_tables(app):
    with app.app_context():
        db.create_all()

# Создание приложения и инициализация бота
app = create_app()
create_database_tables(app)
macbrobot = TeleBot(config('BOT_TOKEN'))


if __name__ == '__main__':
    app.run(debug=True)
