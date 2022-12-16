import sqlite3
from datetime import datetime
import pandas as pd


connection = sqlite3.connect('finance.db')
sql = connection.cursor()

# Таблица доходов
sql.execute('CREATE TABLE IF NOT EXISTS income (user_id INTEGER, type_inc TEXT, sum REAL, reg_date DATETIME);')

# Таблица расходов
sql.execute('CREATE TABLE IF NOT EXISTS expenses ('
            'user_id INTEGER, category TEXT, item TEXT, number REAL, sum REAL, reg_date DATETIME);')




# Сохраняем
connection.commit()

########### Функции ###########


# Функция добавления дохода
def add_income(user_id, type_inc, sum):
    connection = sqlite3.connect('finance.db')
    sql = connection.cursor()

    # Регистрация клиента если нет в базе
    sql.execute('INSERT INTO income VALUES (?,?,?,?);', (user_id, type_inc, sum, datetime.now()))

    # Сохранение
    connection.commit()

# Проверяем всю базу
def check_user(user_id):
    connection = sqlite3.connect('finance.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT user_id FROM expenses WHERE user_id=?;', (user_id,)).fetchone()

    if checker is None:
        return False
    else:
        return True

#Получить все названия категорий из базы
def get_all_categories():
    connection = sqlite3.connect('finance.db')
    sql = connection.cursor()

    category = sql.execute('SELECT Category FROM Categories;').fetchall()

    # Отдаем список категорий
    return category

#Добавляет расходы (для добавления вручную)
def add_expenses(user_id, category, item, number, sum):
    connection = sqlite3.connect('finance.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO expenses VALUES (?,?,?,?,?,?);', (user_id, category, item, number, sum, datetime.now()))

    # Сохранение
    connection.commit()

#Добавляет расходы (для добавления через qr код)
def add_qr_expenses(user_id, category, item, number, sum, year, month, date):
    connection = sqlite3.connect('finance.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO expenses VALUES (?,?,?,?,?,?);', (user_id, category, item, number, sum, datetime(year, month, date)))

    # Сохранение
    connection.commit()

# Создание файла выгрузки доходов
def get_income_file(user_id):
    connection = sqlite3.connect('finance.db')

    inc = pd.read_sql(f'SELECT type_inc, sum, reg_date FROM income WHERE user_id={user_id};', connection)
    inc.to_excel('./Доходы.xlsx', sheet_name='Доходы', index=False)

# Создание файла выгрузки расходов
def get_expenses_file(user_id):
    connection = sqlite3.connect('finance.db')

    exp = pd.read_sql(f'SELECT category, item, number, sum, reg_date FROM expenses WHERE user_id={user_id};', connection)
    exp.to_excel('./Расходы.xlsx', sheet_name='Расходы', index=False)


