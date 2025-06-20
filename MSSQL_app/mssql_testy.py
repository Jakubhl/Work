
import pyodbc
import hashlib  # nebo bcrypt pro lepší zabezpečení
import tkinter as tk
from tkinter import messagebox

# když už jsem připojenej na local účtu netřeba přihlašování
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=NTB0327\SQLEXPRESS;'
    r'DATABASE=Artikly_JHV_new;'  # název tvé databáze
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

def sort_products(list_given):
    """
    0 = description1
    1 = description2
    2 = description3
    3 = description3
    """
    def filter_lang(all_lang_desc,add_separator=False):
        if "cs_CZ@" not in all_lang_desc:
            return ""
        only_cz = all_lang_desc.split(";de_DE@")[0]
        only_cz = only_cz.replace("cs_CZ@","")
        only_cz = only_cz.rstrip(";")
        if add_separator:
            only_cz = " | " + only_cz

        return only_cz
    
    def find_list(data, search_list, ban_list, key_search="description", key_result="type"):
        result = []
        for item in data:
            value = str(item.get(key_search, "")).lower()

            if any(term.lower() in value for term in search_list) and not any(ban.lower() in value for ban in ban_list):
                entry = item.get(key_result)
                # print(item.get(key_search),item.get(key_result))
                # print(item.get(key_search))
                # print(item.get(key_result))
                entry = item
                if entry not in result:
                    result.append(entry)

        print("\n")
        return sorted(result, key=lambda x: x["type"])
    
    def get_accessories(database_list):
        whole_list = filtered_part_list
        
        for database in database_list:
            for items in database:
                # if items in acc_list:
                whole_list.pop(whole_list.index(items))
        # return whole_list
        return sorted(whole_list, key=lambda x: x["type"])



    
    filtered_part_list = []
    for products in list_given:
        # print(str(products[27]))
        # print(str(products),"\n")
        filtered_desc = filter_lang(str(products[0]))
        filtered_desc += filter_lang(str(products[1]),True)
        filtered_desc += filter_lang(str(products[2]),True)

        # print(filtered_desc,str(products[3]))
        part_type = str(products[3])
        part_obj = {
            "description": filtered_desc.replace("\n",""),
            "type": part_type
        }
        if part_obj not in filtered_part_list:
            filtered_part_list.append(part_obj)
    
    camera_list = find_list(filtered_part_list, ["kamera","kamerová"], ["kontrolér","modul"])
    # print(camera_list)
    controller_list = find_list(filtered_part_list, ["kontroler","kontrolér"], ["kabel"])
    # print(controller_list)
    optics_list = find_list(filtered_part_list, ["objekti"], ["přísluše","filtr","pro objektiv"])
    # print(optics_list)
    cable_list = find_list(filtered_part_list, ["kabel"], [])
    # print(cable_list)
    light_list = find_list(filtered_part_list, ["svět"], ["integr","kabel","filtr","kontrolér","senzor"])
    # print(light_list)

    acc_list = get_accessories([camera_list,controller_list,optics_list,cable_list,light_list])
    for acc in acc_list:
        # if acc["type"] == "":
        #     print("k")
        print(str(acc["type"]))
        # print(acc["type"],"               ",acc["description"])
        # print(str(acc["description"]))


    # camera_list = []
    # for products in filtered_part_list:
    #     if "kamera" in products["description"].lower() or "kamerová" in products["description"].lower():
    #         if products["type"] not in camera_list:
    #             camera_list.append(products["type"])
    #             # print(products)

    # print(sorted(camera_list))

    # controller_list = []
    # for products in filtered_part_list:
    #     if ("kontroler" in products["description"].lower() or "kontrolér" in products["description"].lower()) and not "kabel" in products["description"].lower():
    #         if products["type"] not in controller_list:
    #             controller_list.append(products["type"])
    #             # print(products)
    # print(sorted(controller_list))

    



def find_camera_products():
    cursor = conn.cursor()

    # SQL dotaz – hledáme záznamy, kde sloupec obsahuje určitý řetězec
    hledany_string = 'OMR'
    # hledany_string = 'KEY'
    hledany_string = 'COG'
    sql = """
    SELECT * FROM dbo.tblAccessoryList
    WHERE name LIKE ?
    """
    sql = """
    SELECT * FROM dbo.tblPart
    WHERE erpnr LIKE ?
    """

    sql = """
    SELECT description1, description2, description3, typenr
    FROM dbo.tblPart
    WHERE manufacturer LIKE ?
    """

    cursor.execute(sql, f"%{hledany_string}%")  # % pro LIKE
    found_products = []
    # Výpis výsledků
    for row in cursor.fetchall():
        # if row not in found_products:
        found_products.append(row)
        # print(row)
    
    # for products in found_products:
    #     print(products + "\n")
    sort_products(found_products)
    
    conn.close()

try:
    conn = pyodbc.connect(conn_str)
    print("Připojeno k databázi!")

    # read_column("STANICE","[525_SW_PNEU]")
    find_camera_products()

except Exception as e:
    print("Chyba při připojení:", e)

