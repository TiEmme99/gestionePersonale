import tkinter as tk
from tkinter import messagebox
import sqlite3

# Costanti per i giorni della settimana
GIORNI_SETTIMANA = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

# Classe Dipendente per gestire le informazioni sui dipendenti
class Dipendente:
    def __init__(self, nome, ore_disponibili):
        self.nome = nome
        self.ore_disponibili = ore_disponibili

    def __str__(self):
        return f"{self.nome} - Ore disponibili: {self.ore_disponibili}"

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

# Classe GestioneRistorante per gestire i dipendenti e gli orari del ristorante
class GestioneRistorante:
    def __init__(self, connection):
        self.connection = connection
        self.dipendenti = []
        self.orari = Ristorante(connection)
        self.carica_dipendenti_da_db()

    def carica_dipendenti_da_db(self):
        # Recupera i dipendenti dal database
        cursor = self.connection.cursor()
        cursor.execute("SELECT nome, ore_disponibili FROM dipendenti")
        rows = cursor.fetchall()
        self.dipendenti = [Dipendente(nome, ore_disponibili) for nome, ore_disponibili in rows]

    def aggiungi_dipendente(self, nome, ore_disponibili):
        dipendente = Dipendente(nome, ore_disponibili)
        self.dipendenti.append(dipendente)
        # Inserisce il nuovo dipendente nel database
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO dipendenti (nome, ore_disponibili) VALUES (?, ?)",
            (nome, ore_disponibili)
        )
        self.connection.commit()

    def rimuovi_dipendente(self, nome):
        self.dipendenti = [d for d in self.dipendenti if d.nome != nome]
        # Rimuove il dipendente dal database
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM dipendenti WHERE nome=?", (nome,))
        self.connection.commit()

    def modifica_ore_dipendente(self, nome, nuove_ore):
        for dipendente in self.dipendenti:
            if dipendente.nome == nome:
                dipendente.ore_disponibili = nuove_ore
                break
        # Aggiorna le ore del dipendente nel database
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE dipendenti SET ore_disponibili=? WHERE nome=?",
            (nuove_ore, nome)
        )
        self.connection.commit()

    def modifica_orari_ristorante(self, giorno, apertura, chiusura):
        return self.orari.modifica_orario_giorno(giorno, apertura, chiusura)

    def genera_pianificazione_settimanale(self):
        pianificazione = []
        
        # Copia temporanea degli oggetti Dipendente per la pianificazione
        dipendenti_copia = [Dipendente(d.nome, d.ore_disponibili) for d in self.dipendenti]

        for giorno in GIORNI_SETTIMANA:
            ore_giornaliere = self.calcola_ore_giornaliere(giorno)
            ore_giornaliere_rimanenti = ore_giornaliere
            giorno_pianificazione = []

            for dipendente in dipendenti_copia:
                if ore_giornaliere_rimanenti <= 0:
                    break
                ore_assegnabili = min(dipendente.ore_disponibili, ore_giornaliere_rimanenti)
                giorno_pianificazione.append((dipendente.nome, ore_assegnabili))
                dipendente.ore_disponibili -= ore_assegnabili
                ore_giornaliere_rimanenti -= ore_assegnabili

            pianificazione.append((giorno, giorno_pianificazione))

        output = ""
        for giorno, assegnazioni in pianificazione:
            output += f"{giorno}:\n"
            for dipendente, ore in assegnazioni:
                output += f"  {dipendente}: {ore} ore\n"
            output += "\n"

        return output

    def calcola_ore_giornaliere(self, giorno):
        orari = self.orari.orari_settimanali[giorno]
        apertura_ore, apertura_minuti = map(int, orari['apertura'].split(':'))
        chiusura_ore, chiusura_minuti = map(int, orari['chiusura'].split(':'))
        apertura_totale_minuti = apertura_ore * 60 + apertura_minuti
        chiusura_totale_minuti = chiusura_ore * 60 + chiusura_minuti
        ore_giornaliere = (chiusura_totale_minuti - apertura_totale_minuti) / 60
        return max(0, ore_giornaliere)  # Assicura che le ore non siano negative

    def visualizza_dipendenti(self):
        return [str(dipendente) for dipendente in self.dipendenti]

    def visualizza_orari_ristorante(self):
        return str(self.orari)


# Classe principale dell'applicazione GUI per la gestione del ristorante
class GestioneRistoranteApp:
    def __init__(self, root):
        # Connessione al database SQLite
        self.connection = sqlite3.connect('gestione_ristorante.db')
        self.crea_tabelle()

        # Creazione dell'oggetto GestioneRistorante
        self.gestione = GestioneRistorante(self.connection)

        # Creazione della finestra principale
        self.root = root
        self.root.title("Gestione Ristorante")
        self.root.geometry("600x700")

        # Tabella per i dipendenti
        self.frame_dipendenti = tk.Frame(self.root)
        self.frame_dipendenti.pack(pady=10)

        self.label_dipendenti = tk.Label(self.frame_dipendenti, text="Gestione Dipendenti", font=("Helvetica", 16))
        self.label_dipendenti.pack()

        self.label_nome = tk.Label(self.frame_dipendenti, text="Nome Dipendente:")
        self.label_nome.pack()

        self.entry_nome = tk.Entry(self.frame_dipendenti)
        self.entry_nome.pack()

        self.label_ore = tk.Label(self.frame_dipendenti, text="Ore Settimanali Disponibili:")
        self.label_ore.pack()

        self.entry_ore = tk.Entry(self.frame_dipendenti)
        self.entry_ore.pack()

        self.button_aggiungi = tk.Button(self.frame_dipendenti, text="Aggiungi Dipendente", command=self.aggiungi_dipendente)
        self.button_aggiungi.pack(pady=5)

        self.button_rimuovi = tk.Button(self.frame_dipendenti, text="Rimuovi Dipendente", command=self.rimuovi_dipendente)
        self.button_rimuovi.pack(pady=5)

        self.button_modifica = tk.Button(self.frame_dipendenti, text="Modifica Ore Dipendente", command=self.modifica_ore_dipendente)
        self.button_modifica.pack(pady=5)

        self.listbox_dipendenti = tk.Listbox(self.frame_dipendenti, width=50)
        self.listbox_dipendenti.pack(pady=5)

        # Tabella per gli orari settimanali
        self.frame_orari = tk.Frame(self.root)
        self.frame_orari.pack(pady=10)

        self.label_orari = tk.Label(self.frame_orari, text="Orari Settimanali del Ristorante", font=("Helvetica", 16))
        self.label_orari.pack()

        self.orari_inputs = {}
        for giorno in GIORNI_SETTIMANA:
            frame_giorno = tk.Frame(self.frame_orari)
            frame_giorno.pack(pady=5)

            label_giorno = tk.Label(frame_giorno, text=giorno)
            label_giorno.grid(row=0, column=0, padx=5)

            label_apertura = tk.Label(frame_giorno, text="Apertura:")
            label_apertura.grid(row=0, column=1, padx=5)

            entry_apertura = tk.Entry(frame_giorno, width=10)
            entry_apertura.grid(row=0, column=2, padx=5)

            label_chiusura = tk.Label(frame_giorno, text="Chiusura:")
            label_chiusura.grid(row=0, column=3, padx=5)

            entry_chiusura = tk.Entry(frame_giorno, width=10)
            entry_chiusura.grid(row=0, column=4, padx=5)

            self.orari_inputs[giorno] = {"apertura": entry_apertura, "chiusura": entry_chiusura}

        self.button_modifica_orari = tk.Button(self.frame_orari, text="Modifica Orari Settimanali", command=self.modifica_orari)
        self.button_modifica_orari.pack(pady=5)

        self.label_orari_attuali = tk.Label(self.frame_orari, text="")
        self.label_orari_attuali.pack()

        # Output della pianificazione settimanale
        self.frame_pianificazione = tk.Frame(self.root)
        self.frame_pianificazione.pack(pady=10)

        self.button_pianificazione = tk.Button(self.frame_pianificazione, text="Genera Pianificazione Settimanale", command=self.genera_pianificazione)
        self.button_pianificazione.pack(pady=5)

        self.text_pianificazione = tk.Text(self.frame_pianificazione, height=10, width=60)
        self.text_pianificazione.pack()

        # Aggiornamento iniziale della UI
        self.aggiorna_lista_dipendenti()
        self.aggiorna_orari_ristorante()

    def crea_tabelle(self):
        # Creazione delle tabelle nel database SQLite se non esistono
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dipendenti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                ore_disponibili INTEGER NOT NULL
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

        # Inserimento di orari default se non esistono
        cursor.execute("SELECT COUNT(*) FROM orari_settimanali")
        count = cursor.fetchone()[0]
        if count == 0:
            for giorno in GIORNI_SETTIMANA:
                cursor.execute(
                    "INSERT INTO orari_settimanali (giorno, apertura, chiusura) VALUES (?, ?, ?)",
                    (giorno, "09:00", "17:00")
                )
            self.connection.commit()

    def aggiungi_dipendente(self):
        nome = self.entry_nome.get()
        try:
            ore_disponibili = int(self.entry_ore.get())
            if nome and ore_disponibili >= 0:
                self.gestione.aggiungi_dipendente(nome, ore_disponibili)
                self.aggiorna_lista_dipendenti()
                self.entry_nome.delete(0, tk.END)
                self.entry_ore.delete(0, tk.END)
            else:
                messagebox.showerror("Errore", "Nome o ore non validi!")
        except ValueError:
            messagebox.showerror("Errore", "Le ore devono essere un numero intero!")

    def rimuovi_dipendente(self):
        nome = self.entry_nome.get()
        self.gestione.rimuovi_dipendente(nome)
        self.aggiorna_lista_dipendenti()
        self.entry_nome.delete(0, tk.END)

    def modifica_ore_dipendente(self):
        nome = self.entry_nome.get()
        try:
            nuove_ore = int(self.entry_ore.get())
            if nome and nuove_ore >= 0:
                self.gestione.modifica_ore_dipendente(nome, nuove_ore)
                self.aggiorna_lista_dipendenti()
                self.entry_nome.delete(0, tk.END)
                self.entry_ore.delete(0, tk.END)
            else:
                messagebox.showerror("Errore", "Nome o ore non validi!")
        except ValueError:
            messagebox.showerror("Errore", "Le ore devono essere un numero intero!")

    def modifica_orari(self):
        orari_settimanali = {}
        for giorno, widgets in self.orari_inputs.items():
            apertura = widgets["apertura"].get()
            chiusura = widgets["chiusura"].get()
            if self.valida_orari(apertura) and self.valida_orari(chiusura):
                orari_settimanali[giorno] = (apertura, chiusura)
            else:
                messagebox.showerror("Errore", f"Gli orari per {giorno} non sono validi. Devono essere nel formato HH:MM.")
                return
        
        for giorno, (apertura, chiusura) in orari_settimanali.items():
            self.gestione.modifica_orari_ristorante(giorno, apertura, chiusura)
        
        self.aggiorna_orari_ristorante()

    def valida_orari(self, orario):
        try:
            ore, minuti = map(int, orario.split(':'))
            return 0 <= ore <= 23 and 0 <= minuti <= 59
        except ValueError:
            return False

    def aggiorna_lista_dipendenti(self):
        self.listbox_dipendenti.delete(0, tk.END)
        for dipendente in self.gestione.visualizza_dipendenti():
            self.listbox_dipendenti.insert(tk.END, dipendente)

    def aggiorna_orari_ristorante(self):
        orari = self.gestione.visualizza_orari_ristorante()
        self.label_orari_attuali.config(text=orari)

    def genera_pianificazione(self):
        pianificazione = self.gestione.genera_pianificazione_settimanale()
        self.text_pianificazione.delete(1.0, tk.END)
        self.text_pianificazione.insert(tk.END, pianificazione)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestioneRistoranteApp(root)
    root.mainloop()
