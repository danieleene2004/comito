import tkinter as tk
from datetime import datetime
from tkinter import ttk
import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    def insert_libro(self, isbn, titolo, autore, editore, anno_pubblicazione,
                     parola_chiave, scaffale, piano, sezione, posizione):
        self.cursor.execute('''
            INSERT INTO libro (isbn, titolo, autore, editore, annoPubblicazione,
                               parolaChiave, scaffale, piano, sezione, posizione)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (isbn, titolo, autore, editore, anno_pubblicazione,
              parola_chiave, scaffale, piano, sezione, posizione))
        self.conn.commit()

    def get_libri(self):
        self.cursor.execute('SELECT * FROM libro')
        return self.cursor.fetchall()

    def insert_copia(self, numero_copia, disponibilita, condizioni, id_libro):
        self.cursor.execute('''
            INSERT INTO copia (numeroCopia, disponibilita, condizioni, idLibro)
            VALUES (?, ?, ?, ?)
        ''', (numero_copia, disponibilita, condizioni, id_libro))
        self.conn.commit()

    def get_copie(self):
        self.cursor.execute('SELECT * FROM copia')
        return self.cursor.fetchall()
    def insert_prestito(self, data_prestito, data_restituzione, id_copia, numero_rinnovi):
        self.cursor.execute('''
            INSERT INTO prestito (dataPrestito, dataRestituzione, idCopia, numeroRinnoviCopia)
            VALUES (?, ?, ?, ?)
        ''', (data_prestito, data_restituzione, id_copia, numero_rinnovi))
        self.conn.commit()

    def get_prestiti(self):
        self.cursor.execute('SELECT * FROM prestito')
        return self.cursor.fetchall()

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
        self.sociobutt = ttk.Button(root, text="Soci", command=self.soci).grid(row=0, column=0, sticky="W", padx=10, pady=5)
        self.prestibutt = ttk.Button(root, text="Prestito", command=self.presti).grid(row=1, column=0, sticky="W", padx=10, pady=5)
        self.copiabutt = ttk.Button(root, text="Copia", command=self.copia).grid(row=2, column=0, sticky="W", padx=10, pady=5)
        self.librobutt = ttk.Button(root, text="Libro", command=self.libro).grid(row=3, column=0, sticky="W", padx=10, pady=5)

    def soci(self):
        x = SocioWindow(self.root)
    def presti(self):
        x = PrestitoWindow(self.root)
    def copia(self):
        x = CopiaWindow(self.root)
    def libro(self):
        x = LibroWindow(self.root)



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

class PrestitoWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Prestiti")

        self.db_manager = DatabaseManager("database.db")

        self.data_prestito_label = ttk.Label(root, text="Data Prestito (YYYY-MM-DD):")
        self.data_prestito_entry = ttk.Entry(root)

        self.data_restituzione_label = ttk.Label(root, text="Data Restituzione (YYYY-MM-DD):")
        self.data_restituzione_entry = ttk.Entry(root)

        self.id_copia_label = ttk.Label(root, text="ID Copia:")
        self.id_copia_entry = ttk.Entry(root)

        self.numero_rinnovi_label = ttk.Label(root, text="Numero Rinnovi:")
        self.numero_rinnovi_entry = ttk.Entry(root)

        self.add_prestito_button = ttk.Button(root, text="Aggiungi Prestito", command=self.add_prestito)

        self.tree = ttk.Treeview(root,
                                 columns=("ID", "Data Prestito", "Data Restituzione", "ID Copia", "Numero Rinnovi"),
                                 show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Data Prestito", text="Data Prestito")
        self.tree.heading("Data Restituzione", text="Data Restituzione")
        self.tree.heading("ID Copia", text="ID Copia")
        self.tree.heading("Numero Rinnovi", text="Numero Rinnovi")

        self.refresh_tree()

        self.data_prestito_label.grid(row=0, column=0, sticky="W", padx=10, pady=5)
        self.data_prestito_entry.grid(row=0, column=1, padx=10, pady=5)
        self.data_restituzione_label.grid(row=1, column=0, sticky="W", padx=10, pady=5)
        self.data_restituzione_entry.grid(row=1, column=1, padx=10, pady=5)
        self.id_copia_label.grid(row=2, column=0, sticky="W", padx=10, pady=5)
        self.id_copia_entry.grid(row=2, column=1, padx=10, pady=5)
        self.numero_rinnovi_label.grid(row=3, column=0, sticky="W", padx=10, pady=5)
        self.numero_rinnovi_entry.grid(row=3, column=1, padx=10, pady=5)
        self.add_prestito_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def add_prestito(self):
        data_prestito_str = self.data_prestito_entry.get()
        data_restituzione_str = self.data_restituzione_entry.get()
        id_copia = self.id_copia_entry.get()
        numero_rinnovi = self.numero_rinnovi_entry.get()

        try:
            data_prestito = datetime.strptime(data_prestito_str, "%Y-%m-%d")
            data_restituzione = datetime.strptime(data_restituzione_str, "%Y-%m-%d") if data_restituzione_str else None
            id_copia = int(id_copia)
            numero_rinnovi = int(numero_rinnovi) if numero_rinnovi else 0

            self.db_manager.insert_prestito(data_prestito, data_restituzione, id_copia, numero_rinnovi)
            self.refresh_tree()
            self.data_prestito_entry.delete(0, "end")
            self.data_restituzione_entry.delete(0, "end")
            self.id_copia_entry.delete(0, "end")
            self.numero_rinnovi_entry.delete(0, "end")
        except ValueError as e:
            tk.messagebox.showerror("Errore", f"Errore durante la conversione dei dati: {e}")

    def refresh_tree(self):
        prestiti = self.db_manager.get_prestiti()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for prestito in prestiti:
            self.tree.insert("", "end", values=prestito)

class CopiaWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Copie")

        self.db_manager = DatabaseManager("database.db")

        self.numero_copia_label = ttk.Label(root, text="Numero Copia:")
        self.numero_copia_entry = ttk.Entry(root)

        self.disponibilita_label = ttk.Label(root, text="Disponibilità:")
        self.disponibilita_entry = ttk.Entry(root)

        self.condizioni_label = ttk.Label(root, text="Condizioni:")
        self.condizioni_entry = ttk.Entry(root)

        self.id_libro_label = ttk.Label(root, text="ID Libro:")
        self.id_libro_entry = ttk.Entry(root)

        self.add_copia_button = ttk.Button(root, text="Aggiungi Copia", command=self.add_copia)

        self.tree = ttk.Treeview(root, columns=("ID", "Numero Copia", "Disponibilità", "Condizioni", "ID Libro"),
                                 show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Numero Copia", text="Numero Copia")
        self.tree.heading("Disponibilità", text="Disponibilità")
        self.tree.heading("Condizioni", text="Condizioni")
        self.tree.heading("ID Libro", text="ID Libro")

        self.refresh_tree()

        self.numero_copia_label.grid(row=0, column=0, sticky="W", padx=10, pady=5)
        self.numero_copia_entry.grid(row=0, column=1, padx=10, pady=5)
        self.disponibilita_label.grid(row=1, column=0, sticky="W", padx=10, pady=5)
        self.disponibilita_entry.grid(row=1, column=1, padx=10, pady=5)
        self.condizioni_label.grid(row=2, column=0, sticky="W", padx=10, pady=5)
        self.condizioni_entry.grid(row=2, column=1, padx=10, pady=5)
        self.id_libro_label.grid(row=3, column=0, sticky="W", padx=10, pady=5)
        self.id_libro_entry.grid(row=3, column=1, padx=10, pady=5)
        self.add_copia_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def add_copia(self):
        numero_copia = self.numero_copia_entry.get()
        disponibilita = self.disponibilita_entry.get()
        condizioni = self.condizioni_entry.get()
        id_libro = self.id_libro_entry.get()

        try:
            numero_copia = int(numero_copia)
            disponibilita = bool(disponibilita.lower() == "true")
            id_libro = int(id_libro)

            self.db_manager.insert_copia(numero_copia, disponibilita, condizioni, id_libro)
            self.refresh_tree()
            self.numero_copia_entry.delete(0, "end")
            self.disponibilita_entry.delete(0, "end")
            self.condizioni_entry.delete(0, "end")
            self.id_libro_entry.delete(0, "end")
        except ValueError as e:
            tk.messagebox.showerror("Errore", f"Errore durante la conversione dei dati: {e}")

    def refresh_tree(self):
        copie = self.db_manager.get_copie()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for copia in copie:
            self.tree.insert("", "end", values=copia)

class LibroWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Libri")

        self.db_manager = DatabaseManager("database.db")

        self.isbn_label = ttk.Label(root, text="ISBN:")
        self.isbn_entry = ttk.Entry(root)

        self.titolo_label = ttk.Label(root, text="Titolo:")
        self.titolo_entry = ttk.Entry(root)

        self.autore_label = ttk.Label(root, text="Autore:")
        self.autore_entry = ttk.Entry(root)

        self.editore_label = ttk.Label(root, text="Editore:")
        self.editore_entry = ttk.Entry(root)

        self.anno_pubblicazione_label = ttk.Label(root, text="Anno Pubblicazione:")
        self.anno_pubblicazione_entry = ttk.Entry(root)

        self.parola_chiave_label = ttk.Label(root, text="Parola Chiave:")
        self.parola_chiave_entry = ttk.Entry(root)

        self.scaffale_label = ttk.Label(root, text="Scaffale:")
        self.scaffale_entry = ttk.Entry(root)

        self.piano_label = ttk.Label(root, text="Piano:")
        self.piano_entry = ttk.Entry(root)

        self.sezione_label = ttk.Label(root, text="Sezione:")
        self.sezione_entry = ttk.Entry(root)

        self.posizione_label = ttk.Label(root, text="Posizione:")
        self.posizione_entry = ttk.Entry(root)

        self.add_libro_button = ttk.Button(root, text="Aggiungi Libro", command=self.add_libro)

        self.tree = ttk.Treeview(root, columns=(
        "ID", "ISBN", "Titolo", "Autore", "Editore", "Anno Pubblicazione", "Parola Chiave", "Scaffale", "Piano",
        "Sezione", "Posizione"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Titolo", text="Titolo")
        self.tree.heading("Autore", text="Autore")
        self.tree.heading("Editore", text="Editore")
        self.tree.heading("Anno Pubblicazione", text="Anno Pubblicazione")
        self.tree.heading("Parola Chiave", text="Parola Chiave")
        self.tree.heading("Scaffale", text="Scaffale")
        self.tree.heading("Piano", text="Piano")
        self.tree.heading("Sezione", text="Sezione")
        self.tree.heading("Posizione", text="Posizione")

        self.refresh_tree()

        self.isbn_label.grid(row=0, column=0, sticky="W", padx=10, pady=5)
        self.isbn_entry.grid(row=0, column=1, padx=10, pady=5)
        self.titolo_label.grid(row=1, column=0, sticky="W", padx=10, pady=5)
        self.titolo_entry.grid(row=1, column=1, padx=10, pady=5)
        self.autore_label.grid(row=2, column=0, sticky="W", padx=10, pady=5)
        self.autore_entry.grid(row=2, column=1, padx=10, pady=5)
        self.editore_label.grid(row=3, column=0, sticky="W", padx=10, pady=5)
        self.editore_entry.grid(row=3, column=1, padx=10, pady=5)
        self.anno_pubblicazione_label.grid(row=4, column=0, sticky="W", padx=10, pady=5)
        self.anno_pubblicazione_entry.grid(row=4, column=1, padx=10, pady=5)
        self.parola_chiave_label.grid(row=5, column=0, sticky="W", padx=10, pady=5)
        self.parola_chiave_entry.grid(row=5, column=1, padx=10, pady=5)
        self.scaffale_label.grid(row=6, column=0, sticky="W", padx=10, pady=5)
        self.scaffale_entry.grid(row=6, column=1, padx=10, pady=5)
        self.piano_label.grid(row=7, column=0, sticky="W", padx=10, pady=5)
        self.piano_entry.grid(row=7, column=1, padx=10, pady=5)
        self.sezione_label.grid(row=8, column=0, sticky="W", padx=10, pady=5)
        self.sezione_entry.grid(row=8, column=1, padx=10, pady=5)
        self.posizione_label.grid(row=9, column=0, sticky="W", padx=10, pady=5)
        self.posizione_entry.grid(row=9, column=1, padx=10, pady=5)
        self.add_libro_button.grid(row=10, column=0, columnspan=2, pady=10)
        self.tree.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

    def add_libro(self):
        isbn = self.isbn_entry.get()
        titolo = self.titolo_entry.get()
        autore = self.autore_entry.get()
        editore = self.editore_entry.get()
        anno_pubblicazione = self.anno_pubblicazione_entry.get()
        parola_chiave = self.parola_chiave_entry.get()
        scaffale = self.scaffale_entry.get()
        piano = self.piano_entry.get()
        sezione = self.sezione_entry.get()
        posizione = self.posizione_entry.get()

        try:
            anno_pubblicazione = int(anno_pubblicazione)

            self.db_manager.insert_libro(isbn, titolo, autore, editore, anno_pubblicazione,
                                         parola_chiave, scaffale, piano, sezione, posizione)
            self.refresh_tree()
            self.isbn_entry.delete(0, "end")
            self.titolo_entry.delete(0, "end")
            self.autore_entry.delete(0, "end")
            self.editore_entry.delete(0, "end")
            self.anno_pubblicazione_entry.delete(0, "end")
            self.parola_chiave_entry.delete(0, "end")
            self.scaffale_entry.delete(0, "end")
            self.piano_entry.delete(0, "end")
            self.sezione_entry.delete(0, "end")
            self.posizione_entry.delete(0, "end")
        except ValueError as e:
            tk.messagebox.showerror("Errore", f"Errore durante la conversione dei dati: {e}")

    def refresh_tree(self):
        libri = self.db_manager.get_libri()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for libro in libri:
            self.tree.insert("", "end", values=libro)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()