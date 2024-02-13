import sqlite3 as sql


with sql.connect('Warehouses_db.db') as db:
    cursor = db.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        login TEXT,
        password TEXT
    );

    CREATE TABLE IF NOT EXISTS Companies(
        id INTEGER PRIMARY KEY,
        company_name TEXT,
        company_address TEXT
    );

    CREATE TABLE IF NOT EXISTS Orders(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        company_id INTEGER,
        delivery_address TEXT,
        date_of_completion TEXT,
        file_word TEXT,
        file_excel TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (company_id) REFERENCES Companies(id)
    );

    CREATE TABLE IF NOT EXISTS Categories(
        id INTEGER PRIMARY KEY,
        category_name TEXT
    );
    
    CREATE TABLE IF NOT EXISTS Goods_in_order(
        order_id INTEGER,
        good_id INTEGER,
        amount  INTEGER,
        FOREIGN KEY (good_id) REFERENCES Goods(article_number),
        FOREIGN KEY (order_id) REFERENCES Orders(id)
    );

    CREATE TABLE IF NOT EXISTS Goods(
        warehouse_id INTEGER,
        category_id INTEGER,
        good_name TEXT,
        amount INTEGER,
        measure_unit TEXT,
        price INTEGER,
        time_start TEXT,
        time_to_end TEXT,
        description TEXT,
        article_number INTEGER PRIMARY KEY UNIQUE,
        image TEXT,
        FOREIGN KEY (warehouse_id) REFERENCES Warehouses(id),
        FOREIGN KEY (category_id) REFERENCES Categories(id)
    );

    CREATE TABLE IF NOT EXISTS Warehouses(
        id INTEGER PRIMARY KEY,
        category_id INTEGER,
        warehouse_name TEXT,
        warehouse_address TEXT,
        address_coordinates TEXT,
        FOREIGN KEY (category_id) REFERENCES Categories(id)
    );

    """)

print('ready')