import tkinter as tk
import repositories.RoleRepository as ROLEREPO
from tkinter import messagebox

roles = []

def get_roles():
    return ROLEREPO.get_roles()


def insert_role(entry_role_name, callback):
    role_name = entry_role_name.get()
    if role_name:
        try:
            ROLEREPO.insert_role(role_name)
            roles.append(role_name)
            entry_role_name.delete(0, tk.END)
            callback()
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiunta del ruolo: {e}")
    else:
        messagebox.showerror("Errore", "Inserisci un nome per il ruolo")

def delete_role(listbox_roles, callback):
    role_name = listbox_roles.get(tk.ACTIVE)
    if role_name:
        try:
            ROLEREPO.delete_role(role_name)
            roles.remove(role_name)
            callback()
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la rimozione del ruolo: {e}")
    else:
        messagebox.showerror("Errore", "Nessun ruolo selezionato")