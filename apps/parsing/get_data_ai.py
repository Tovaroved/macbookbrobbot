import requests
from bs4 import BeautifulSoup
import re

def get_data(url, headers, model) -> dict:

    models = []
    response = requests.get(
        url=url, headers=headers
    )

    if response.status_code == 200:

        """Создание дерева объектов"""
        soup = BeautifulSoup(response.text, 'html.parser')

        """Получение всех моделей"""
        all_rows_count = int(len(soup.find_all('tr', class_='item-row'))/2)
        all_rows = soup.find_all('tr', class_='item-row')[:all_rows_count]

        """Определение названий магазинов"""
        store_names = [store.get('title') for store in soup.find('table', class_='price-guide').find('tr').find_all('th')[0:-2]]

        for row in all_rows:
            """Определение цен для каждой строки, а также описание и ссылка на товар"""
            all_prices = row.find_all('td', class_=re.compile('item-price'))
            row_desc = row.find('td', class_='item-desc').text.replace('\n', ' ').replace('\t', '')

            substring = 'blue-bold'

            try:
                row_link = row.find('td', class_=lambda class_name: class_name and substring in class_name).find('a').get('href')
            except AttributeError:
                row_link = row.find('td', class_='item-desc').find('a').get('href')

            """Проходимся по ценам """

            try:
                best_price = row.find('td', class_=re.compile('bold')).text
                if 'place order' in best_price:
                    best_price = '$' + str(round(float(all_prices[0].text[1:].replace(',','')) - float(row.find('td', class_='item-discount').text[1:].replace(',','')), 2))

                else:
                    best_price = row.find('td', class_=re.compile('bold')).find('a').text

                best_price = int(float(best_price.split()[0].replace('$', '').replace(',', '')))

            except AttributeError:
                best_price = row.find('td', class_='item-price').text
            
            try:
                models.append({model[row_desc]: [best_price, row_link]})
            except KeyError:
                continue

        return models
    else:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")

