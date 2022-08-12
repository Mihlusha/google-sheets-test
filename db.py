import psycopg2
from psycopg2 import Error


def auth() -> list:
    with open("data_auth.txt", "r", encoding="utf-8") as f:
        i = f.readline().split()
    return i


host = auth()[0]
user = auth()[1]
password = auth()[2]
db_name = auth()[3]
port = auth()[4]

db = psycopg2.connect(
    user=user,
    # пароль, который указали при установке PostgreSQL
    password=password,
    host=host,
    port=port,
    database=db_name
)
sql = db.cursor()

create_sheets = """
CREATE TABLE IF NOT EXISTS sheets (
    num INT PRIMARY KEY,
    order_num INT,
    cost_usd DECEMICAL,
    delivery_date DATE,
    cost_rub DECEMICAL
    

);
"""



def creat_conection():
    try:
        sql.execute(create_sheets)
        db.commit()
    except Error as e:
        print(f'Родилась ошибка {e}')
        raise e


creat_conection()
