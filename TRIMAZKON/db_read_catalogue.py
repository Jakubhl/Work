
import pyodbc

conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=NTB0327\SQLEXPRESS;'
    r'DATABASE=Artikly_JHV_new;'  # název tvé databáze
    r'Trusted_Connection=yes;'  # nebo místo toho použij UID/PWD pro SQL autentizaci
)


# def call_store_procedure():
#     # Volání uložené procedury s parametry
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             EXEC version_0_1_0.update_from_creo_table @ProjectId = ?, @AuthorId = ?
#         """, '525', '1111')

#         conn.commit()  # pokud procedura něco zapisuje

#         # for row in cursor.fetchall():
#         #     print(row)  # nebo: print(row.sloupec)

#         print("Procedura úspěšně vykonána")
#     except Exception as e:
#         print("Chyba:", e)
#     finally:
#         conn.close()

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
        """
        - hledá podle search_list převedené na lower
        - a nebere nic co má v ban_list
        """
        result = []
        for item in data:
            value = str(item.get(key_search, "")).lower()

            if any(term.lower() in value for term in search_list) and not any(ban.lower() in value for ban in ban_list):
                entry = item.get(key_result)
                entry = item
                if entry not in result:
                    result.append(entry)
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
        filtered_desc = filter_lang(str(products[0]))
        filtered_desc += filter_lang(str(products[1]),True)
        filtered_desc += filter_lang(str(products[2]),True)

        part_type = str(products[3])
        part_obj = {
            "description": filtered_desc.replace("\n",""),
            "type": part_type
        }
        if part_obj not in filtered_part_list:
            filtered_part_list.append(part_obj)
    
    camera_list = find_list(filtered_part_list, ["kamera","kamerová","camera"], ["kontrolér","modul"])
    # print(camera_list)
    controller_list = find_list(filtered_part_list, ["kontroler","kontrolér","controller","controllers"], ["kabel"])
    # print(controller_list)
    optics_list = find_list(filtered_part_list, ["objekti"], ["přísluše","filtr","pro objektiv"])
    # print(optics_list)
    cable_list = find_list(filtered_part_list, ["kabel"], [])
    # print(cable_list)
    light_list = find_list(filtered_part_list, ["svět"], ["integr","kabel","filtr","kontrolér","senzor"])
    # print(light_list)

    acc_list = get_accessories([camera_list,controller_list,optics_list,cable_list,light_list])
    # for acc in acc_list:
    #     print(str(acc["type"]))

    db_all_producs_sorted = {
        "camera_list":camera_list,
        "controller_list":controller_list,
        "optics_list":optics_list,
        "cable_list":cable_list,
        "light_list":light_list,
        "acc_list":acc_list
    }
    return db_all_producs_sorted


def find_camera_products_db(conn,manufacturer):
    cursor = conn.cursor()

    sql = """
    SELECT description1, description2, description3, typenr
    FROM dbo.tblPart
    WHERE manufacturer LIKE ?
    """

    cursor.execute(sql, f"%{manufacturer}%")  # % pro LIKE
    found_products = []
    for row in cursor.fetchall():
        found_products.append(row)
    
    db_all_producs_sorted = sort_products(found_products)
    return db_all_producs_sorted
    
    # conn.close()

# try:
#     conn = pyodbc.connect(conn_str)
#     print("Připojeno k databázi!")

#     # read_column("STANICE","[525_SW_PNEU]")
#     find_camera_products_db(conn,"OMR")

# except Exception as e:
#     print("Chyba při připojení:", e)

