
import pyodbc
import hashlib  # nebo bcrypt pro lepší zabezpečení
import tkinter as tk
from tkinter import messagebox

# když už jsem připojenej na local účtu netřeba přihlašování
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=NTB0327\SQLEXPRESS;'
    r'DATABASE=JHV_CM;'  # název tvé databáze
    r'Trusted_Connection=yes;'  # nebo místo toho použij UID/PWD pro SQL autentizaci
)


def read_column(column_name, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT {column_name} FROM {table_name}")
    for row in cursor.fetchall():
        # print(row[0])
        print(row)
    print(len(row[0]))


def check_login(username, password):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=NTB0327\SQLEXPRESS;'
        r'DATABASE=JHV_CM;'  # název tvé databáze
        rf"UID={username};"
        rf"PWD={password};"
        r'Trusted_Connection=no;'
    )
    try:
        conn = pyodbc.connect(conn_str)
    except Exception as e:
        print("Chyba při připojení:", e)
        return False

    cursor = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    # try:
    # cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", username, hashed)
    cursor.execute("SELECT FUNKCNI_TEXT FROM [525_SW_PNEU]")
    for row in cursor.fetchall():
        print(row[0])  # Nebo: print(row[0])
    print(len(cursor.fetchall()))
    return True
    # except Exception:
    #     print("špatný název tabulky")
    #     return False
    # row = cursor.fetchone()
    
    # if row:
    #     return True
    # else:
    #     return False
    
# check_login("sa","2708")
# k = input("kk?")

def login():
    user = username_entry.get()
    pwd = password_entry.get()
    
    if check_login(user, pwd):
    # if check_login("user", "pwd"):
        messagebox.showinfo("Úspěch", "Přihlášení proběhlo úspěšně!")
    else:
        messagebox.showerror("Chyba", "Špatné jméno nebo heslo.")

# login()
# root = tk.Tk()
# tk.Label(root, text="Uživatel:").pack()
# username_entry = tk.Entry(root)
# username_entry.pack()
# tk.Label(root, text="Heslo:").pack()
# password_entry = tk.Entry(root, show="*")
# password_entry.pack()
# tk.Button(root, text="Přihlásit", command=login).pack()
# root.mainloop()

def call_store_procedure():
    # Volání uložené procedury s parametry
    cursor = conn.cursor()
    try:
        cursor.execute("""
            EXEC version_0_1_0.update_from_creo_table @ProjectId = ?, @AuthorId = ?
        """, '525', '1111')

        conn.commit()  # pokud procedura něco zapisuje

        # for row in cursor.fetchall():
        #     print(row)  # nebo: print(row.sloupec)

        print("Procedura úspěšně vykonána")
    except Exception as e:
        print("Chyba:", e)
    finally:
        conn.close()

try:
    conn = pyodbc.connect(conn_str)
    print("Připojeno k databázi!")

    # read_column("STANICE","[525_SW_PNEU]")
    call_store_procedure()

except Exception as e:
    print("Chyba při připojení:", e)