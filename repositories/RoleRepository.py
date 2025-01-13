import sqlite3

def get_roles():   
    connection = sqlite3.connect('restaurant_management.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM role")
    roles = [role[0] for role in cursor.fetchall()]
    connection.close()
    return roles

def insert_role(name):
    connection = sqlite3.connect('restaurant_management.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO role (name) VALUES (?)", (name,))
    connection.commit()
    connection.close()

def delete_role(name):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM role WHERE name=?", (name,))
        role_id = cursor.fetchone()[0]
        if not role_id:
            print(f"Ruolo '{name}' non trovato nel database")
            return False
        
        cursor.execute("SELECT id FROM employee_role WHERE role_id=?", (role_id,))
        found_employee_role = cursor.fetchone()
        if found_employee_role:
            raise Exception(f"Impossibile rimuovere un ruolo associato ad un dipendente")
        
        cursor.execute("SELECT id FROM room_role WHERE role_id=?", (role_id,))
        found_room_role = cursor.fetchone()
        if found_room_role:
            raise Exception(f"Impossibile rimuovere un ruolo associato ad una stanza")

        cursor.execute("DELETE FROM role WHERE id = ?", (role_id,))
        cursor.execute("DELETE FROM employee_role WHERE role_id = ?", (role_id,))
        cursor.execute("DELETE FROM employee_role WHERE role_id = ?", (role_id,))
        
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print("Errore durante la rimozione del ruolo")
        connection.rollback()
