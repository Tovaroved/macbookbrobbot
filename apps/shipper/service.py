import requests
from datetime import datetime, timedelta
from .models import Shipper
from decouple import config

from app import macbrobot



def get_list(chat_id):
    url = 'https://api.shipper.space/v1/orders/in_progress'
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response_uran = requests.get(url=url, headers=config('uran'))
            response_altai = requests.get(url=url, headers=config('altai'))

            return {'sulaimanovuran@gmail.com': response_uran.json(), 'macbookbrogoods@gmail.com': response_altai.json()}
        
        except Exception as err:
            macbrobot.send_message(chat_id=chat_id, text=f"ERROR: Ошикбка при выполнении запроса\n{err}")
        
    return "ERROR: Не удалось выполнить запрос проверьте сайт"


###########################
def get_by_id(obj_id, headers=None):
    url = 'https://api.shipper.space/v1/orders/{obj_id}'
    response = requests.get(url=url,
                            headers=headers)
    return response.json()
    

def edit_product(obj_id, title: str, price: float, headers=None):
    """ Функция для изменения названия и цены, на товаре который едет в Бишкек!!! """

    url = 'https://api.shipper.space/v1/orders/{obj_id}'
    data = {'description':title, 'parcel_price':price}
    status = requests.get(url, headers=headers)
    if status.json().get('status')==3:
        response = requests.put(url, headers=headers,
                                json=data)
        if response:
            return {"status":"success"}
    else:   return {"status":"не подходит статус"}