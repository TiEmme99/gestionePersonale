import tkinter as tk
from tkinter import messagebox
import sqlite3
import openpyxl
from openpyxl import Workbook

# Costanti per i giorni della settimana
GIORNI_SETTIMANA = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

# Classe Dipendente per gestire le informazioni sui dipendenti
class Dipendente:
    def __init__(self, nome, ore_disponibili, ruoli=None):
        self.nome = nome
        self.ore_disponibili = ore_disponibili
        self.ruoli = ruoli if ruoli else []  # Lista di ruoli associati al dipendente

    def __str__(self):
        return f"{self.nome} - Ore disponibili: {self.ore_disponibili} - Ruoli: {', '.join(self.ruoli)}"

# Classe Ruolo per gestire le informazioni sui ruoli
class Ruolo:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return f"Ruolo: {self.nome}"

# Classe Ristorante per gestire gli orari settimanali del ristorante
class Ristorante:
    def __init__(self, connection):
        self.connection = connection
        self.orari_settimanali = {}
        self.carica_orari_da_db()

    def carica_orari_da_db(self):
        # Recupera gli orari settimanali dal database
        cursor = self.connection.cursor()
        cursor.execute("SELECT giorno, apertura, chiusura FROM orari_settimanali")
        rows = cursor.fetchall()
        for row in rows:
            giorno, apertura, chiusura = row
            self.orari_settimanali[giorno] = {"apertura": apertura, "chiusura": chiusura}

    def modifica_orario_giorno(self, giorno, apertura, chiusura):
        if giorno in GIORNI_SETTIMANA:
            self.orari_settimanali[giorno] = {"apertura": apertura, "chiusura": chiusura}
            # Aggiorna il database con i nuovi orari
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE orari_settimanali SET apertura=?, chiusura=? WHERE giorno=?",
                (apertura, chiusura, giorno)
            )
            self.connection.commit()
            return True
        return False

    def __str__(self):
        orari_str = "Orari Settimanali del Ristorante:\n"
        for giorno in GIORNI_SETTIMANA:
            orari = self.orari_settimanali.get(giorno, {"apertura": "00:00", "chiusura": "00:00"})
            orari_str += f"{giorno}: Apertura: {orari['apertura']}, Chiusura: {orari['chiusura']}\n"
        return orari_str

# Classe GestioneRistorante per gestire dipendenti, ruoli e stanze
class GestioneRistorante:
    def __init__(self, connection):
        self.connection = connection
        self.dipendenti = []
        self.stanze = []  # Lista di stanze
        self.ruoli = []  # Lista di ruoli
        self.num_persone_stanze_ruolo = {}  # Dizionario che associa stanze a numero di persone per ruolo
        self.orari = Ristorante(connection)
        self.carica_dipendenti_da_db()
        self.carica_ruoli_da_db()

    # Carica dipendenti dal database
    def carica_dipendenti_da_db(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT d.nome, d.ore_disponibili, r.nome FROM dipendenti d
            LEFT JOIN dipendenti_ruoli dr ON d.nome = dr.dipendente_nome
            LEFT JOIN ruoli r ON dr.ruolo_nome = r.nome
        """)
        rows = cursor.fetchall()
        dipendenti_dict = {}
        for nome, ore_disponibili, ruolo in rows:
            if nome not in dipendenti_dict:
                dipendenti_dict[nome] = Dipendente(nome, ore_disponibili, [])
            if ruolo:
                dipendenti_dict[nome].ruoli.append(ruolo)
        self.dipendenti = list(dipendenti_dict.values())

    # Carica ruoli dal database
    def carica_ruoli_da_db(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT nome FROM ruoli")
        rows = cursor.fetchall()
        self.ruoli = [Ruolo(nome) for nome, in rows]

    # CRUD Dipendenti
    def aggiungi_dipendente(self, nome, ore_disponibili, ruoli):
        dipendente = Dipendente(nome, ore_disponibili, ruoli)
        self.dipendenti.append(dipendente)
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO dipendenti (nome, ore_disponibili) VALUES (?, ?)",
            (nome, ore_disponibili)
        )
        for ruolo in ruoli:
            cursor.execute(
                "INSERT INTO dipendenti_ruoli (dipendente_nome, ruolo_nome) VALUES (?, ?)",
                (nome, ruolo)
            )
        self.connection.commit()

    def rimuovi_dipendente(self, nome):
        self.dipendenti = [d for d in self.dipendenti if d.nome != nome]
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM dipendenti WHERE nome=?", (nome,))
        cursor.execute("DELETE FROM dipendenti_ruoli WHERE dipendente_nome=?", (nome,))
        self.connection.commit()

    def modifica_dipendente(self, vecchio_nome, nuovo_nome, nuove_ore, nuovi_ruoli):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE dipendenti SET nome=?, ore_disponibili=? WHERE nome=?", (nuovo_nome, nuove_ore, vecchio_nome))
        cursor.execute("DELETE FROM dipendenti_ruoli WHERE dipendente_nome=?", (vecchio_nome,))
        for ruolo in nuovi_ruoli:
            cursor.execute("INSERT INTO dipendenti_ruoli (dipendente_nome, ruolo_nome) VALUES (?, ?)", (nuovo_nome, ruolo))
        self.connection.commit()

    # CRUD Ruoli
    def aggiungi_ruolo(self, nome):
        ruolo = Ruolo(nome)
        self.ruoli.append(ruolo)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO ruoli (nome) VALUES (?)", (nome,))
        self.connection.commit()

    def rimuovi_ruolo(self, nome):
        self.ruoli = [r for r in self.ruoli if r.nome != nome]
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM ruoli WHERE nome=?", (nome,))
        self.connection.commit()

    # CRUD Stanze
    def aggiungi_stanza(self, nome_stanza, persone_ruoli):
        self.stanze.append(nome_stanza)
        self.num_persone_stanze_ruolo[nome_stanza] = persone_ruoli
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO stanze (nome) VALUES (?)", (nome_stanza,))
        for ruolo, numero_persone in persone_ruoli.items():
            cursor.execute(
                "INSERT INTO stanze_ruoli (stanza_nome, ruolo_nome, numero_persone) VALUES (?, ?, ?)",
                (nome_stanza, ruolo, numero_persone)
            )
        self.connection.commit()

    def modifica_stanza(self, nome_stanza, persone_ruoli):
        self.num_persone_stanze_ruolo[nome_stanza] = persone_ruoli
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM stanze_ruoli WHERE stanza_nome=?", (nome_stanza,))
        for ruolo, numero_persone in persone_ruoli.items():
            cursor.execute(
                "INSERT INTO stanze_ruoli (stanza_nome, ruolo_nome, numero_persone) VALUES (?, ?, ?)",
                (nome_stanza, ruolo, numero_persone)
            )
        self.connection.commit()

    def rimuovi_stanza(self, nome_stanza):
        self.stanze.remove(nome_stanza)
        del self.num_persone_stanze_ruolo[nome_stanza]
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM stanze WHERE nome=?", (nome_stanza,))
        cursor.execute("DELETE FROM stanze_ruoli WHERE stanza_nome=?", (nome_stanza,))
        self.connection.commit()

    # Pianificazione settimanale
    def genera_pianificazione_settimanale(self):
        pianificazione = []
        dipendenti_copia = [Dipendente(d.nome, d.ore_disponibili, d.ruoli) for d in self.dipendenti]

        for giorno in GIORNI_SETTIMANA:
            ore_giornaliere = self.calcola_ore_giornaliere(giorno)
            ore_giornaliere_rimanenti = ore_giornaliere
            giorno_pianificazione = []

            for stanza, persone_ruoli in self.num_persone_stanze_ruolo.items():
                for ruolo, persone_necessarie in persone_ruoli.items():
                    persone_assegnate = []
                    while persone_necessarie > 0 and ore_giornaliere_rimanenti > 0 and dipendenti_copia:
                        dipendente = next((d for d in dipendenti_copia if ruolo in d.ruoli), None)
                        if not dipendente:
                            break
                        ore_assegnabili = min(dipendente.ore_disponibili, ore_giornaliere_rimanenti)
                        if ore_assegnabili > 0:
                            persone_assegnate.append((dipendente.nome, ore_assegnabili, ruolo))
                            dipendente.ore_disponibili -= ore_assegnabili
                            ore_giornaliere_rimanenti -= ore_assegnabili
                            persone_necessarie -= 1

                    giorno_pianificazione.append((stanza, persone_assegnate))

            pianificazione.append((giorno, giorno_pianificazione))
        return pianificazione

    def calcola_ore_giornaliere(self, giorno):
        orari = self.orari.orari_settimanali[giorno]
        apertura_ore, apertura_minuti = map(int, orari['apertura'].split(':'))
        chiusura_ore, chiusura_minuti = map(int, orari['chiusura'].split(':'))
        apertura_totale_minuti = apertura_ore * 60 + apertura_minuti
        chiusura_totale_minuti = chiusura_ore * 60 + chiusura_minuti
        ore_giornaliere = (chiusura_totale_minuti - apertura_totale_minuti) / 60
        return max(0, ore_giornaliere)  # Assicura che le ore non siano negative

    def esporta_pianificazione_excel(self, file_path="pianificazione_settimanale.xlsx"):
        pianificazione = self.genera_pianificazione_settimanale()
        wb = Workbook()
        
        for giorno, assegnazioni in pianificazione:
            ws = wb.create_sheet(title=giorno)
            ws.append(["Stanza", "Dipendente", "Ore", "Ruolo"])
            for stanza, persone_assegnate in assegnazioni:
                for dipendente, ore, ruolo in persone_assegnate:
                    ws.append([stanza, dipendente, ore, ruolo])
        
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])

        wb.save(file_path)

# Classe principale dell'applicazione GUI per la gestione del ristorante
class GestioneRistoranteApp:
    def __init__(self, root):
        self.connection = sqlite3.connect('gestione_ristorante.db')
        self.crea_tabelle()

        self.gestione = GestioneRistorante(self.connection)

        self.root = root
        self.root.title("Gestione Ristorante")
        self.root.minsize(1200, 600)

        # Crea una finestra con scrollbar verticale
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

        # CRUD dipendenti (a sinistra)
        self.frame_personale = tk.Frame(self.scrollable_frame, bd=2, relief="groove")
        self.frame_personale.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.label_personale = tk.Label(self.frame_personale, text="Gestione Personale", font=("Helvetica", 16))
        self.label_personale.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.label_nome = tk.Label(self.frame_personale, text="Nome:")
        self.label_nome.grid(row=1, column=0, sticky="e")

        self.entry_nome = tk.Entry(self.frame_personale)
        self.entry_nome.grid(row=1, column=1, sticky="ew")

        self.label_ore = tk.Label(self.frame_personale, text="Ore Settimanali:")
        self.label_ore.grid(row=2, column=0, sticky="e")

        self.entry_ore = tk.Entry(self.frame_personale)
        self.entry_ore.grid(row=2, column=1, sticky="ew")

        self.label_ruolo_personale = tk.Label(self.frame_personale, text="Ruolo:")
        self.label_ruolo_personale.grid(row=3, column=0, sticky="e")

        self.listbox_ruoli_personale = tk.Listbox(self.frame_personale, selectmode=tk.MULTIPLE)
        self.listbox_ruoli_personale.grid(row=3, column=1, sticky="ew")

        self.button_aggiungi_personale = tk.Button(self.frame_personale, text="Aggiungi Personale", command=self.aggiungi_personale)
        self.button_aggiungi_personale.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.listbox_personale = tk.Listbox(self.frame_personale, width=40)
        self.listbox_personale.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.button_rimuovi_personale = tk.Button(self.frame_personale, text="Rimuovi Personale", command=self.rimuovi_personale)
        self.button_rimuovi_personale.grid(row=6, column=0, columnspan=2, sticky="ew")

        self.button_modifica_personale = tk.Button(self.frame_personale, text="Modifica Personale", command=self.modifica_personale)
        self.button_modifica_personale.grid(row=7, column=0, columnspan=2, sticky="ew")

        # CRUD stanze (a destra)
        self.frame_stanze = tk.Frame(self.scrollable_frame, bd=2, relief="groove")
        self.frame_stanze.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.label_stanze = tk.Label(self.frame_stanze, text="Gestione Stanze", font=("Helvetica", 16))
        self.label_stanze.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.label_nome_stanza = tk.Label(self.frame_stanze, text="Nome Stanza:")
        self.label_nome_stanza.grid(row=1, column=0, sticky="e")

        self.entry_nome_stanza = tk.Entry(self.frame_stanze)
        self.entry_nome_stanza.grid(row=1, column=1, sticky="ew")

        self.label_num_persone_ruolo = tk.Label(self.frame_stanze, text="Numero di persone per ruolo:")
        self.label_num_persone_ruolo.grid(row=2, column=0, sticky="e")

        self.listbox_ruoli_stanze = tk.Listbox(self.frame_stanze, selectmode=tk.SINGLE)
        self.listbox_ruoli_stanze.grid(row=2, column=1, sticky="ew")

        self.entry_num_persone_ruolo = tk.Entry(self.frame_stanze)
        self.entry_num_persone_ruolo.grid(row=3, column=1, sticky="ew")

        self.button_aggiungi_stanza = tk.Button(self.frame_stanze, text="Aggiungi Stanza", command=self.aggiungi_stanza)
        self.button_aggiungi_stanza.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.listbox_stanze = tk.Listbox(self.frame_stanze, width=40)
        self.listbox_stanze.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.button_rimuovi_stanza = tk.Button(self.frame_stanze, text="Rimuovi Stanza", command=self.rimuovi_stanza)
        self.button_rimuovi_stanza.grid(row=6, column=0, columnspan=2, sticky="ew")

        # Gestione Ruoli (sotto)
        self.frame_ruoli = tk.Frame(self.scrollable_frame, bd=2, relief="groove")
        self.frame_ruoli.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.label_ruoli = tk.Label(self.frame_ruoli, text="Gestione Ruoli", font=("Helvetica", 16))
        self.label_ruoli.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.label_nome_ruolo = tk.Label(self.frame_ruoli, text="Nome Ruolo:")
        self.label_nome_ruolo.grid(row=1, column=0, sticky="e")

        self.entry_nome_ruolo = tk.Entry(self.frame_ruoli)
        self.entry_nome_ruolo.grid(row=1, column=1, sticky="ew")

        self.button_aggiungi_ruolo = tk.Button(self.frame_ruoli, text="Aggiungi Ruolo", command=self.aggiungi_ruolo)
        self.button_aggiungi_ruolo.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.listbox_ruoli = tk.Listbox(self.frame_ruoli, width=40)
        self.listbox_ruoli.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.button_rimuovi_ruolo = tk.Button(self.frame_ruoli, text="Rimuovi Ruolo", command=self.rimuovi_ruolo)
        self.button_rimuovi_ruolo.grid(row=4, column=0, columnspan=2, sticky="ew")

        # Esportazione in Excel
        self.button_export_excel = tk.Button(self.frame_ruoli, text="Esporta Pianificazione in Excel",
                                             command=self.esporta_pianificazione_excel)
        self.button_export_excel.grid(row=5, column=0, columnspan=2, sticky="ew")

        # Aggiorna le liste
        self.aggiorna_lista_personale()
        self.aggiorna_lista_stanze()
        self.aggiorna_lista_ruoli()

    def crea_tabelle(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dipendenti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                ore_disponibili INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ruoli (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dipendenti_ruoli (
                dipendente_nome TEXT NOT NULL,
                ruolo_nome TEXT NOT NULL,
                FOREIGN KEY (dipendente_nome) REFERENCES dipendenti(nome),
                FOREIGN KEY (ruolo_nome) REFERENCES ruoli(nome)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stanze (
                nome TEXT PRIMARY KEY
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stanze_ruoli (
                stanza_nome TEXT NOT NULL,
                ruolo_nome TEXT NOT NULL,
                numero_persone INTEGER NOT NULL,
                FOREIGN KEY (stanza_nome) REFERENCES stanze(nome),
                FOREIGN KEY (ruolo_nome) REFERENCES ruoli(nome)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orari_settimanali (
                giorno TEXT PRIMARY KEY,
                apertura TEXT NOT NULL,
                chiusura TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def aggiungi_personale(self):
        nome = self.entry_nome.get()
        try:
            ore_disponibili = int(self.entry_ore.get())
            ruoli_selezionati = [self.listbox_ruoli_personale.get(i) for i in self.listbox_ruoli_personale.curselection()]
            if nome and ore_disponibili >= 0:
                self.gestione.aggiungi_dipendente(nome, ore_disponibili, ruoli_selezionati)
                self.aggiorna_lista_personale()
                self.entry_nome.delete(0, tk.END)
                self.entry_ore.delete(0, tk.END)
            else:
                messagebox.showerror("Errore", "Nome o ore non validi!")
        except ValueError:
            messagebox.showerror("Errore", "Le ore devono essere un numero intero!")

    def rimuovi_personale(self):
        try:
            nome = self.listbox_personale.get(tk.ACTIVE).split(" - ")[0]
            self.gestione.rimuovi_dipendente(nome)
            self.aggiorna_lista_personale()
        except IndexError:
            messagebox.showerror("Errore", "Seleziona un dipendente dalla lista.")

    def modifica_personale(self):
        try:
            nome_selezionato = self.listbox_personale.get(tk.ACTIVE).split(" - ")[0]
            nuovo_nome = self.entry_nome.get()
            nuove_ore = int(self.entry_ore.get())
            ruoli_selezionati = [self.listbox_ruoli_personale.get(i) for i in self.listbox_ruoli_personale.curselection()]

            if nuovo_nome and nuove_ore >= 0:
                self.gestione.modifica_dipendente(nome_selezionato, nuovo_nome, nuove_ore, ruoli_selezionati)
                self.aggiorna_lista_personale()
                self.entry_nome.delete(0, tk.END)
                self.entry_ore.delete(0, tk.END)
            else:
                messagebox.showerror("Errore", "Nome o ore non validi!")
        except (ValueError, IndexError):
            messagebox.showerror("Errore", "Seleziona un dipendente e inserisci valori validi.")

    def aggiorna_lista_personale(self):
        self.listbox_personale.delete(0, tk.END)
        for dipendente in self.gestione.dipendenti:
            self.listbox_personale.insert(tk.END, str(dipendente))

    def aggiungi_stanza(self):
        nome_stanza = self.entry_nome_stanza.get()
        try:
            ruolo = self.listbox_ruoli_stanze.get(tk.ACTIVE)
            num_persone = int(self.entry_num_persone_ruolo.get())
            persone_ruoli = {ruolo: num_persone}
            if nome_stanza and num_persone > 0:
                self.gestione.aggiungi_stanza(nome_stanza, persone_ruoli)
                self.aggiorna_lista_stanze()
                self.entry_nome_stanza.delete(0, tk.END)
                self.entry_num_persone_ruolo.delete(0, tk.END)
            else:
                messagebox.showerror("Errore", "Nome della stanza o numero di persone non validi!")
        except ValueError:
            messagebox.showerror("Errore", "Il numero di persone deve essere un numero intero positivo!")

    def rimuovi_stanza(self):
        nome_stanza = self.entry_nome_stanza.get()
        self.gestione.rimuovi_stanza(nome_stanza)
        self.aggiorna_lista_stanze()
        self.entry_nome_stanza.delete(0, tk.END)

    def aggiorna_lista_stanze(self):
        self.listbox_stanze.delete(0, tk.END)
        for stanza in self.gestione.stanze:
            persone_ruoli = self.gestione.num_persone_stanze_ruolo[stanza]
            descrizione_stanza = f"{stanza}: {', '.join([f'{ruolo} ({num})' for ruolo, num in persone_ruoli.items()])}"
            self.listbox_stanze.insert(tk.END, descrizione_stanza)

    def aggiungi_ruolo(self):
        nome_ruolo = self.entry_nome_ruolo.get()
        if nome_ruolo:
            self.gestione.aggiungi_ruolo(nome_ruolo)
            self.aggiorna_lista_ruoli()
            self.entry_nome_ruolo.delete(0, tk.END)
        else:
            messagebox.showerror("Errore", "Inserisci un nome per il ruolo!")

    def rimuovi_ruolo(self):
        nome_ruolo = self.listbox_ruoli.get(tk.ACTIVE)
        if nome_ruolo:
            self.gestione.rimuovi_ruolo(nome_ruolo)
            self.aggiorna_lista_ruoli()
        else:
            messagebox.showerror("Errore", "Seleziona un ruolo dalla lista!")

    def aggiorna_lista_ruoli(self):
        self.listbox_ruoli.delete(0, tk.END)
        self.listbox_ruoli_personale.delete(0, tk.END)
        self.listbox_ruoli_stanze.delete(0, tk.END)
        for ruolo in self.gestione.ruoli:
            self.listbox_ruoli.insert(tk.END, ruolo.nome)
            self.listbox_ruoli_personale.insert(tk.END, ruolo.nome)
            self.listbox_ruoli_stanze.insert(tk.END, ruolo.nome)

    def esporta_pianificazione_excel(self):
        self.gestione.esporta_pianificazione_excel()
        messagebox.showinfo("Esportazione completata", "La pianificazione settimanale è stata esportata in Excel.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestioneRistoranteApp(root)
    root.mainloop()
