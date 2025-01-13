import tkinter as tk
import repositories.RoomRepository as ROOMREPO
from tkinter import messagebox

rooms = []
room_roles = {} # {role_name: employee_number}
selected_room = ""

def get_rooms():
    return ROOMREPO.get_rooms()

def insert_room(entry_room_name, callback):
    room_name = entry_room_name.get()
    if room_name:
        try:
            ROOMREPO.insert_room(room_name)
            rooms.append(room_name)
            entry_room_name.delete(0, tk.END)
            callback()  
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiunta della stanza: {e}")
    else:
        messagebox.showerror("Errore", "Inserisci un nome per la stanza")

def delete_room(listbox_rooms, callback):
    room_name = listbox_rooms.get(tk.ACTIVE)
    if room_name:
        ROOMREPO.delete_room(room_name)
        rooms.remove(room_name)
        callback()
    else:
        messagebox.showerror("Errore", "Nessuna stanza selezionata")

def get_room_roles(room_name):
    return ROOMREPO.get_room_roles(room_name)

def explode_roles(room_roles):
    exploded_roles = []
    for role, number in room_roles.items():
        for _ in range(number):
            exploded_roles.append(role)
    return exploded_roles

def add_role(cb_room_name, cb_role_name, callback):
    room_name = cb_room_name.get()
    role_name = cb_role_name.get()
    try:
        if room_name and role_name:
            if role_name in room_roles:
                room_roles[role_name] += 1
            else:
                room_roles[role_name] = 1
            ROOMREPO.add_role(room_name, role_name, room_roles.get(role_name))
            callback()
        else:
            messagebox.showerror("Errore", "Seleziona una stanza e un ruolo")
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def remove_role(cb_room_name, listbox_roles, callback):
    room_name = cb_room_name.get()
    if room_name and listbox_roles.curselection():
        role_name = listbox_roles.get(listbox_roles.curselection()[0]).split(" (")[0]
        room_roles[role_name] -= 1
        ROOMREPO.remove_role(room_name, role_name, room_roles[role_name])
        if room_roles[role_name] == 0:
            room_roles.pop(role_name)
        callback()
    else:
        messagebox.showerror("Errore", "Seleziona un ruolo assegnato alla stanza")

def set_selected_room(room_name):
    global room_roles
    global selected_room
    if room_name:
        selected_room = room_name
        room_roles = ROOMREPO.get_room_roles(room_name) or {}
    else:
        room_roles = {}
        selected_room = ""