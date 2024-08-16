import gspread
import time
from flask import Blueprint

from .models_articles import *
from .get_data_ai import get_data

gsheetRouter = Blueprint('gsheet', __name__, url_prefix='/gsheet')

@gsheetRouter.route('/', methods=['GET'])
def update_google_sheets():

    """Авторизация"""
    sa = gspread.service_account()

    """Подключаемся к документу"""
    sh = sa.open("MacPython")

    """Подключаемся к странице"""
    wks = sh.worksheet('Apple Edu (копия)')

    links_models = {
    #Air 13" M2
    url_air_13_m2: air_13_m2,

    #Air 13" M3
    url_air_13_m3: air_13_m3,

    #Air 15" M3
    url_air_15_m3: air_15_m3,

    #Pro 14" M3
    url_pro_14_m3: pro_14_m3,

    #Pro 14" M3 Pro & Max
    url_pro_14_m3_pro_max: pro_14_m3_pro_max,

    #Pro 16" M3 Pro & Max
    url_pro_16_m3_pro_max: pro_16_m3_pro_max,

    #Mac Studio Max & Ultra
    url_mac_studio_m2_max_ultra: mac_studio_m2_max_ultra,

    #Mac Mini M2 & M2 Pro
    url_macmini_m2_pro: macmini_m2_pro
    }

    "Проходимся по каждой ссылке и запускаем для каждой модели функцию для сбора цен"
    for url, models in links_models.items():
        time.sleep(70)
        "Получаем список моделей"
        for models in get_data(url=url, headers=headers, model=models):

            "Проходимся по каждой модели и звписывем в ее в таблицу"
            try:
                article = list(models.keys())[0]

                finded_row = wks.find(article)

                edu_price = wks.get(f"D{finded_row.row}")[0][0].replace('$','').replace('\xa0','')

                insider_price = models[article][0]

                wks.update(f'E{finded_row.row}', insider_price)
                time.sleep(10)

            except Exception as ex:
                with open("errors.txt", "a+") as file:
                    file.write(str(ex))
                if 'quota' in str(ex).lower():
                    print("Превышен лимит запросов. Ожидание перед повторной попыткой...")
                    time.sleep(63)  # Подождите минуту перед повторной попыткой
                else:
                    print(ex)
                time.sleep(10)

    return {"status":"success", "message": "Обновлено"}


    # # cell = wks.find("MLY03")

    # # print((cell.row, cell.col))

    # # wks.update(f"E{cell.row}", "Hello")