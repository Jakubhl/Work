
import pyodbc

conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=NTB0327\SQLEXPRESS;'
    r'DATABASE=Artikly_JHV_new;'  # název tvé databáze
    r'Trusted_Connection=yes;'  # nebo místo toho použij UID/PWD pro SQL autentizaci
)


class Tools:
    @classmethod
    def filter_lang(cls,all_lang_desc,add_separator=False):
        if "cs_CZ@" not in all_lang_desc:
            return ""
        only_cz = all_lang_desc.split(";de_DE@")[0]
        only_cz = only_cz.replace("cs_CZ@","")
        only_cz = only_cz.rstrip(";")
        if add_separator:
            only_cz = " | " + only_cz

        return only_cz
    
    @classmethod
    def find_list(cls,data, search_list, ban_list, key_search="description", key_result="type"):
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
    
    @classmethod
    def filer_part_list(cls,list_given):
        """
        list_given:
        - 0 = description1
        - 1 = description2
        - 2 = description3
        - 3 = typ součásti (typenr)
        """
        filtered_part_list = []
        for products in list_given:
            filtered_desc = Tools.filter_lang(str(products[0]))
            filtered_desc += Tools.filter_lang(str(products[1]),True)
            filtered_desc += Tools.filter_lang(str(products[2]),True)

            part_type = str(products[3])
            part_obj = {
                "description": filtered_desc.replace("\n",""),
                "type": part_type
            }
            if part_obj not in filtered_part_list:
                filtered_part_list.append(part_obj)
        return filtered_part_list


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


def get_camera_products(list_given):
    """
    - světla jsou od různých výrobců, stejně tak i kabely
    """
    filtered_part_list = Tools.filer_part_list(list_given)
    
    def get_accessories(database_list):
        whole_list = filtered_part_list
        
        for database in database_list:
            for items in database:
                # if items in acc_list:
                whole_list.pop(whole_list.index(items))
        # return whole_list
        return sorted(whole_list, key=lambda x: x["type"])
    
    
    camera_list = Tools.find_list(filtered_part_list, ["kamera","kamerová","camera"], ["kontrolér","modul"])
    # print(camera_list)
    controller_list = Tools.find_list(filtered_part_list, ["kontroler","kontrolér","controller","controllers"], ["kabel"])
    # print(controller_list)
    optics_list = Tools.find_list(filtered_part_list, ["objekti"], ["přísluše","filtr","pro o"])
    # print(optics_list)
    cable_list = Tools.find_list(filtered_part_list, ["kabel"], [])
    # print(cable_list)
    light_list = Tools.find_list(filtered_part_list, ["svět","osv"], ["integr","kabel","filtr","kontrolér","senzor"])
    # print(light_list)

    acc_list = get_accessories([camera_list,controller_list,optics_list,cable_list,light_list])
    # for acc in acc_list:
    #     print(str(acc["type"]))

    db_all_producs_sorted = {
        "camera_list":sorted(camera_list, key=lambda x: x["type"]),
        "controller_list":sorted(controller_list, key=lambda x: x["type"]),
        "optics_list":sorted(optics_list, key=lambda x: x["type"]),
        "cable_list":sorted(cable_list, key=lambda x: x["type"]),
        "light_list":sorted(light_list, key=lambda x: x["type"]),
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
    
    db_all_producs_sorted = get_camera_products(found_products)

    sql2 = """
    SELECT description1, description2, description3, typenr
    FROM dbo.tblPart
    WHERE description1 LIKE ?
    OR description1 LIKE ?
    OR description1 LIKE ?
    """
    cursor.execute(sql2, (r'%osv%', r'%svet%', r'%svět%'))

    found_lights = []
    for row in cursor.fetchall():
        found_lights.append(row)
        print(found_lights)

    filtered_part_list = Tools.filer_part_list(found_lights)
    all_light_list = Tools.find_list(filtered_part_list, ["osv","svet","svět"], ["prosv","kabel","držák","filtr","světelný ","světle ","senzor","závěs","podsvět","modul","závora","integrované"])
    combined = db_all_producs_sorted["light_list"] + all_light_list
    db_all_producs_sorted["light_list"] = sorted(combined, key=lambda x: x["type"])


    return db_all_producs_sorted
    
    # conn.close()

# try:
#     conn = pyodbc.connect(conn_str)
#     print("Připojeno k databázi!")

#     # read_column("STANICE","[525_SW_PNEU]")
#     find_camera_products_db(conn,"OMR")

# except Exception as e:
#     print("Chyba při připojení:", e)

