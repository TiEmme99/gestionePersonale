import tkinter as tk
from tkinter import ttk
import services.EmployeeService as EMPSERV
import services.RoomService as ROOMSERV
import services.RoleService as ROLESERV
import services.ScheduleService as SCHEDSERV
from DatabaseSetup import create_test_tables
# from openpyxl import Workbook

class RestaurantManagementApp:
    def setup_role_gui(self):
        tk.Label(self.frame_roles, text="Gestione Ruoli", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)

        label_role_name = tk.Label(self.frame_roles, text="Nome Ruolo")
        entry_role_name = tk.Entry(self.frame_roles)
        btn_insert_role = tk.Button(self.frame_roles, text="Aggiungi Ruolo", command=lambda: ROLESERV.insert_role(entry_role_name, self.refresh_role_list))
        label_role_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_role_name.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        btn_insert_role.grid(row=2, column=1, padx=5, pady=(5, 20), sticky="e")
        
        label_existing_roles = tk.Label(self.frame_roles, text="Ruoli Inseriti")
        self.listbox_roles = tk.Listbox(self.frame_roles, width=40)
        scrollbar_roles = tk.Scrollbar(self.frame_roles, orient="vertical", command=self.listbox_roles.yview)
        self.listbox_roles.config(yscrollcommand=scrollbar_roles.set)
        btn_remove_role = tk.Button(self.frame_roles, text="Elimina Ruolo", command=lambda: ROLESERV.delete_role(self.listbox_roles, self.refresh_role_list))
        label_existing_roles.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.listbox_roles.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        scrollbar_roles.grid(row=3, column=2, sticky="ns")
        btn_remove_role.grid(row=4, column=1, padx=5, pady=5, sticky="e")

    def setup_employee_gui(self):
        tk.Label(self.frame_employee, text="Gestione Dipendenti", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)
        self.frame_employee.grid_columnconfigure(0, weight=0)
        self.frame_employee.grid_columnconfigure(1, weight=1)
        label_name = tk.Label(self.frame_employee, text="Nome Dipendente")
        entry_name = tk.Entry(self.frame_employee)
        label_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_name.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        label_hours = tk.Label(self.frame_employee, text="Ore Settimanali")
        entry_hours = tk.Entry(self.frame_employee)
        label_hours.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entry_hours.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        btn_insert_employee = tk.Button(self.frame_employee, text="Inserisci Dipendente", command=lambda: EMPSERV.insert_employee(entry_name, entry_hours, self.refresh_employee_list))
        btn_insert_employee.grid(row=4, column=1, padx=5, pady=(5, 20), sticky="e")

        label_existing_employees = tk.Label(self.frame_employee, text="Dipendenti Inseriti")
        self.listbox_employee = tk.Listbox(self.frame_employee, width=40)
        scrollbar_employee = tk.Scrollbar(self.frame_employee, orient="vertical", command=self.listbox_employee.yview)
        self.listbox_employee.config(yscrollcommand=scrollbar_employee.set)
        btn_remove_employee = tk.Button(self.frame_employee, text="Elimina Dipendente", command=lambda: EMPSERV.delete_employee(self.listbox_employee, self.refresh_employee_list))
        label_existing_employees.grid(row=5, column=0, padx=5, pady=5, sticky="nw")
        self.listbox_employee.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")
        scrollbar_employee.grid(row=5, column=2, sticky="ns")
        btn_remove_employee.grid(row=6, column=1, padx=5, pady=5, sticky="e")

        if len(EMPSERV.employees) > 0:
            self.on_cb_emp_name_change(EMPSERV.employees[0])

    def setup_room_gui(self):
        tk.Label(self.frame_rooms, text="Gestione Stanze", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)

        label_room_name = tk.Label(self.frame_rooms, text="Nome Stanza")
        entry_room_name = tk.Entry(self.frame_rooms)
        btn_insert_room = tk.Button(self.frame_rooms, text="Aggiungi Stanza", command=lambda: ROOMSERV.insert_room(entry_room_name, self.refresh_room_list))
        label_room_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_room_name.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        btn_insert_room.grid(row=2, column=1, padx=5, pady=(5, 20), sticky="e")

        label_existing_rooms = tk.Label(self.frame_roles, text="Ruoli Inseriti")
        self.listbox_rooms = tk.Listbox(self.frame_rooms, width=40)
        scrollbar_rooms = tk.Scrollbar(self.frame_rooms, orient="vertical", command=self.listbox_rooms.yview)
        self.listbox_rooms.config(yscrollcommand=scrollbar_rooms.set)
        btn_remove_room = tk.Button(self.frame_rooms, text="Elimina Stanza", command=lambda: ROOMSERV.delete_room(self.listbox_rooms, self.refresh_room_list))
        label_existing_rooms.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.listbox_rooms.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        scrollbar_rooms.grid(row=3, column=2, sticky="ns")
        btn_remove_room.grid(row=4, column=1, padx=5, pady=5, sticky="e")

    def setup_employee_roles_gui(self):
        tk.Label(self.frame_employee_roles, text="Associazione Dipendenti - Ruoli", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)
        self.frame_employee_roles.grid_columnconfigure(0, weight=0)
        self.frame_employee_roles.grid_columnconfigure(1, weight=1)
        label_emp_name = tk.Label(self.frame_employee_roles, text="Dipendente")
        self.cb_emp_name = ttk.Combobox(self.frame_employee_roles)
        self.cb_emp_name.bind("<<ComboboxSelected>>", self.on_cb_emp_name_change)
        label_emp_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cb_emp_name.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")   

        label_roles = tk.Label(self.frame_employee_roles, text="Ruolo")
        self.cb_role_name = ttk.Combobox(self.frame_employee_roles)
        label_roles.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.cb_role_name.grid(row=2, column=1, padx=5, pady=5, sticky="nsew") 
        btn_assign_role = tk.Button(self.frame_employee_roles, text="Assegna Ruolo", command=lambda: EMPSERV.assign_role(self.cb_emp_name, self.cb_role_name, self.refresh_assigned_role_list))
        btn_assign_role.grid(row=3, column=1, padx=5, pady=(5, 20), sticky="e")

        label_assigned_roles = tk.Label(self.frame_employee_roles, text="Ruoli Assegnati")
        self.listbox_assigned_roles = tk.Listbox(self.frame_employee_roles, width=40)
        scrollbar_assigned_roles = tk.Scrollbar(self.frame_employee_roles, orient="vertical", command=self.listbox_assigned_roles.yview)
        self.listbox_assigned_roles.config(yscrollcommand=scrollbar_assigned_roles.set)
        btn_remove_assigned_role = tk.Button(self.frame_employee_roles, text="Rimuovi Ruolo Assegnato", command=lambda: EMPSERV.remove_assigned_role(self.cb_emp_name, self.listbox_assigned_roles, self.refresh_assigned_role_list))
        label_assigned_roles.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
        self.listbox_assigned_roles.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        scrollbar_assigned_roles.grid(row=4, column=2, sticky="ns")
        btn_remove_assigned_role.grid(row=5, column=1, padx=5, pady=5, sticky="e")

    def setup_room_roles_gui(self):
        tk.Label(self.frame_room_roles, text="Associazione Stanze - Ruoli", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)

        label_room_name = tk.Label(self.frame_room_roles, text="Stanza")
        self.cb_room_name = ttk.Combobox(self.frame_room_roles)
        self.cb_room_name.bind("<<ComboboxSelected>>", self.on_cb_room_name_change)
        label_room_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cb_room_name.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")   

        label_roles = tk.Label(self.frame_room_roles, text="Ruolo")
        self.cb_room_role_name = ttk.Combobox(self.frame_room_roles)
        label_roles.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.cb_room_role_name.grid(row=2, column=1, padx=5, pady=5, sticky="nsew") 
        btn_assign_role = tk.Button(self.frame_room_roles, text="Aggiungi Ruolo", command=lambda: ROOMSERV.add_role(self.cb_room_name, self.cb_room_role_name, self.refresh_room_role_list))
        btn_assign_role.grid(row=3, column=1, padx=5, pady=(5, 20), sticky="e")

        label_room_roles = tk.Label(self.frame_room_roles, text="Ruoli Richiesti")
        self.listbox_room_roles = tk.Listbox(self.frame_room_roles, width=40)
        scrollbar_room_roles = tk.Scrollbar(self.frame_room_roles, orient="vertical", command=self.listbox_room_roles.yview)
        self.listbox_room_roles.config(yscrollcommand=scrollbar_room_roles.set)
        btn_remove_room_role = tk.Button(self.frame_room_roles, text="Rimuovi Ruolo Assegnato", command=lambda: ROOMSERV.remove_role(self.cb_room_name, self.listbox_room_roles, self.refresh_room_role_list))
        label_room_roles.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
        self.listbox_room_roles.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        scrollbar_room_roles.grid(row=4, column=2, sticky="ns")
        btn_remove_room_role.grid(row=5, column=1, padx=5, pady=5, sticky="e")

    def setup_export_gui(self):
        tk.Label(self.frame_export, text="Esporta Pianificazione", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)
        tk.Label(self.frame_export, text="Seleziona la cartella di destinazione").grid(row=1, column=0, columnspan=2)
        entry_export = tk.Entry(self.frame_export)
        entry_export.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        btn_browse = tk.Button(self.frame_export, text="Sfoglia", command=lambda: SCHEDSERV.browse_folder(entry_export))
        btn_browse.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        btn_export = tk.Button(self.frame_export, text="Esporta", command=lambda: SCHEDSERV.export_schedule(self))
        btn_export.grid(row=3, column=0, padx=5, pady=(10, 20), columnspan=2, sticky="ew")

    def refresh_role_list(self):
        self.listbox_roles.delete(0, tk.END)
        for role in ROLESERV.roles:
            self.listbox_roles.insert(tk.END, role)
        self.cb_role_name.delete(0, tk.END)
        self.cb_role_name["values"] = ROLESERV.roles    
        self.cb_room_role_name.delete(0, tk.END)
        self.cb_room_role_name["values"] = ROLESERV.roles

    def refresh_employee_list(self):
        self.listbox_employee.delete(0, tk.END)
        for employee in EMPSERV.employees:
            if(EMPSERV.employees[employee][1] == 1):
                self.listbox_employee.insert(tk.END, f"{employee} ({EMPSERV.employees[employee][1]} ora settimanale)")
            else:
                self.listbox_employee.insert(tk.END, f"{employee} ({EMPSERV.employees[employee][1]} ore settimanali)")
        self.cb_emp_name.delete(0, tk.END)
        emp = []
        for employee in EMPSERV.employees:
            emp.append(employee)
        self.cb_emp_name["values"] = emp
        self.on_cb_emp_name_change(self)

    def refresh_room_list(self):
        self.listbox_rooms.delete(0, tk.END)
        for room in ROOMSERV.rooms:
            self.listbox_rooms.insert(tk.END, room)
        self.cb_room_name.delete(0, tk.END)
        self.cb_room_name["values"] = ROOMSERV.rooms
        self.on_cb_room_name_change(self)
    
    def refresh_assigned_role_list(self):
        self.listbox_assigned_roles.delete(0, tk.END)
        for role in EMPSERV.assigned_roles:
            self.listbox_assigned_roles.insert(tk.END, role)

    def refresh_room_role_list(self):
        self.listbox_room_roles.delete(0, tk.END)
        if ROOMSERV.selected_room:
            for role, number in ROOMSERV.get_room_roles(ROOMSERV.selected_room).items():
                self.listbox_room_roles.insert(tk.END, f"{role} ({number})")

    def on_cb_emp_name_change(self, event):
        EMPSERV.set_selected_employee(self.cb_emp_name.get())
        self.refresh_assigned_role_list()

    def on_cb_room_name_change(self, event):  
        ROOMSERV.set_selected_room(self.cb_room_name.get())
        self.refresh_room_role_list()

    def load_initial_data(self):
        ROLESERV.roles = ROLESERV.get_roles()
        ROOMSERV.rooms = ROOMSERV.get_rooms()
        EMPSERV.employees = EMPSERV.get_employees()

        self.refresh_role_list()
        self.refresh_employee_list()
        self.refresh_room_list()
        
    def __init__(self, root):
        def setup_gui(root):
            self.root = root
            self.root.title("Gestione Ristorante")

            tabControl = ttk.Notebook(root)
            tab1 = ttk.Frame(tabControl)
            tab2 = ttk.Frame(tabControl)
            tabControl.add(tab1, text="Gestione Ruoli e Dipendenti")
            tabControl.add(tab2, text="Gestione Stanze")
            tabControl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

            self.frame_roles = tk.Frame(tab1, bd=2, relief="groove")
            self.frame_roles.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            self.frame_employee = tk.Frame(tab1, bd=2, relief="groove")
            self.frame_employee.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            self.frame_employee_roles = tk.Frame(tab1, bd=2, relief="groove")
            self.frame_employee_roles.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

            self.frame_rooms = tk.Frame(tab2, bd=2, relief="groove")
            self.frame_rooms.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            self.frame_room_roles = tk.Frame(tab2, bd=2, relief="groove")
            self.frame_room_roles.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            self.frame_export = tk.Frame(tab2, bd=2, relief="groove")
            self.frame_export.grid(row=0, column=2, padx=5, pady=5)

            # Configure row and column weights to center frame_export
            tab2.grid_rowconfigure(0, weight=1)
            tab2.grid_columnconfigure(2, weight=1)
            self.frame_export.grid_rowconfigure(0, weight=1)
            self.frame_export.grid_columnconfigure(0, weight=1)

            self.setup_role_gui()
            self.setup_employee_gui()
            self.setup_room_gui()
            self.setup_employee_roles_gui()
            self.setup_room_roles_gui()
            self.setup_export_gui()

        setup_gui(root)

        # FOR TESTING PURPOSES // ¡¡¡ WILL DELETE ANY EXISTING DATA IN THE DB !!!
        # create_test_tables()
        
        self. load_initial_data() 

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantManagementApp(root)
    root.mainloop()
