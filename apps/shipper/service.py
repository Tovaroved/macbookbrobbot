import requests
from datetime import datetime, timedelta
from .models import Shipper


# headers= {'Authorization':'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozOTg2NH0.7NBFKQH1zLk6BdkQh6ZDBBGYl-uM5npAXkGv_lBGvHY'} # Антон
headers= {'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0MzE4OX0.URp-X1LowI5_FbxXdv0LtMciRFYrLSXyMHH07BQPSjM'} # Уран

def get_list():
    url = 'https://api.shipper.space/v1/orders/in_progress'
    response = requests.get(url=url,
                            headers=headers)
    return response.json()


###########################
def get_by_id(obj_id):
    url = 'https://api.shipper.space/v1/orders/{obj_id}'
    response = requests.get(url=url,
                            headers=headers)
    return response.json()
    

def edit_product(obj_id, title: str, price: float):
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