from datetime import datetime, timedelta

def encode_date(timestamp):
    dt_object = datetime.utcfromtimestamp(timestamp)
    return dt_object


def arriving_date(timestamp):
    """ Функция определяет день когда можно забрать товар,
        без учета других ситуаций """

    # >>> Eсли товар приедет после среды, товар будет отправлен на след неделе в пятницу
    dt_object = datetime.utcfromtimestamp(timestamp)
    day_of_week = dt_object.weekday()

    # Определение, до или после среды
    if day_of_week <= 2:  # Если до среды
        friday_of_current_week = dt_object + timedelta(days=(4 - day_of_week + 7))
        return friday_of_current_week
    else:                 # Если после среды
        days_until_next_friday = (4 - day_of_week + 7) % 7
        next_week_friday = dt_object + timedelta(days=days_until_next_friday + 14)
        return next_week_friday
    #TODO Проверка по времени