import time

from db import db,sql
import requests
from bs4 import BeautifulSoup
import lxml

import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


# Авторизация в гугл и запрос данных из таблицы
def google_sheets() -> tuple:
    CREDENTIALS_FILE = 'creds.json'
    sheet_id = "1lOKNBD1sdYi53OrQBHY4jZSVRLtyRyRyhe8L3A6UOCU"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
                                                                   )
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets','v4', http=http_auth)
    range_ = 'A:D'
    values = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_)
    response = tuple(values.execute()['values']) # получение данных из таблицы и преобразование в кортеж
    return response


# Запрашиваем актуальный курс доллара от ЦБ
def dollar_exchange() -> float:
    req = requests.get('https://www.cbr.ru/scripts/XML_daily.asp?') # Запрос в ЦБ по всем валютам

    soup = BeautifulSoup(req.content, 'lxml') # Передача ответа в библиотеку для расшифровки

    tag = soup.find(
        "valute",
        {'id':'R01235'},
    ) # Поиск нужной валюты по ID

    price = float(
        tuple(tag.children)[4]
        .text
        .replace(',','.')
                ) # Поиск цены и преобразование в число с плавающей запятой

    return price


# Записываем в базу новые строки и обновления
def write_base(data_for_write:tuple):

    sql.execute(f'SELECT * FROM sheets WHERE num = {int(data_for_write[0])}')
    sql_select = sql.fetchone()

    if sql_select is None:
        sql.execute(f"""INSERT INTO sheets (num, order_num, cost_usd, delivery_date, cost_rub) 
                                VALUES ({int(data_for_write[0])},
                                        {int(data_for_write[1])},
                                        {float(data_for_write[2])},
                                        '{data_for_write[3]}',
                                        {float(data_for_write[4])}
                                        )""")
        db.commit()
    else:
        sql.execute(f"""UPDATE sheets SET num = {int(data_for_write[0])},
                                        order_num = {int(data_for_write[1])},
                                        cost_usd = {float(data_for_write[2])},
                                        delivery_date = '{data_for_write[3]}',
                                        cost_rub = {float(data_for_write[4])} 
                                        WHERE num = {int(data_for_write[0])}
                    """)
        db.commit()


# Функия для проверки расхождений с информацией в таблице и той, что была записана последняя
def difference(tuple_1: tuple, tuple_2: tuple) -> list:
    list_difference = []
    for x in tuple_1:
        if x in tuple_2:
            continue
        else:
            list_difference.append(x)
    return list_difference


# Основная функция работы
def processing():
    snap_last_update = ()
    while True:
        data_from_sheet = google_sheets()[1:] # Берем из таблицы все строки кроме первой

        if data_from_sheet != snap_last_update: # Сравниваем с последней записью

            # Проверка есть ли разница в значениях и в длине кортежей
            if len(snap_last_update) == 0 or len(snap_last_update) == len(data_from_sheet) :
                usd = dollar_exchange() # Актальный курс USD
                snap_last_update = data_from_sheet[:] # Сохраняем последние данные из таблицы в переменную
                for i in data_from_sheet:
                    list_i = i[:]
                    coast_rub = float(i[2]) * usd # Получаем стоимость в рублях
                    list_i.append(coast_rub)
                    tuple_base_rec = tuple(list_i)
                    write_base(tuple_base_rec) # Отправляем кортеж с готовой информацией на запись в таблицу

            # Условие, что разная длина кортежей и последняя сохраненная запись не равна 0
            else:
                # В зависимости от того какой из кортежей больше делаем вывод была удалена строчка или добавлена
                if len(data_from_sheet) < len(snap_last_update):
                    # Видим, что была удалена строчка и сравнением ищем какая именно, после чего удаляем строчку из базы
                    dif = tuple(difference(snap_last_update, data_from_sheet))
                    sql.execute(f'DELETE FROM sheets WHERE num = {int(dif[0][0])}')
                    db.commit()
                    snap_last_update = data_from_sheet[:] # Запоминаем последнее обновление
                elif len(snap_last_update) < len(data_from_sheet):
                    # Видим что была добавлена строка в таблицу, сравнением ищем какая именно и отправляем
                    # ее на запись в таблицу
                    dif = tuple(difference(data_from_sheet, snap_last_update))
                    print(dif)
                    usd = dollar_exchange()
                    snap_last_update = data_from_sheet[:]
                    for i in dif:
                        list_i = i[:]
                        coast_rub = float(i[2]) * usd
                        list_i.append(coast_rub)
                        tuple_base_rec = tuple(list_i)
                        write_base(tuple_base_rec)






        else:
            # Ожидание изменений в таблице
            time.sleep(5)


def main():
    processing()


if __name__ == '__main__':
    main()

