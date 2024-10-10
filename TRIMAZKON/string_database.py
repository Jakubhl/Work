change_log_list = [" Verze 3.4 (3.3.2024)",
    """ 
    - velikost písma
    - načítací animace
    - nové konzole (převedeno na thread "real time")
    - image browser - jména souborů (zkopírovatelná)
    - chybové hlášky při procházení subfolderů
    - pokročilá nastavení - nová vizualizace + nový způsob nabídky\n"""
        ," Verze 3.5 (22.4.2024)"
        ,
    """ 
    - film obrázků před a po + bind přepínání kolečkem
    - možnost procházet obrázky ve formátu .ifz
    - třídění podle ID - úprava popisu
    - oprava zoomování obrázku
    - nové možnosti v pokročilých možnostech
    - oprava chyb se soubory s mezerou v názvu
    - možnost nastavit trimazkon, jako výchozí prohlížeč obrázků\n"""
        ," Verze 3.6.0 (5.6.2024)"
        ,
    """ 
    - Nové možnosti změny IP a mountění disků (import ver.3.7)
    - okno s informacemi o aktualizacích v menu
    - nová vizualizace u pokročilých nastavení (okno se záložkami)
    - tlačítka nastavení ve všech oknech programu\n"""
        ," Verze 3.6.1 (17.6.2024)"
        ,
    """ 
    - Zadávání při vkládání nového síťového disku již nevyžaduje
    jméno a heslo
    - Ošetření spouštění IP setting s otevřeným excelem se
    vstupními daty
    - Opraveno čtení statických IP adres (četla se vždy, pro daný
    inteface, automaticky nastavená místo privátní adresy)
    - Aplikace již k sobě nevyžaduje přikládat složku images
    - Bind klávesy F5 pro reset (refresh)
    - Nové, přesné chybové hlášky + nepřekrývají okna cmd a pws
    - Vizualizace již přiřazených ip adres\n"""
        ," Verze 3.6.2 (19.6.2024)"
        ,
    """ 
    - Oprava chyb s aut. plněním interfaců
    - dotaz o admin práva, když je vyžadováno
    - chybová hláška při mazání používaného síť. disku
    - po namapování otevře explorer v novém disku
    - zobrazování připojených interfaců\n"""
        ," Verze 3.7.0 (20.6.2024)"
        ,
    """ 
    - Plně funkční nastavování ip adres a mounting disků
    - nová vizualizace hlavního menu
    - rozklik poznámek převeden na hover
    - odebrány možnosti přídávání/ odebírání interfaců
    - možnost refresh online připojení
    - refresh disků na tlačítko\n"""
        ," Verze 3.7.1 (24.6.2024)"
        ,
    """ 
    - Nově lze poznámky v ip setting upravovat přímo 
    - Možnosti nastavení základního chování u disků
    - Změny v excelu: list-Setting, buňka-B6 (automaticky se zapíše)\n"""
        ," Verze 3.7.2 (1.7.2024)"
        ,
    """ 
    - Oprava padání aplikace při přechodu na admina
    - Vyskakovací okno cmd odstaněno (při změně ip)
    - Oprava duplikovaných jmen
    - Oprava vypisování seznamu online interfaců
    - Nově lze pro daný interface nastavit DHCP
    - Možnost volby u poznámek - editovatelné/ needitovatelné
    - Předčasné zjištění úspěšné změny ip adresy
    - Sloníci odebráni
    - Oprava aktualizace současně nastavených adres
    - Namapované disky persistentní (zůstanou po restartu)
    - Oprava kontroly připojených disků\n"""
        ," Verze 3.7.3 (11.7.2024)"
        ,
    """ 
    - Ošetření nastavování DHCP chyb. hláškami
    - Možnost v nastavení u ip_setting změnit způsob mapování disků
    - Po aplikování změn v okně nastavení se okno shodí
    - Přidání funkce pro vytváření katalogů\n"""
        ," Verze 3.7.4 (1.8.2024)"
        ,
    """ 
    Katalog:
    - Nová logika stromové struktury u vytváření katalogů
    - aut. zavírání ponechaných oken
    - oprava ukazatelů při přidávání vybavení
    - oprava focusovaných oken
    - Zvýšená kapacita produktů k jednomu objektu (z 26 na 78)
    - Varování při přepisování .xml souboru
    - Ukládání posledně zvolených souborů/ cest
    - Automaticky nabízí nalezené soubory
    - Oprava 2x export po sobě shodil aplikaci
    - Oprava chování po smazání stanice - pamatovalo si to
    některé parametry
    IP setting:
    - Podbarvování právě zvolených oken
    - Oprava braní focusu při přejezdu nad poznámkami
    - Optimalizace vyskakovacích oken
    Správa souborů - třídění:
    - Možnost při třídění podle id ignorovat nepáry\n"""
        ," Verze 3.7.5 (2.8.2024)"
        ,
    """ 
    - Oprava možnosti ignorovat nepáry
    - Optimalizace načítání buněk v ip setting\n"""
        ," Verze 3.7.6 (15.8.2024)"
        ,
    """ 
    - Úpravy v souboru Recources.txt
    IP setting:
    - úprava aut. velikosti widgetů
    - oprava chybových hlášení v consoli
    - při změně ip aktualizovat pouze statusy
    - refresh/odpojeni/pripojeni disku aktualizuje pouze statusy
    - opraven Tcl error
    - delší ověřování statusu disku (1s->2s)
    Katalog:
    - ukládání poslední cesty do config
    - filtrace uživatelských vstupů
    - vizualizace nastavení
    - možnost změnit defaultní název sharepoint databáze
    TRIMAZKON:
    - po změně nastavení v prohlížeči obrázků se zinitily
    defaultní parametry\n"""
        ," Verze 3.7.7 (22.8.2024)"
        ,
    """ 
    IP setting:
    - enterem při přímé editaci poznámek se přidá řádek
    - nová logika editace poznámek (zůstane rozbaleno)
    - opraveno chybové hlášení při neposkytnutí práv (pws)
    - klik mimo odebere focus widgetu
    - dotazování, zda určitě smazat projekt
    - přímé upravování všeho v sekci oblíbené
    - zvýraznění oblíbených v sekci všech
    - odolnost proti chybám v exelu
    - nová možnost zvolit si automatické řazení na začátek
    po editu projektu
    - ve všech oknech přidáno tlačítko zrušit
    TRIMAZKON:
    - Odolnost proti chybějícím config souborům
    - Opravy chybových hlášení\n"""
        ," Verze 3.8.0 (16.9.2024)"
        ,
    """ 
    IP setting:
    - oprava ukládání konfigurace nastavení
    - rozlišování persistent/ nepersistent disků
    - projekty lze nově přepínat v okně editu
    - nově lze mazat projekty v okně editu
    - nově možnost odvolit dotazovaní při mazání
    - bind tlačítka delete
    - lze vrátit posledně smazaný projekt
    - lze vrátit poslední provedené změny projektu
    - tlačítkem ctrl lze vybrat více projektů najednou
    - lze mazat více projektů najednou
    Prohlížeč obrázků
    - Ochrana před poškozenými soubory\n"""
]


default_setting_database = ["Podporované typy souborů u možností třídění:",
                            "Podporované typy souborů u možností mazání:",
                            "Základní cesta k souborům:",
                            "Základní množství ponechaných souborů: (MAZÁNÍ)",
                            "Základní cutoff date: (MAZÁNÍ)",
                            "Prefix funkce:",
                            "Prefix kamery:",
                            "Spouštět v maximalizovaném okne?",
                            "Základní maximální počet palet v oběhu: (Třídění)",
                            "Název složky pro nepáry (nezastoupenými všemi nalezenými formáty):",
                            "Název složky pro nalezené dvojice:",
                            "Název složky se soubory, které jsou určené ke smazání:",
                            "Název složky pro soubory převedené do .bmp formátu:",
                            "Název složky pro soubory převedené do .jpg formátu:",
                            "Název složky pro kopírované obrázky v prohlížeči obrázků:",
                            "Název složky pro přesunuté obrázky v prohlížeči obrázků:",
                            "Bezpečný mód při procházení subsložek:",
                            "Nastavení prohlížeče obrázků: (1. zvolená možnost, 2. krok přibližování [%], 3. krok posunu)",
                            "",
                            "",
                            "Zobrazit changelog?",
                            "Zobrazovat v prohlížeči obrázků film obrázků?",
                            "Kolik obrázků ve filmu obrázků zobrazovat na každé straně?",
                            "Default název pro sharepoint databázi:",
                            "Default název pro excel (Katalog):",
                            "Default název pro xml (Katalog):",
                            "Defaultní chování suboken (Katalog):",
                            "Defaultní přípona exportu (Katalog):",
                            "Defaultní cesta katalog:",
                            "nastavení celkového zoomu [%]:"
                            ]

default_setting_database_param = ["bmp,png",
                                "jpg,bmp,png,ifz",
                                "C:/Users/",
                                1000,
                                "28.02.2024",
                                "Func_",
                                "Cam_",
                                "ano",
                                55,
                                "Temp",
                                "Pairs",
                                "Ke_smazani",
                                "Konvertovane_BMP",
                                "Konvertovane_JPG",
                                "Kopírované_obrázky",
                                "Přesunuté_obrázky",
                                "ano",
                                2,
                                30,
                                40,
                                "ne",
                                "ano",
                                6,
                                "Sharepoint_databaze.xlsx",
                                "Katalog_kamerového_vybavení",
                                "_metadata_catalogue",
                                0,
                                "xlsx",
                                "C:/Users/",
                                80
                                ]