import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import sqlite3

def otevri_databazi():
    global soubor
    soubor = filedialog.askopenfilename(filetypes=[("SQLite databáze", "*.db *.sqlite")])
    if soubor:
        try:
            conn = sqlite3.connect(soubor)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tabulky = [row[0] for row in cursor.fetchall()]
            conn.close()

            if not tabulky:
                messagebox.showinfo("Info", "Databáze neobsahuje žádné tabulky.")
                return

            combo_tabulek['values'] = tabulky
            combo_tabulek.current(0)
            vyber_a_nacti_tab()
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst databázi:\n{e}")

def vyber_a_nacti_tab(*args):
    nazev_tab = combo_tabulek.get()
    if not nazev_tab:
        return

    try:
        conn = sqlite3.connect(soubor)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {nazev_tab}")
        zaznamy = cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({nazev_tab})")
        sloupce = [s[1] for s in cursor.fetchall()]
        conn.close()

        for widget in frame_tabulka.winfo_children():
            widget.destroy()

        # Nadpisy
        for j, nazev in enumerate(sloupce):
            label = tk.Label(frame_tabulka, text=nazev, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", padx=4, pady=2)
            label.grid(row=0, column=j, sticky="nsew")

        # Data
        for i, radek in enumerate(zaznamy, start=1):
            for j, hodnota in enumerate(radek):
                label = tk.Label(frame_tabulka, text=str(hodnota), borderwidth=1, relief="solid", padx=4, pady=2)
                label.grid(row=i, column=j, sticky="nsew")

    except Exception as e:
        messagebox.showerror("Chyba", f"Nepodařilo se načíst tabulku:\n{e}")

# GUI
okno = tk.Tk()
okno.title("Univerzální SQLite prohlížeč")

frame_ovladani = tk.Frame(okno)
frame_ovladani.pack(pady=10)

btn_otevrit = tk.Button(frame_ovladani, text="Otevřít databázi", command=otevri_databazi)
btn_otevrit.pack(side=tk.LEFT, padx=5)

combo_tabulek = ttk.Combobox(frame_ovladani, state="readonly")
combo_tabulek.pack(side=tk.LEFT, padx=5)
combo_tabulek.bind("<<ComboboxSelected>>", vyber_a_nacti_tab)

frame_tabulka = tk.Frame(okno)
frame_tabulka.pack(padx=10, pady=10)

soubor = ""  # proměnná mimo funkce pro uchování cesty

okno.mainloop()
