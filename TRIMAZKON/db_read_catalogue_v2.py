

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
        - LEPŠÍ DĚLAT ROVNOU V SQL
        """
        ban_list.append("NEPOUŽÍVAT")
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
    def filter_part_list(cls,list_given):
        """
        list_given:
        - 0 = description1
        - 1 = description2
        - 2 = description3
        - 3 = typ součásti (typenr)
        - 4 = unikátní id
        """
        filtered_part_list = []
        for products in list_given:
            filtered_desc = Tools.filter_lang(str(products[0]))
            filtered_desc += Tools.filter_lang(str(products[1]),True)
            filtered_desc += Tools.filter_lang(str(products[2]),True)

            part_type = str(products[3])
            part_id = str(products[4])
            part_obj = {
                "description": filtered_desc.replace("\n",""),
                "type": part_type,
                "id": part_id
            }
            if part_obj not in filtered_part_list:
                filtered_part_list.append(part_obj)
        return filtered_part_list
    
    @classmethod
    def find_unknown(cls,conn,part):
        """
        hledá jestli není v ostré databázi
        """
        cursor = conn.cursor()
        sql = """
        SELECT description1, description2, description3, typenr, id
        FROM dbo.tblPart
        WHERE typenr LIKE ?
        """
        cursor.execute(sql, f"{part}")  # % pro LIKE
        found_products = []
        for row in cursor.fetchall():
            found_products.append(row)

        filtered_list = Tools.filter_part_list(found_products)

        if len(filtered_list) == 1:
            print(filtered_list)
            return "ok"
        elif len(filtered_list) == 0:
            return "ng"
        elif len(filtered_list) > 1:
            return filtered_list

def get_camera_products(list_given):
    """
    - světla jsou od různých výrobců, stejně tak i kabely
    """
    filtered_part_list = Tools.filter_part_list(list_given)
    
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


def find_camera_products_db(conn,manufacturer,not_initial = True):
    """
    manufacturer neovlivňuje:
    - filtry
    - kabely ke světlům\n
    Accessory jsou tvořeny tak, že od daného výrobce bere zbytek najitých produktů, které ještě nejsou přiřazeny
    """
    cursor = conn.cursor()
    sql = """
    SELECT description1, description2, description3, typenr, id
    FROM dbo.tblPart
    WHERE manufacturer LIKE ?
    """

    cursor.execute(sql, f"%{manufacturer}%")  # % pro LIKE
    found_products = []
    for row in cursor.fetchall():
        found_products.append(row)
    
    db_all_producs_sorted = get_camera_products(found_products)

    sql_get_lights = r"""
    SELECT description1, description2, description3, typenr, id
    FROM dbo.tblPart
    WHERE (
        description1 LIKE '%osv%'
        OR description1 LIKE '%low angle%'
        OR description1 LIKE '%light%'
    )
    AND description1 NOT LIKE '%curtain%'
    AND description1 NOT LIKE '%prosv%'
    AND description1 NOT LIKE '%kabel%'
    AND description1 NOT LIKE '%držák%'
    AND description1 NOT LIKE '%filtr%'
    AND description1 NOT LIKE '%signal%'
    AND description1 NOT LIKE '%signálk%'
    AND description1 NOT LIKE '%indic%'
    AND description1 NOT LIKE '%safety%'
    AND description1 NOT LIKE '%for light%'
    AND description1 NOT LIKE '%for ringlight%'
    AND description1 NOT LIKE '%sensor%'
    AND description1 NOT LIKE '%for LED%'
    AND description1 NOT LIKE '%integrov%'
    AND description1 NOT LIKE '%lightened%'
    AND description1 NOT LIKE '%lightning%'
    AND description1 NOT LIKE '%lightw%'
    AND description1 NOT LIKE '%kamen%'
    AND description1 NOT LIKE '%NEPOUŽÍVAT%'
    """
    cursor.execute(sql_get_lights)
    found_lights = []
    for row in cursor.fetchall():
        found_lights.append(row)

    filtered_part_list = Tools.filter_part_list(found_lights)
    # all_light_list = Tools.find_list(filtered_part_list, ["osv","svet","svět"], ["prosv","kabel","držák","filtr","světelný ","světle ","senzor","závěs","podsvět","modul","závora","integrované"])
    combined = db_all_producs_sorted["light_list"] + filtered_part_list
    db_all_producs_sorted["light_list"] = sorted(combined, key=lambda x: x["type"])
    # db_all_producs_sorted["light_list"] = sorted(filtered_part_list, key=lambda x: x["type"])
    # db_all_producs_sorted["all_lights_list"] = filtered_part_list

    if not_initial:
        return db_all_producs_sorted
    
    sql_get_filters = r"""
    SELECT description1, description2, description3, typenr, id
    FROM dbo.tblPart
    WHERE (
        description1 LIKE '%Polarizing%'
        OR description1 LIKE '%Lens prote%'
        OR description1 LIKE '%extension ri%'
    )
    AND description1 NOT LIKE '%závora%'
    AND description1 NOT LIKE '%NEPOUŽÍVAT%'

    """
    cursor.execute(sql_get_filters)
    found_filters = []
    for row in cursor.fetchall():
        found_filters.append(row)
    filtered_part_list = Tools.filter_part_list(found_filters)
    db_all_producs_sorted["filter_list"] = sorted(filtered_part_list, key=lambda x: x["type"])


    sql_get_cables = r"""
    SELECT description1, description2, description3, typenr, id, manufacturer
    FROM dbo.tblPart
    WHERE (
        description1 LIKE '%reader cabl%'
        OR description1 LIKE '%camera cable%'
        OR description1 LIKE '%cable for camera%'
        OR description1 LIKE '%light cable%'
        OR description1 LIKE '%cable for light%'
        OR description1 LIKE '%kabel pro osv%'
        OR description1 LIKE '%přívodní kabel%'
        OR description1 LIKE '%kabel pro LED%'
        OR (description1 LIKE '%kabel s konekto%' AND manufacturer LIKE '%BAL%')
    )
    AND description1 NOT LIKE '%NEPOUŽÍVAT%'
    AND description1 NOT LIKE '%curtain%'
    """
    cursor.execute(sql_get_cables)
    found_cables = []
    for row in cursor.fetchall():
        found_cables.append(row)
    filtered_part_list = Tools.filter_part_list(found_cables)
    db_all_producs_sorted["light_cable_list"] = sorted(filtered_part_list, key=lambda x: x["type"])
    
    
    return db_all_producs_sorted


#TESTING------------------------------------------------------------------------------
# import pyodbc
# try:
#     conn = pyodbc.connect(conn_str)
#     print("Připojeno k databázi!")

#     # read_column("STANICE","[525_SW_PNEU]")
#     output = find_camera_products_db(conn,"OMR")
#     # print(output["light_list"])
#     # print(output["filter_list"])
#     # print(output["light_cable_list"])
#     conn.close()

# except Exception as e:
#     print("Chyba při připojení:", e)

