import sqlite3

def get_rooms():
    connection = sqlite3.connect('restaurant_management.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM room")
    rooms = [room[0] for room in cursor.fetchall()]
    connection.close()
    return rooms

def insert_room(name):
    connection = sqlite3.connect('restaurant_management.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO room (name) VALUES (?)", (name,))
    connection.commit()
    connection.close()

def delete_room(name):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM room WHERE name=?", (name,))
        room_id = cursor.fetchone()[0]
        if not room_id:
            print(f"Stanza '{name}' non trovata nel database")
            return False

        cursor.execute("DELETE FROM room WHERE id = ?", (room_id,))
        cursor.execute("DELETE FROM room_role WHERE room_id = ?", (room_id,))

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print("Errore durante la rimozione della stanza")
        connection.rollback()

def add_role(room_name, role_name, employee_number):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM room WHERE name=?", (room_name,))
        room_id = cursor.fetchone()[0]
        if not room_id:
            print(f"Stanza '{room_name}' non trovata nel database")
            return False

        cursor.execute("SELECT id FROM role WHERE name=?", (role_name,))
        role_id = cursor.fetchone()[0]
        if not role_id:
            print(f"Ruolo '{role_name}' non trovato nel database")
            return False
        cursor.execute("DELETE FROM room_role WHERE room_id = ? AND role_id = ?", (room_id, role_id))
        cursor.execute("INSERT INTO room_role (room_id, role_id, employee_number) VALUES (?, ?, ?)", (room_id, role_id, employee_number))

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print("Errore durante l'aggiunta del ruolo alla stanza")
        connection.rollback()

def remove_role(room_name, role_name, employee_number):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM room WHERE name=?", (room_name,))
        room_id = cursor.fetchone()[0]
        if not room_id:
            print(f"Stanza '{room_name}' non trovata nel database")
            return False

        cursor.execute("SELECT id FROM role WHERE name=?", (role_name,))
        role_id = cursor.fetchone()[0]
        if not role_id:
            print(f"Ruolo '{role_name}' non trovato nel database")
            return False
        if employee_number == 0:
            cursor.execute("DELETE FROM room_role WHERE room_id = ? AND role_id = ?", (room_id, role_id))
        else:    
            cursor.execute("UPDATE room_role SET employee_number = ? WHERE room_id = ? AND role_id = ?", (employee_number, room_id, role_id))
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print("Errore durante la rimozione del ruolo dalla stanza")
        connection.rollback()

def get_room_roles(room_name):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM room WHERE name=?", (room_name,))
        room_id = cursor.fetchone()[0]
        if not room_id:
            print(f"Stanza '{room_name}' non trovata nel database")
            return False

        cursor.execute("SELECT role_id, employee_number FROM room_role WHERE room_id=?", (room_id,))
        room_roles = {}
        for role_id, employee_number in cursor.fetchall():            
            cursor.execute("SELECT name FROM role WHERE id=?", (role_id,))
            role_name = cursor.fetchone()[0]
            room_roles[role_name] = employee_number                
        connection.close()
        return room_roles
    except sqlite3.Error as e:
        print("Errore durante il recupero dei ruoli della stanza")
        connection.rollback()
        return False