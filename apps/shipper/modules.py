from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta, datetime
from typing import List
from decouple import config

from .models import Shipper
from utils.extensions import db
from utils.gb_models import Customer
from ..utils import encode_date, arriving_date, validate_track_number




class PackagesDB:
    """Класс для создания записей в БД для посылок из Shipper"""
    def __init__(self, data: dict, week: str) -> None:
        self.statuses = {1: 'Ожидаем', 2: 'На упаковке', 3: 'Отправили', 4: 'Готова к выдаче', 5: ''}
        self.week = week
        self.create_packages = self.create_update_shipper_objects(data)
        self.weekly_packages = self.get_weekly_packages()


    def create_update_shipper_objects(self, data: dict):
        """Функция создания и обновления данных в БД"""
        
        try:
            for email, packages in data.items():
                for package in packages:
                    customer = Customer.query.filter_by(email=email, company='shipper').first()
                    if customer:
                        shipper = Shipper.query.get(package.get('id'))
                        if not shipper and package.get('status') != 1:
                            # Создаем записи в БД если она ранее не была добавлена
                            obj = Shipper(
                                id=package.get('id'),
                                customer=customer.id,
                                title=package.get('description'),
                                weight=package.get('weight'),
                                status=self.statuses.get(package.get('status', 1)),  # Значение по умолчанию 'Ожидаем'
                                track_number=validate_track_number(package.get('tracking_number')),
                                created_date=encode_date(package.get('created_at')),
                                coming_date=arriving_date(package.get('created_at'))
                            )
                            db.session.add(obj)


                        elif package.get('status') != 1:
                            # Если добавлена обновляем данные
                            shipper.customer = customer.id
                            shipper.title = package.get('description')
                            shipper.weight = package.get('weight')
                            shipper.status = self.statuses.get(package.get('status', 1))  # Значение по умолчанию 'Ожидаем'
                            shipper.track_number = validate_track_number(package.get('tracking_number'))
                            shipper.created_date = encode_date(package.get('created_at'))
                            shipper.coming_date = arriving_date(package.get('created_at'))
                        
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            return f"ERROR: Ошибка базы данных\n{e}"
        except Exception as e:
            return f"ERROR: Произошла ошибка\n{e}"
        return "SUCCESS"
    

    def get_weekly_packages(self):
        
        if "ERROR" not in self.create_packages:
            """Получение объектов Shipper для текущей или следующей недели"""
            try:
                today = datetime.now().date()
                start_of_week = today - timedelta(days=today.weekday())
                if self.week == "next":
                    start_of_week += timedelta(days=7)
                end_of_week = start_of_week + timedelta(days=6)
                return Shipper.query.filter(
                    Shipper.coming_date >= start_of_week,
                    Shipper.coming_date <= end_of_week
                ).all()
            except Exception as e:
                return []  
        else:
            return self.create_packages
        


def telegram_message_info(packages: List[Shipper], week: str):
    """Функция для формирования ответа в тг чат"""

    message = f"Товары на {'текущей' if "next" not in week else 'следующей'} неделе *Shipper*\n```\n"
    sum_price = 0
    for package in packages:
        price = round(package.weight * package.customer.tarif, 2)
        sum_price+=price
        message+=f"{package.name} – {package.customer.name} – {price}"
    
    sum_price_in_soms = sum_price * config('KGS')
    message+=f"```\nИтого на следующей неделе: *${sum_price}*\nВ сомах: *{sum_price_in_soms}*"

    return 