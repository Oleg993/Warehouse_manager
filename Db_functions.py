import sqlite3 as sql
from datetime import date, datetime
from Documents.create_documents import description_good

class DataBase:
    def __init__(self):
        self.db_file = 'Warehouses_db.db'
        self.db_old_orders = "Orders_history.db"
        self.db = sql.connect(self.db_file)
        self.db1 = sql.connect(self.db_old_orders)

    '''log_in'''
    def log_in(self, login):
        """Вход в приложение базы пользователем
        :param login: логин
        :return: Возвращает пароль, если пароль не верный - None"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT password 
                                  FROM users 
                                  WHERE login=?''', [login])
                password = cursor.fetchone()
                return password
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''all files'''
    def get_all_goods_from_warehouses(self):
        """Получение информации о всех товарах на всех складах
        :return: возвращает все товары на всех складах (склад, категория, название, количество, ед. изм.,
                 цена, дата изготовления, годен до, описание, артикул, путь к фото)"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT warehouse_name, category_name, good_name, amount, measure_unit, price, 
                                         time_start, time_to_end, description, article_number, image 
                                  FROM Goods G JOIN Warehouses W ON G.warehouse_id = W.id 
                                               JOIN Categories C ON G.category_id = C.id''')
                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_warehouse_main'''
    def get_goods_from_warehouse(self, warehouse_name):
        """Получение информации о товарах на определенном складе
        :param warehouse_name: название склада
        :return: возвращает список с кортежами каждого товара (категория, название, количество, ед. изм.,
                 цена, дата изготовления, годен до, описание, артикул, путь к фото)"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT warehouse_name, category_name, good_name, amount, measure_unit, price, time_start, 
                                         time_to_end, description, article_number, image
                                  FROM Goods G JOIN Warehouses W ON G.warehouse_id = W.id 
                                               JOIN Categories C ON G.category_id = C.id
                                  WHERE warehouse_name = ?''', [warehouse_name])
                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def get_warehouses_names(self):
        """Получение всех названий складов
        :return: лист названий складов, пример: ['Запчасть плюс', 'Готовое и спелое']"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT warehouse_name
                                  FROM Warehouses''')
                names = cursor.fetchall()
                return [i[0] for i in names]
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_add_good'''
    def get_all_categories(self):
        """Получение всех доступных категорий товаров
        :return: Возвращает все категории товаров"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT category_name 
                                  FROM Categories''')
                categories = cursor.fetchone()
                return categories
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def add_new_good_into_db(self, good_info):
        """Добавление нового товара на склад
        :param good_info: [название склада (str), категория (str), название товара (str),
                           количество (int), ед. изм. (str), цена (int), дата изготовления (str),
                           годен до (str), описание (str), путь к фото (str)]
        :return: True - товар добавлен"""
        try:
            with self.db:
                '''Проверка на наличие категории/добавление и получение id категории'''
                cursor = self.db.cursor()
                cursor.execute('''SELECT id
                                  FROM Categories
                                  WHERE category_name = ?''', [good_info[1]])
                categ_id = cursor.fetchone()
                if categ_id is not None:
                    good_info[1] = categ_id
                else:
                    cursor.execute('''INSERT INTO Categories (category_name)
                                      VALUES (?)''', [good_info[1]])
                    cursor.execute('''SELECT MAX(id)
                                      FROM Categories''')
                    good_info[1] = cursor.fetchone()
                cursor.execute('''SELECT id
                                  FROM Warehouses
                                  WHERE warehouse_name = ?''', [good_info[0]])
                good_info[0] = cursor.fetchone()
                good_info[0], good_info[1] = good_info[1][0], good_info[0][0]  # из кортежа в число

                cursor.execute('''INSERT INTO Goods(warehouse_id, category_id, good_name, amount, measure_unit,
                                                    price, time_start, time_to_end, description, image)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', good_info)
                return cursor.rowcount > 0
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_edit_goods'''
    def delete_good(self, article_id):
        """Удаление товара со склада
        :param article_id - номер товара"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''DELETE FROM Goods 
                                  WHERE article_number = ?''', [article_id])
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_admin_panel'''
    def get_all_users(self):
        """Получение всей информации о пользователях
        :return Возвращает список [login, password]"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT * 
                                  FROM Users''')
                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def add_new_user(self, login, password):
        """Добавление пользователя
        :param login - логин нового пользователя, password - пароль нового пользователя"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''INSERT INTO Users(login, password) 
                                  VALUES(?, ?)''', [login, password])
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def update_user_info(self, login, password, user_id):
        """Обновление информации пользователя
        :param login - логин пользователя, password - пароль пользователя"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''UPDATE Users 
                                  SET login = ?, password = ? 
                                  WHERE id = ?''', [login, password, user_id])
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def delete_user(self, user_id):
        """Удаление пользователя
        :param user_id - номер пользователя"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''DELETE FROM Users 
                                  WHERE id = ?''', [user_id])
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_client_data'''
    def get_all_companies(self):
        """Получение информации о товарах заказа
        :return: Возвращает список информации о компаниях"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT * 
                                  FROM Companies''')
                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def add_new_order_into_bd_orders_and_good_in_orders(self, user_id, company_name, delivery_address, cart, paths=['-', '-']):
        """Формирование заказа в бд
        :param user_id - id логина пользователя, company_name - название компании,
               delivery_address - адрес компании/доставки,
               cart - список списков товаров [[article_id (int), amount (int)]...]
        :return: """
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT id
                                  FROM Companies
                                  WHERE company_name = ?''', [company_name])
                company_id = cursor.fetchone()
                if company_id is not None:
                    company_id = company_id[0]

                if company_id is None:
                    cursor.execute('''INSERT INTO Companies(company_name, company_address)
                                      VALUES (?, ?)''', [company_name, delivery_address])
                    cursor.execute('''SELECT MAX(id)
                                      FROM Companies''')
                    company_id = cursor.fetchone()[0]

                cursor.execute('''INSERT INTO Orders(user_id, company_id, delivery_address, date_of_completion, file_word, file_excel)
                                  VALUES (?, ?, ?, ?, ?, ?)''', [user_id, company_id, delivery_address, str(date.today()), paths[0], paths[1]])
                cursor.execute('''SELECT MAX(id)
                                  FROM Orders''')
                order_id = cursor.fetchone()[0]
                cart_with_index = [[order_id] + i for i in cart]

                cursor.executemany('''INSERT INTO Goods_in_order(order_id, good_id, amount)
                                      VALUES(?, ?, ?)''', cart_with_index)
                for good_id, amount in cart:
                    cursor.execute('''SELECT amount 
                                      FROM Goods 
                                      WHERE article_number = ?''', [good_id])
                    good_warehouse_amount = cursor.fetchone()[0]
                    cursor.execute('''UPDATE Goods 
                                      SET amount = ? 
                                      WHERE article_number = ?''', [good_warehouse_amount - amount, good_id])
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_orders_history'''
    def get_completed_orders(self, search_text=None):
        """Получение всех заказов
        :return: Возвращает список заказов"""
        try:
            with self.db:
                cursor = self.db.cursor()
                if search_text not in (None, ""):
                    cursor.execute('''SELECT O.id, login, company_name, delivery_address, date_of_completion, 
                                             file_word, file_excel
                                      FROM Users U JOIN Orders O ON U.id = O.user_id JOIN Companies C ON 
                                                        O.company_id = C.id
                                      WHERE LOWER(company_name) LIKE LOWER(?)''', [f"%{search_text}%"])
                else:
                    cursor.execute('''SELECT O.id, login, company_name, delivery_address, date_of_completion, 
                                             file_word, file_excel
                                      FROM Users U JOIN Orders O ON U.id = O.user_id JOIN Companies C ON 
                                                        O.company_id = C.id''')
                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def get_goods_info_from_order(self, id):
        """Получение информации о товарах заказа
        :param id - ид заказа
        :return: Возвращает список информации о товарах заказа"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT good_name, measure_unit, GO.amount
                                  FROM Goods_in_order GO JOIN Goods G ON GO.good_id = G.article_number
                                  WHERE order_id = ?''', [id])
                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def get_goods_info_from_old_orders(self, between, year, id):
        """Получение информации о товарах заказа
        :param id - ид заказа
        :return: Возвращает список информации о товарах заказа"""
        try:
            tables_order_goods_info = []
            table_name_goods = [f"Goods_in_order_{months[name]}_{year}" for name in between]
            print(table_name_goods)
            with self.db1:
                cursor = self.db1.cursor()
                for name in table_name_goods:
                    cursor.execute(f'''SELECT good_name, measure_unit, amount
                                       FROM {name}
                                       WHERE id = {id}''')
                    info = cursor.fetchall()
                    print(info)
                    tables_order_goods_info += info
                return tables_order_goods_info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def get_old_orders(self, between, year):
        """Получение информации о товарах заказа
        :param id - ид заказа
        :return: Возвращает список информации о товарах заказов"""
        try:
            global months
            months = {"Январь": "January", "Февраль": "February", "Март": "March", "Апрель": "April",
                      "Май": "May", "Июнь": "June", "Июль": "July", "Август": "August", "Сентябрь": "September",
                      "Октябрь": "October", "Ноябрь": "November", "Декабрь": "December"}
            tables_order_info = []
            tables_orders_names = [f"Orders_{months[name]}_{year}" for name in between]

            with self.db1:
                cursor = self.db1.cursor()
                cursor.execute("""SELECT name 
                                  FROM sqlite_master 
                                  WHERE type='table'""")
                all_exist_tables = cursor.fetchone()
                for table in tables_orders_names:
                    if table in all_exist_tables:
                        cursor.execute(f'''SELECT *
                                           FROM {table}''')
                        info = cursor.fetchall()
                        tables_order_info += info
                return tables_order_info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_authorization_form - schedule'''
    def create_db_for_old_orders(self):
        """Создание таблиц для архивации
        :return: True - таблицы созданы, False - таблицы не созданы"""
        try:
            with sql.connect('Orders_history.db') as db:
                cursor = db.cursor()
                current_date = datetime.now()
                table_name_orders = f"Orders_{current_date.strftime('%B')}_{current_date.year}"
                table_name_goods = f"Goods_in_order_{current_date.strftime('%B')}_{current_date.year}"
                print(table_name_orders, table_name_goods)

                '''Есть ли таблица в базе'''
                cursor.execute("""SELECT name 
                                  FROM sqlite_master 
                                  WHERE type='table' AND name= ?""", [table_name_orders])
                table_exists = cursor.fetchone()
                if table_exists:
                    print("Таблица существует, перенос не требуется")
                    is_table_real = [False]
                else:
                    print("Таблица не существует и будет создана")
                    is_table_real = [True, table_name_orders, table_name_goods]

                '''Создание таблиц'''
                cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name_orders}(
                    id INTEGER,
                    login TEXT,
                    company_name TEXT,
                    delivery_address TEXT,
                    date_of_completion TEXT,
                    file_word TEXT,
                    file_excel TEXT,
                    FOREIGN KEY (id) REFERENCES {table_name_goods} (id)
                )""")
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name_goods}(
                    id INTEGER,
                    good_name INTEGER,
                    measure_unit TEXT,
                    amount INTEGER
                )""")
            return is_table_real
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def tranfer_old_orders_into_archive_db_and_delete(self, table_names):
        """Создание таблиц для архивации"""
        try:
            with sql.connect('Warehouses_db.db') as db, sql.connect('Orders_history.db') as db1:
                cursor_warehouse = db.cursor()
                cursor_orders_history = db1.cursor()

                '''Перенос заказов и удаление из основной таблицы'''
                orders = DataBase().get_completed_orders()
                cursor_orders_history.executemany(f'''INSERT INTO {table_names[0]} (id, login, company_name, 
                                                            delivery_address, date_of_completion, file_word, file_excel)
                                                      VALUES (?, ?, ?, ?, ?, ?, ?)''', orders)
                cursor_warehouse.execute('''DELETE FROM Orders''')

                '''Перенос товаров заказа и удаление из основной таблицы'''
                cursor_warehouse.execute(f'''SELECT order_id, good_name, measure_unit, GO.amount
                                             FROM Goods_in_order GO JOIN Goods G ON GO.good_id = G.article_number''')
                goods = cursor_warehouse.fetchall()
                cursor_orders_history.executemany(f'''INSERT INTO {table_names[1]} (id, good_name, measure_unit, amount)
                                                      VALUES (?, ?, ?, ?)''', goods)
                cursor_warehouse.execute('''DELETE FROM Goods_in_order''')

        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def delete_after_time_good_ends(self):
        """Удаление товара со склада после окончания срока годности
        :return: Возвращает пароль, если пароль не верный"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT article_number, good_name, warehouse_address, time_to_end, 
                                         measure_unit, description, amount, price 
                                  FROM Goods G JOIN Warehouses W ON G.warehouse_id = W.id 
                                  WHERE time_to_end IS NOT NULL 
                                        AND Cast((JulianDay('now') - JulianDay(time_to_end)) as Integer) >= 0''')
                goods_for_deleting = cursor.fetchall()

                for id, name, address, time_to_end, measure_unit, description, amount, price in goods_for_deleting:
                    list_description = {'article_number': str(id), 'good_name': name, 'address_description': address,
                                        'date_description': time_to_end, 'measure_unit': measure_unit,
                                        'description': description, 'amount': str(amount), 'price': str(price)}
                    description_good(list_description)
                    cursor.execute('''DELETE FROM Goods
                                      WHERE article_number = ?''', [id])
                print(f"Delete done: {date.today()}")
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False
