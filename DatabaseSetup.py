import sqlite3

def create_test_tables():
    connection = sqlite3.connect('restaurant_management.db')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS employee")
    cursor.execute("DROP TABLE IF EXISTS role")
    cursor.execute("DROP TABLE IF EXISTS employee_role")
    cursor.execute("DROP TABLE IF EXISTS room")
    cursor.execute("DROP TABLE IF EXISTS room_role")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            working_hours INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS role (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_role (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employee(id),
            FOREIGN KEY (role_id) REFERENCES role(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS room (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS room_role (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            employee_number INTEGER NOT NULL,
            FOREIGN KEY (room_id) REFERENCES room(id),
            FOREIGN KEY (role_id) REFERENCES role(id)
        )
    """)

    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Mario', 40)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Luigi', 36)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Paolo', 36)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Giovanni', 36)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Carlo', 40)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Andrea', 20)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Giuseppe', 36)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Antonio', 16)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Francesco', 36)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Roberto', 36)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Alberto', 36)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Alessandro', 36)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Davide', 20)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Fabio', 40)")
    cursor.execute("INSERT INTO employee (name, working_hours) VALUES ('Federico', 40)")

    cursor.execute("INSERT INTO role (name) VALUES ('Cuoco')")
    cursor.execute("INSERT INTO role (name) VALUES ('Aiuto cuoco')")
    cursor.execute("INSERT INTO role (name) VALUES ('Lavapiatti')")
    cursor.execute("INSERT INTO role (name) VALUES ('Cameriere')")
    cursor.execute("INSERT INTO role (name) VALUES ('Barista')")

    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (1, 1)") # Mario cuoco
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (2, 1)") # Luigi cuoco
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (3, 1)") # Paolo cuoco
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (4, 2)") # Giovanni aiuto cuoco
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (5, 2)") # Carlo aiuto cuoco
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (5, 3)") # Carlo lavapiatti
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (6, 4)") # Andrea cameriere
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (7, 4)") # Giuseppe cameriere
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (7, 3)") # Giuseppe lavapiatti
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (8, 4)") # Antonio cameriere
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (8, 5)") # Antonio barista
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (9, 5)") # Francesco barista
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (10, 1)") # Roberto cuoco
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (10, 2)") # Roberto aiuto cuoco
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (11, 4)") # Alberto cameriere
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (12, 4)") # Alessandro cameriere
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (13, 4)") # Davide cameriere
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (14, 4)") # Fabio cameriere
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (15, 4)") # Federico cameriere
    cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (15, 5)") # Federico barista



    cursor.execute("INSERT INTO room (name) VALUES ('Cucina')")
    cursor.execute("INSERT INTO room (name) VALUES ('Sala 1')")
    cursor.execute("INSERT INTO room (name) VALUES ('Sala 2')")
    cursor.execute("INSERT INTO room (name) VALUES ('Bar')")

    cursor.execute("INSERT INTO room_role (room_id, role_id, employee_number) VALUES (1, 1, 2)") # 2 cuochi in cucina
    cursor.execute("INSERT INTO room_role (room_id, role_id, employee_number) VALUES (1, 2, 1)") # 1 aiuto cuoco in cucina
    cursor.execute("INSERT INTO room_role (room_id, role_id, employee_number) VALUES (1, 3, 1)") # 1 lavapiatti in cucina
    cursor.execute("INSERT INTO room_role (room_id, role_id, employee_number) VALUES (2, 4, 2)") # 2 camerieri in sala 1
    cursor.execute("INSERT INTO room_role (room_id, role_id, employee_number) VALUES (3, 4, 1)") # 1 cameriere in sala 2
    cursor.execute("INSERT INTO room_role (room_id, role_id, employee_number) VALUES (4, 5, 1)") # 1 barista al bar
    cursor.execute("INSERT INTO room_role (room_id, role_id, employee_number) VALUES (4, 4, 1)") # 1 cameriere al bar
    
    connection.commit()
