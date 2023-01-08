import sqlite3 as sql

database = "restaurant.db"
connection = sql.connect(database)
connection.execute("PRAGMA foreign_keys = 1")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS RESTAURANT_ORDER(
    order_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    state TEXT DEFAULT "open" NOT NULL,
    payment_method TEXT NOT NULL,
    cost REAL NOT NULL,
    date TEXT DEFAULT (date('now','localtime')) NOT NULL,
    time TEXT DEFAULT (time('now','localtime')) NOT NULL,
    comment TEXT
    )
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS OUTSIDE_ORDER(
    order_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    street TEXT,
    floor INTEGER,
    number INTEGER,
    area TEXT,
    customer_id,
    FOREIGN KEY (order_number) REFERENCES RESTAURANT_ORDER(order_number) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS RESTAURANT_TABLE(
    table_number INTEGER NOT NULL,
    capacity INTEGER NOT NULL,
    state TEXT DEFAULT "free" NOT NULL,
    PRIMARY KEY (table_number) 
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS INSIDE_ORDER(
    order_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    table_number INTEGER NOT NULL,
    FOREIGN KEY (table_number) REFERENCES RESTAURANT_TABLE(table_number) ON DELETE CASCADE
    FOREIGN KEY (order_number) REFERENCES RESTAURANT_ORDER(order_number) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS CUSTOMER(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    phone_number INTEGER NOT NULL,
    email TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS RESERVATION(
    reservation_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date TEXT NOT NULL,
    phone_number INTEGER NOT NULL,
    people INTEGER NOT NULL,
    time TEXT NOT NULL,
    name TEXT NOT NULL,
    state TEXT DEFAULT "reserved" NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS RESERVE(
    table_number INTEGER NOT NULL,
    reservation_number INTEGER NOT NULL,
    PRIMARY KEY (table_number,reservation_number),
    FOREIGN KEY (table_number) REFERENCES RESTAURANT_TABLE(table_number),
    FOREIGN KEY (reservation_number) REFERENCES RESERVATION(reservation_number)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS EMPLOYEE(
    tin INTEGER NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    sex TEXT,
    birthday TEXT NOT NULL,
    email TEXT,
    address TEXT NOT NULL,
    phone_number INTEGER NOT NULL,
    salary REAL NOT NULL,
    PRIMARY KEY (tin)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS HANDLES(
    start_time TEXT,
    end_time TEXT,
    date TEXT NOT NULL,
    table_number INTEGER NOT NULL,
    employee_tin INTEGER NOT NULL,
    FOREIGN KEY (table_number) REFERENCES RESTAURANT_TABLE(table_number),
    FOREIGN KEY (employee_tin) REFERENCES EMPLOYEE(tin)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS DELIVER(
    order_number INTEGER NOT NULL,
    employee_tin INTEGER NOT NULL,
    time TEXT DEFAULT (time('now','localtime')) NOT NULL,
    PRIMARY KEY (order_number),
    FOREIGN KEY (order_number) REFERENCES OUTSIDE_ORDER(order_number),
    FOREIGN KEY (employee_tin) REFERENCES EMPLOYEE(tin)
    ) 
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS CONSISTS(
    order_number INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_number,dish_id),
    FOREIGN KEY (order_number) REFERENCES RESTAURANT_ORDER(order_number) ON DELETE CASCADE,
    FOREIGN KEY (dish_id) REFERENCES DISH(id)
    ) 
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS DISH(
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    cost REAL NOT NULL,
    PRIMARY KEY (id)
    ) 
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS MADE_OF(
    dish_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    PRIMARY KEY (dish_id,ingredient_id),
    FOREIGN KEY (dish_id) REFERENCES DISH(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES INGREDIENT(id)
    ) 
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS INGREDIENT(
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    state TEXT NOT NULL,
    expiration_date TEXT NOT NULL,
    PRIMARY KEY (id)
    ) 
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS INGREDIENT_INCLUDED_IN_ORDER(
    ingredient_id INTEGER NOT NULL,
    ingredient_order_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    cost_per_unit REAL NOT NULL,
    expiration_date TEXT NOT NULL,
    PRIMARY KEY (ingredient_id,ingredient_order_id),
    FOREIGN KEY (ingredient_order_id) REFERENCES INGREDIENT_ORDER(id)
    ) 
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS INGREDIENT_ORDER(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    supplier_tin INTEGER NOT NULL,
    state TEXT NOT NULL DEFAULT "processing",
    cost REAL NOT NULL,
    date TEXT DEFAULT (date('now','localtime')) NOT NULL,
    arrival_date TEXT,
    arrival_time TEXT,
    FOREIGN KEY (supplier_tin) REFERENCES SUPPLIER(tin)
    ) 
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS SUPPLIER(
    tin INTEGER NOT NULL,
    name TEXT NOT NULL,
    phone_number INTEGER NOT NULL,
    address TEXT NOT NULL,
    email TEXT,
    PRIMARY KEY (tin) 
    ) 
""")

connection.commit()
