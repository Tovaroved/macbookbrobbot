import gspread
from models_articles import *
from get_data_ai import get_data

links_models = {
    # Air 13" M2
    url_air_13_m2: air_13_m2, 

    #Air 13" M3
    url_air_13_m3: air_13_m3
    }


def update_google_sheets(links_models: dict):
    """Авторизация"""
    sa = gspread.service_account()

    """Подключаемся к документу"""
    sh = sa.open("MacPython")

    """Подключаемся к странице"""
    wks = sh.worksheet('Test Case')

    "Проходимся по каждой ссылке и запускаем для каждой модели функцию для сбора цен"
    for url, models in links_models.items():

        "Получаем список моделей"
        for models in get_data(url=url, headers=headers, model=models):

            "Проходимся по каждой модели и звписывем в ее в таблицу"

            article = list(models.keys())[0]

            finded_row = wks.find(article)

            edu_price = wks.get(f"D{finded_row.row}")[0][0].replace('$','').replace('\xa0','')

            insider_price = models[article][0]

            wks.update(f'E{finded_row.row}', )

    print('DONE')




update_google_sheets(links_models=links_models)

    # cell = wks.find("MLY03")

    # print((cell.row, cell.col))

    # wks.update(f"E{cell.row}", "Hello")