from flask import Flask
from utils.extensions import db, DB_URL
from apps.routes import routers
from telebot import TeleBot
from decouple import config
import threading
import time
from apps.parsing.gsheet import links_models, update_google_sheets


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


# Функция для вызова в фоновом потоке
def run_continuously():
    while True:
        update_google_sheets(links_models=links_models)
        time.sleep(1800)  # Задержка между вызовами функции


if __name__ == '__main__':
    # Запуск фонового потока
    background_thread = threading.Thread(target=run_continuously)
    background_thread.daemon = True  # Поток завершится при завершении главной программы
    background_thread.start()

    app.run(debug=True)
