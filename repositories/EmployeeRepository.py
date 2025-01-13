import sqlite3

def get_employees():
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()
        cursor.execute("SELECT name, working_hours, working_hours as remaining_hours FROM employee")
        employees = {name: [working_hours, remaining_hours] for name, working_hours, remaining_hours in cursor.fetchall()}
        connection.close()
        return employees
    except sqlite3.Error as e:
        raise Exception("Errore durante il recupero dei dipendenti")
       
def insert_employee(name, hours):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO employee (name, working_hours) VALUES (?, ?)", (name, hours))
        connection.commit()
        connection.close()
    except sqlite3.IntegrityError as e:
        raise Exception(f"Il nome '{name}' è già stato inserito")

def delete_employee(name):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM employee WHERE name=?", (name,))
        employee_id = cursor.fetchone()[0]
        if not employee_id:
            raise Exception(f"Dipendente '{name}' non trovato nel database")

        cursor.execute("DELETE FROM employee WHERE id = ?", (employee_id,))
        cursor.execute("DELETE FROM employee_role WHERE employee_id = ?", (employee_id,))

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        raise Exception(f"Errore durante la rimozione del dipendente")
    
def assign_role(employee_name, role_name):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM employee WHERE name=?", (employee_name,))
        employee_id = cursor.fetchone()[0]
        if not employee_id:
            raise Exception(f"Dipendente '{employee_name}' non trovato nel database")

        cursor.execute("SELECT id, name FROM role WHERE name=?", (role_name,))
        role_id = cursor.fetchone()[0]
        if not role_id:
            raise Exception(f"Ruolo '{role_name}' non trovato nel database")

        cursor.execute("INSERT INTO employee_role (employee_id, role_id) VALUES (?, ?)", (employee_id, role_id))

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        raise Exception(f"Errore durante l'assegnazione del ruolo al dipendente")

def remove_assigned_role(employee_name, role_name):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM employee WHERE name=?", (employee_name,))
        employee_id = cursor.fetchone()[0]
        if not employee_id:
            raise Exception(f"Dipendente '{employee_name}' non trovato nel database")

        cursor.execute("SELECT id, name FROM role WHERE name=?", (role_name,))
        role_id = cursor.fetchone()[0]
        if not role_id:
            raise Exception(f"Ruolo '{role_name}' non trovato nel database")

        cursor.execute("DELETE FROM employee_role WHERE employee_id = ? AND role_id = ?", (employee_id, role_id))

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        raise Exception(f"Errore durante la rimozione del ruolo assegnato al dipendente")

def get_assigned_roles(employee_name):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("""
            SELECT r.name
            FROM employee e
            JOIN employee_role er ON e.id = er.employee_id
            JOIN role r ON er.role_id = r.id
            WHERE e.name = ?
        """, (employee_name,))
        roles = [role for role, in cursor.fetchall()]

        connection.close()
        return roles
    except sqlite3.Error as e:
        raise Exception(f"Errore durante il recupero dei ruoli del dipendente")
    
def get_employees_by_role(role_name):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("""
            SELECT e.name
            FROM employee e
            JOIN employee_role er ON e.id = er.employee_id
            JOIN role r ON er.role_id = r.id
            WHERE r.name = ?
        """, (role_name,))
        employees = [employee for employee, in cursor.fetchall()]

        connection.close()
        return employees
    except sqlite3.Error as e:
        raise Exception(f"Errore durante il recupero dei dipendenti per ruolo")
    
def get_roles_by_employee(employee_name):
    try:
        connection = sqlite3.connect('restaurant_management.db')
        cursor = connection.cursor()

        cursor.execute("""
            SELECT r.name
            FROM employee e
            JOIN employee_role er ON e.id = er.employee_id
            JOIN role r ON er.role_id = r.id
            WHERE e.name = ?
        """, (employee_name,))
        roles = [role for role, in cursor.fetchall()]

        connection.close()
        return roles
    except sqlite3.Error as e:
        raise Exception(f"Errore durante il recupero dei ruoli del dipendente")