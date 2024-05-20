from flask import Blueprint, request

from .service import get_list
from .models import Shipper
from .modules import PackagesDB, telegram_message_info


shipperRouter = Blueprint('shipper', __name__, url_prefix='/shipper')

@shipperRouter.route('/', methods=['GET'])
def hello():
    return {'message': 'Hello!!!'}


@shipperRouter.route('/packages', methods=['GET','POST'])
def get_data():

    if request.method == "POST":
        # try:
        # Получаем chat_id чтобы транслировать ошибки если они есть
        # chat_id = request.data.get('chat_id')
        print(request.data)
        week = request.get_json()['week']
    
        # Отправляем запрос на получени данных из API Shipper
        data: dict = get_list()

        # При успешном запросе создаем новые и обновляем старые данные в БД
        if "ERROR" not in data:
            packages: list[Shipper] = PackagesDB(data, week)
        else:
            return {"status": "error", "message": data}
        
        # Проверяем создан ли объект PackagesDB (создание и обновление данных о посылках в БД)
        if isinstance(packages, PackagesDB):

            # Проверяем что нет ошибок при получении данных для целевой недели
            if 'ERROR' not in packages.weekly_packages:
                message = telegram_message_info(packages.weekly_packages, week)

                return {"status":"success", "message": message}
            else:
                return {"status": "error", "message": packages.weekly_packages}
        # except Exception as ex:
        #     print(ex)
        #     return {"status": "error", "message": f"Ошибка:\n{ex}"}
            