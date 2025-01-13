import tkinter as tk
import repositories.EmployeeRepository as EMPREPO
from tkinter import messagebox

employees = {} # {name: (total_hours, remaining_hours)}
assigned_roles = []

def get_employees():
    return EMPREPO.get_employees()

def insert_employee(entry_name, entry_hours, callback):
    name = entry_name.get()
    hours = entry_hours.get()
    if name and hours:
        try:
            hours = int(hours)  # Validate that hours is a number
            EMPREPO.insert_employee(name, hours)
            employees[name] = (hours, hours) # Add the employee to the list, the remaining hours are equal to the total hours
            entry_name.delete(0, tk.END)
            entry_hours.delete(0, tk.END)
            callback() 
        except ValueError:
            messagebox.showerror("Errore", "Le ore settimanali devono essere un numero")
        except Exception as e:
            messagebox.showerror("Errore", str(e))
    else:
        messagebox.showerror("Errore", "Inserisci un nome e le ore settimanali per il dipendente")

def delete_employee(listbox_employees, callback):
    selected_employee = listbox_employees.curselection()
    if selected_employee:
        employee_name = listbox_employees.get(selected_employee[0]).split(" (")[0]
        EMPREPO.delete_employee(employee_name)
        employees.pop(employee_name)
        callback()
    else:
        messagebox.showerror("Errore", "Nessun dipendente selezionato")

def assign_role(cb_emp_name, cb_role_name, callback):
    employee_name = cb_emp_name.get()
    role_name = cb_role_name.get()
    if employee_name and role_name:
        if(role_name in assigned_roles):
            messagebox.showerror("Errore", "Ruolo già assegnato a questo dipendente")
        else:
            assigned_roles.append(role_name)
            EMPREPO.assign_role(employee_name, role_name)
            callback()
    else:
        messagebox.showerror("Errore", "Seleziona un dipendente e un ruolo")

def remove_assigned_role(cb_emp_name, listbox_assigned_roles, callback):
    employee_name = cb_emp_name.get()
    if employee_name and listbox_assigned_roles.curselection():
        role_name = assigned_roles[listbox_assigned_roles.curselection()[0]]
        assigned_roles.remove(role_name)
        EMPREPO.remove_assigned_role(employee_name, role_name)
        callback()
    else:
        messagebox.showerror("Errore", "Seleziona un ruolo assegnato al dipendente")

def set_selected_employee(employee_name):
    global assigned_roles
    assigned_roles = EMPREPO.get_assigned_roles(employee_name)
    
def get_employees_by_role(role_name):
    return EMPREPO.get_employees_by_role(role_name)

def get_roles_by_employee(employee_name):
    return EMPREPO.get_roles_by_employee(employee_name)