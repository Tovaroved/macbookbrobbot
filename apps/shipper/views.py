from flask import Blueprint, request
from utils.extensions import db
from .service import get_list
from .models import Shipper
from .modules import PackagesDB
import json

shipperRouter = Blueprint('shipper', __name__, url_prefix='/shipper')


@shipperRouter.route('/packages', methods=['GET','POST'])
def get_data():
    # Получаем chat_id чтобы транслировать ошибки если они есть
    chat_id = request.data.get('chat_id')
    week = request.data.get('week')

    # Отправляем запрос на получени данных из API Shipper
    data: dict = get_list(chat_id)

    # При успешном запросе создаем новые и обновляем старые данные в БД
    if "ERROR" not in data:
        packages: list[Shipper] = PackagesDB(data)
    else:
        return packages
    
    if isinstance(packages, list):
        ...
    

    return {"status":"success", "data": data}