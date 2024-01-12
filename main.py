import tkinter as tk
from tkinter import ttk
import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS socio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                cognome TEXT,
                indirizzo TEXT,
                numeroTesseraSocio INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prestito (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataPrestito DATE,
                dataRestituzione DATE,
                dataScadenza DATE,
                idCopia INTEGER,
                numeroRinnoviCopia INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS copia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numeroCopia INTEGER,
                disponibilita BOOLEAN,
                condizioni TEXT,
                idLibro INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS libro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT,
                titolo TEXT,
                autore TEXT,
                editore TEXT,
                annoPubblicazione INTEGER,
                parolaChiave TEXT,
                scaffale TEXT,
                piano TEXT,
                sezione TEXT,
                posizione TEXT
            )
        ''')

        self.conn.commit()

    def insert_socio(self, nome, cognome, indirizzo, numero_tessera):
        self.cursor.execute('''
            INSERT INTO socio (nome, cognome, indirizzo, numeroTesseraSocio)
            VALUES (?, ?, ?, ?)
        ''', (nome, cognome, indirizzo, numero_tessera))
        self.conn.commit()

    # Aggiungi altri metodi per inserire dati nelle tabelle prestito, copia, libro, ecc.

    def get_soci(self):
        self.cursor.execute('SELECT * FROM socio')
        return self.cursor.fetchall()

    # Aggiungi altri metodi per ottenere dati dalle altre tabelle.


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Database")
        self.sociobutt = ttk.Button(root, text="Aggiungi Socio", command=self.add_socio)

    def soci(self):
        x = SocioWindow(self.root)



class SocioWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Database")

        self.db_manager = DatabaseManager("database.db")

        self.nome_label = ttk.Label(root, text="Nome:")
        self.nome_entry = ttk.Entry(root)

        self.cognome_label = ttk.Label(root, text="Cognome:")
        self.cognome_entry = ttk.Entry(root)

        self.indirizzo_label = ttk.Label(root, text="Indirizzo:")
        self.indirizzo_entry = ttk.Entry(root)

        self.numero_tessera_label = ttk.Label(root, text="Numero Tessera:")
        self.numero_tessera_entry = ttk.Entry(root)

        self.add_socio_button = ttk.Button(root, text="Aggiungi Socio", command=self.add_socio)

        self.tree = ttk.Treeview(root, columns=("ID", "Nome", "Cognome", "Indirizzo", "Numero Tessera"),
                                 show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Cognome", text="Cognome")
        self.tree.heading("Indirizzo", text="Indirizzo")
        self.tree.heading("Numero Tessera", text="Numero Tessera")

        self.refresh_tree()

        self.nome_label.grid(row=0, column=0, sticky="W", padx=10, pady=5)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)
        self.cognome_label.grid(row=1, column=0, sticky="W", padx=10, pady=5)
        self.cognome_entry.grid(row=1, column=1, padx=10, pady=5)
        self.indirizzo_label.grid(row=2, column=0, sticky="W", padx=10, pady=5)
        self.indirizzo_entry.grid(row=2, column=1, padx=10, pady=5)
        self.numero_tessera_label.grid(row=3, column=0, sticky="W", padx=10, pady=5)
        self.numero_tessera_entry.grid(row=3, column=1, padx=10, pady=5)
        self.add_socio_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def add_socio(self):
        nome = self.nome_entry.get()
        cognome = self.cognome_entry.get()
        indirizzo = self.indirizzo_entry.get()
        numero_tessera = self.numero_tessera_entry.get()

        if nome and cognome and indirizzo and numero_tessera:
            self.db_manager.insert_socio(nome, cognome, indirizzo, numero_tessera)
            self.refresh_tree()
            self.nome_entry.delete(0, "end")
            self.cognome_entry.delete(0, "end")
            self.indirizzo_entry.delete(0, "end")
            self.numero_tessera_entry.delete(0, "end")

    def refresh_tree(self):
        soci = self.db_manager.get_soci()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for socio in soci:
            self.tree.insert("", "end", values=socio)


if __name__ == "__main__":
    root = tk.Tk()
    app = SocioWindow(root)
    root.mainloop()