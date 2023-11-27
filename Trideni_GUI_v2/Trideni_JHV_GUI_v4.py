import customtkinter
import os
from PIL import Image, ImageTk
import trideni_JHV_v4_gui as Trideni
import mazani_v1 as Deleting
from tkinter import filedialog
import tkinter as tk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root=customtkinter.CTk()
root.geometry("1200x900")
root.wm_iconbitmap('images/JHV.ico')
root.title("Zpracování souborů z průmyslových kamer")
#root.attributes('-fullscreen', True)

def menu():
    frame_with_logo = customtkinter.CTkFrame(master=root)
    frame_with_logo.pack(pady=10,padx=5,fill="both",expand=False,side = "top")
    frame_with_buttons = customtkinter.CTkFrame(master=root)
    frame_with_buttons.pack(pady=0,padx=5,fill="both",expand=True,side = "top")
    list_of_menu_frames = [frame_with_logo,frame_with_buttons]
    


    #logo = customtkinter.CTkImage(Image.open("images/logo2.bmp"),size=(571, 70))
    logo = customtkinter.CTkImage(Image.open("images/logo.png"),size=(961, 125))
    image_logo = customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
    image_logo.pack()

    labelx = customtkinter.CTkLabel(master = frame_with_buttons,width=400,height=185,text = "",justify = "left") #jen vyplni volny prostor
    labelx.grid(column =0,row=0,pady =0,padx=0)

    #label_menu = customtkinter.CTkLabel(master = frame_with_buttons,width=400,height=100,text = "MENU",justify = "left",font=("Arial",30,"bold"))
    #label_menu.grid(column =1,row=1,pady =0,padx=0)

    sorting_button = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Možnosti třídění souborů", command = lambda: Sorting_option(list_of_menu_frames),font=("Arial",25,"bold"))
    sorting_button.grid(column =1,row=2,pady =20,padx=0)
    deleting_button = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Možnosti mazání souborů", command = lambda: Deleting_option(list_of_menu_frames),font=("Arial",25,"bold"))
    deleting_button.grid(column =1,row=3,pady =0,padx=0)
    convert_button = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Možnosti konvertování souborů", command = lambda: Sorting_option(list_of_menu_frames),font=("Arial",25,"bold"))
    convert_button.grid(column =1,row=4,pady =20,padx=0)

    root.mainloop()

def Deleting_option(list_of_menu_frames):
    #cisteni menu widgets
    for frames in list_of_menu_frames: 
        frames.pack_forget()
        frames.grid_forget()
        frames.destroy()
    
    global more_dirs
    more_dirs = False
    global files_to_keep
    files_to_keep = 1000
    global cutoff_date
    cutoff_date = ["01","01","1999"]

    #cisteni pred vstupem do menu
    def call_menu():
        list_of_frames = [frame_with_logo,frame_path_input,bottom_frame1,bottom_frame2,frame_right,frame_with_checkboxes]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        menu()
    #definice EXPLORERU
    def browseDirectories():
        programme_path = os.getcwd()
        if os.path.exists(programme_path+"/"+"Default_path.txt"):
            f = open("Default_path.txt", "r")
            start_path = str(f.read())
            if not os.path.exists(start_path):
                start_path = ""
                console.configure(text="")
                console.configure(text="Konfigurační soubor obsahuje neplatnou cestu")

        else:
            console.configure(text="")
            console.configure(text="Chybí konfigurační soubor s počáteční cestou...\n(Založte s názvem: Default_path.txt)")
            start_path=""

        if(start_path != ""):
            foldername_path = filedialog.askdirectory(initialdir = start_path,
                                                title = "Select a Directory",
                                                )
        else:
            foldername_path = filedialog.askdirectory(initialdir = "/",
                                                title = "Select a Directory",
                                                )

        check = Trideni.path_check(foldername_path)
        if check == False:
            console.configure(text="")
            console.configure(text = "Zadaná cesta: "+foldername_path+" nebyla nalezena")
        else:
            if foldername_path != "":
                entry1.delete("0","100")
                entry1.insert("0", foldername_path)
                console.configure(text="")
                console.configure(text = "Byla vložena cesta: " + foldername_path)

    
    def start():
        if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:
            console.configure(text = "Nevybrali jste žádný způsob třídění :-)")
            #nothing = customtkinter.CTkImage(Image.open("images/nothing.png"),size=(1, 1))
            #images.configure(image = nothing)
            info.configure(text = "")

        else:
            path = entry1.get() 
            if path != "":
                check = Trideni.path_check(path)
                if check == False:
                    console.configure(text = "Zadaná cesta: "+str(path)+" nebyla nalezena")
                else:
                    path = check
                    console.configure(text = str(path)+" je OK")
                    del_files(path)
            else:
                console.configure(text = "Nebyla vložena cesta k souborům")

    def del_files(path):
        del_option = 0
        if checkbox.get() == 1:
            del_option = 1
        if checkbox2.get() == 1:
            del_option = 2
        if checkbox3.get() == 1:
            del_option = 3
        if checkbox4.get() == 1:
            del_option = 4
        if checkbox5.get() == 1:
            del_option = 5
        if checkbox6.get() == 1:
            more_dirs = True
        else:
            more_dirs = False

        Deleting.output = []
        #Deleting.output_console2 = []

        Deleting.whole_deleting_function(path,more_dirs,del_option,files_to_keep,cutoff_date)
        output_text = ""
        #output_text2 = ""
        for i in range(0,len(Deleting.output)):
            output_text = output_text + Deleting.output[i]# + "\n"
        console.configure(text = output_text)

        #if len(Deleting.output_console2) != 0:
            #for i in range(0,len(Deleting.output_console2)):
                #output_text2 = output_text2 + Deleting.output_console2[i]# + "\n"
            #console2.configure(text = output_text2)

    #definice ramcu
    frame_with_logo = customtkinter.CTkFrame(master=root)
    frame_with_logo.pack(pady=0,padx=5,fill="both",expand=False,side = "top")
    frame_path_input = customtkinter.CTkFrame(master=root)
    frame_path_input.pack(pady=5,padx=5,fill="both",expand=False,side = "top")
    bottom_frame2 = customtkinter.CTkScrollableFrame(master=root)
    bottom_frame2.pack(pady=0,padx=5,fill="both",expand=True,side = "bottom")
    bottom_frame1 = customtkinter.CTkFrame(master=root,height = 80)
    bottom_frame1.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
    checkbox_frame = customtkinter.CTkFrame(master=root,width=400)
    checkbox_frame.pack(pady=0,padx=5,fill="y",expand=False,side="left")
    frame_right = customtkinter.CTkScrollableFrame(master=root)
    frame_right.pack(pady=0,padx=5,fill="both",expand=True,side="right")
    

    logo = customtkinter.CTkImage(Image.open("images/logo.png"),size=(961, 125))
    image_logo = customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
    image_logo.pack()

    menu_button = customtkinter.CTkButton(master = frame_path_input, width = 180, text = "MENU", command = lambda: call_menu(),font=("Arial",20,"bold"))
    menu_button.pack(pady =12,padx=10,anchor ="w",side="left")
    entry1 = customtkinter.CTkEntry(master = frame_path_input,placeholder_text="Zadejte cestu k souborům z kamery (kde se nacházejí složky se soubory nebo soubory přímo)")
    entry1.pack(pady = 12,padx =0,anchor ="w",side="left",fill="both",expand=True)
    tree = customtkinter.CTkButton(master = frame_path_input, width = 180,text = "EXPLORER", command = browseDirectories,font=("Arial",20,"bold"))
    tree.pack(pady = 12,padx =10,anchor ="w",side="left")

    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def selected(console_frame_right_1_text,console_frame_right_2_text):
        clear_frame(frame_right)
        console.configure(text = " ")
        #view_image(1)
        checkbox2.deselect()
        checkbox3.deselect()
        checkbox4.deselect()
        checkbox5.deselect()
        info.configure(text = "")
        info.configure(text = f"- Budou smazány soubory starší než nastavené datum, přičemž bude ponechán nastavený počet souborů, vyhodnocených, jako starších\nPodporované formáty: {Deleting.supported_formats}",font = ("Arial",16,"bold"),justify="left")
        selected6() #update

        def set_cutoff_date():
            console_frame_right_1_text = ""
            console_frame_right_2_text = ""  
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        cutoff_date[1] = int(input_month)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Měsíc: " + str(input_month) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "U nastavení měsíce jste nezadali číslo"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        cutoff_date[0] = int(input_day)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Den: " + str(input_day) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "U nastavení dne jste nezadali číslo"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        cutoff_date[2] = int(input_year) + 2000
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    elif len(str(input_year)) == 4:
                        cutoff_date[2] = int(input_year)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Rok: " + str(input_year) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "U nastavení roku jste nezadali číslo"

            selected(console_frame_right_1_text,console_frame_right_2_text)

        def set_files_to_keep():
            global files_to_keep
            input_files_to_keep = files_to_keep_set.get()
            if input_files_to_keep.isdigit():
                if int(input_files_to_keep) >= 0:
                    files_to_keep = int(input_files_to_keep)
                    console_frame_right_2.configure(text="")
                    console_frame_right_2_text = "Počet ponechaných starších souborů nastaven na: " + str(files_to_keep)
                else:
                    console_frame_right_2.configure(text="")
                    console_frame_right_2_text = "Mimo rozsah"
            else:
                console_frame_right_2.configure(text="")
                console_frame_right_2_text = "Nazadali jste číslo"

            
            selected(console_frame_right_1_text,console_frame_right_2_text)

        today = Deleting.get_current_date()
        row_index = 0
        label0 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",16,"bold"))
        label1 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",12))
        set_day = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[0])
        sep1 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_month = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[1])
        sep2 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_year = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_cutoff_date(),font=("Arial",12,"bold"))
        console_frame_right_1=customtkinter.CTkLabel(master = frame_right,height=30,text = console_frame_right_1_text,justify = "left",font=("Arial",12))
        label0.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        console_frame_right_1.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)

        label2 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte počet ponechaných souborů, vyhodnocených jako starších:",justify = "left",font=("Arial",12))
        files_to_keep_set = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= files_to_keep)
        button_save2 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_files_to_keep(),font=("Arial",12,"bold"))
        console_frame_right_2=customtkinter.CTkLabel(master = frame_right,height=30,text =console_frame_right_2_text,justify = "left",font=("Arial",12))
        label2.grid(column =0,row=5,sticky = tk.W,pady =0,padx=10)
        files_to_keep_set.grid(column =0,row=6,sticky = tk.W,pady =0,padx=10)
        button_save2.grid(column =0,row=6,sticky = tk.W,pady =0,padx=60)
        console_frame_right_2.grid(column =0,row=7,sticky = tk.W,pady =0,padx=10)
          
    def selected2(console_frame_right_1_text,console_frame_right_2_text):
        clear_frame(frame_right)
        console.configure(text = " ")
        checkbox.deselect()
        checkbox3.deselect()
        checkbox4.deselect()
        checkbox5.deselect()
        info.configure(text = "")
        info.configure(text = f"- Budou smazány VŠECHNY soubory starší než nastavené datum, přičemž budou redukovány i soubory novější\n- Souborů, vyhodnocených, jako novější, bude ponechán nastavený počet\n(vhodné při situacích rychlého pořizování velkého množství fotografií, kde je potřebné ponechat nějaké soubory pro referenci)\nPodporované formáty: {Deleting.supported_formats}",font = ("Arial",16,"bold"),justify="left")
        selected6() #update

        def set_cutoff_date():
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        cutoff_date[1] = int(input_month)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Měsíc: " + str(input_month) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        cutoff_date[0] = int(input_day)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Den: " + str(input_day) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        cutoff_date[2] = int(input_year) + 2000
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    elif len(str(input_year)) == 4:
                        cutoff_date[2] = int(input_year)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Rok: " + str(input_year) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

                        
            selected2(console_frame_right_1_text,console_frame_right_2_text)

        def set_files_to_keep():
            global files_to_keep
            input_files_to_keep = files_to_keep_set.get()
            if input_files_to_keep.isdigit():
                if int(input_files_to_keep) >= 0:
                    files_to_keep = int(input_files_to_keep)
                    console_frame_right_2.configure(text="")
                    console_frame_right_2_text = "Počet ponechaných starších souborů nastaven na: " + str(files_to_keep)
                else:
                    console_frame_right_2.configure(text="")
                    console_frame_right_2_text = "Mimo rozsah"
            else:
                console_frame_right_2.configure(text="")
                console_frame_right_2_text = "Nazadali jste číslo"

            
            selected2(console_frame_right_1_text,console_frame_right_2_text)

        today = Deleting.get_current_date()
        row_index = 0
        label0 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",16,"bold"))
        label1 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",12))
        set_day = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[0])
        sep1 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_month = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[1])
        sep2 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_year = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_cutoff_date(),font=("Arial",12,"bold"))
        console_frame_right_1=customtkinter.CTkLabel(master = frame_right,height=30,text = console_frame_right_1_text,justify = "left",font=("Arial",12))
        label0.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        console_frame_right_1.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)

        label2 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte počet ponechaných novějších souborů:",justify = "left",font=("Arial",12))
        files_to_keep_set = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= files_to_keep)
        button_save2 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_files_to_keep(),font=("Arial",12,"bold"))
        console_frame_right_2=customtkinter.CTkLabel(master = frame_right,height=30,text =console_frame_right_2_text,justify = "left",font=("Arial",12))
        label2.grid(column =0,row=5,sticky = tk.W,pady =0,padx=10)
        files_to_keep_set.grid(column =0,row=6,sticky = tk.W,pady =0,padx=10)
        button_save2.grid(column =0,row=6,sticky = tk.W,pady =0,padx=60)
        console_frame_right_2.grid(column =0,row=7,sticky = tk.W,pady =0,padx=10)
        
    def selected3(console_frame_right_1_text,console_frame_right_2_text):
        clear_frame(frame_right)
        console.configure(text = " ")
        checkbox2.deselect()
        checkbox.deselect()
        checkbox4.deselect()
        checkbox5.deselect()
        info.configure(text = "")
        info.configure(text = f"- Budou smazány VŠECHNY adresáře (včetně všech subadresářů), které obsahují v názvu podporovaný formát datumu a jsou vyhodnoceny,\njako starší než nastavené datum\nPodporované datumové formáty: {Deleting.supported_date_formats}\nPodporované separátory datumu: {Deleting.supported_separators}",font = ("Arial",16,"bold"),justify="left")
        selected6() #update

        def set_cutoff_date():
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        cutoff_date[1] = int(input_month)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Měsíc: " + str(input_month) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        cutoff_date[0] = int(input_day)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Den: " + str(input_day) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        cutoff_date[2] = int(input_year) + 2000
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    elif len(str(input_year)) == 4:
                        cutoff_date[2] = int(input_year)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Rok: " + str(input_year) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

                        
            selected3(console_frame_right_1_text,console_frame_right_2_text)

        today = Deleting.get_current_date()
        row_index = 0
        label0 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",16,"bold"))
        images2 = customtkinter.CTkLabel(master = frame_right,text = "")
        label1 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte datum pro vyhodnocení datumu v názvu adresářů, jako staršího:",justify = "left",font=("Arial",12))
        set_day = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[0])
        sep1 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_month = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[1])
        sep2 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_year = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_cutoff_date(),font=("Arial",12,"bold"))
        console_frame_right_1=customtkinter.CTkLabel(master = frame_right,height=30,text = console_frame_right_1_text,justify = "left",font=("Arial",12))
        directories = customtkinter.CTkImage(Image.open("images/directories.png"),size=(240, 190))

        label0.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        images2.grid(column =0,row=row_index,sticky = tk.W,pady =10,padx=500,rowspan=5)
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        console_frame_right_1.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)
        images2.configure(image = directories)

    def selected4():
        console.configure(text = " ")
        checkbox2.deselect()
        checkbox3.deselect()
        checkbox.deselect()
        checkbox5.deselect()
        info.configure(text = "")

    def selected5():
        console.configure(text = " ")
        checkbox2.deselect()
        checkbox3.deselect()
        checkbox4.deselect()
        checkbox.deselect()
        info.configure(text = "")

    def selected6():
        if checkbox6.get() == 1:
            if checkbox3.get() == 1:
                info2.configure(text = "- Pro tuto možnost třídění není tato funkce podporována",font=("Arial",16,"bold"))
            else:
                info2.configure(text = "- VAROVÁNÍ: Máte spuštěné možnosti mazání souborů i ve všech subsložkách vložené cesty (max:6 subsložek)",font=("Arial",16,"bold"))
        else:
            info2.configure(text = "")

    frame_with_checkboxes = checkbox_frame

    checkbox = customtkinter.CTkCheckBox(master = frame_with_checkboxes, text = "Mazání souborů starších než: určité datum",command = lambda: selected("",""))
    checkbox.pack(pady =12,padx=10,anchor ="w")
    checkbox2 = customtkinter.CTkCheckBox(master = frame_with_checkboxes, text = "Redukce novějších, mazání souborů starších než: určité datum",command = lambda: selected2("",""))
    checkbox2.pack(pady =12,padx=10,anchor ="w")
    checkbox3 = customtkinter.CTkCheckBox(master = frame_with_checkboxes, text = "Mazání adresářů s názvem ve formátu určitého datumu",command = lambda: selected3("",""))
    checkbox3.pack(pady =12,padx=10,anchor ="w")
    checkbox4 = customtkinter.CTkCheckBox(master = frame_with_checkboxes, text = "rezerva",command = selected4)
    checkbox4.pack(pady =12,padx=10,anchor ="w")
    checkbox5 = customtkinter.CTkCheckBox(master = frame_with_checkboxes, text = "rezerva",command = selected5)
    checkbox5.pack(pady =12,padx=10,anchor ="w")

    #images = customtkinter.CTkLabel(master = bottom_frame2,text = "")
    #images.pack()
    checkbox6 = customtkinter.CTkCheckBox(master = bottom_frame1, text = "Procházet subsložky? (max:6)",command = selected6,font=("Arial",16,"bold"))
    checkbox6.grid(column =0,row=0,sticky = tk.W,pady =12,padx=10)
    info2 = customtkinter.CTkLabel(master = bottom_frame1,text = "",font=("Arial",16,"bold"))
    info2.grid(column =0,row=0,sticky = tk.W,pady =12,padx=300)
    info = customtkinter.CTkLabel(master = bottom_frame2,text = "",font=("Arial",16,"bold"))
    info.pack(pady = 12,padx =10,anchor="w")
    button = customtkinter.CTkButton(master = bottom_frame2, text = "SPUSTIT", command = start,font=("Arial",20,"bold"))
    button.pack(pady =20,padx=10)
    button._set_dimensions(300,60)
    console = customtkinter.CTkLabel(master = bottom_frame2,text = " ",justify = "left",font=("Arial",15))
    console.pack(pady =10,padx=10)

    #default:
    checkbox.select()
    selected("","")

    root.mainloop()

def Sorting_option(list_of_menu_frames):
    for frames in list_of_menu_frames:
        frames.pack_forget()
        frames.grid_forget()
        frames.destroy()

    prefix_func = "Func_"
    prefix_Cam = "Cam_"
    max_num_of_pallets = 55
    by_which_ID_num = ""
    global more_dirs
    more_dirs = False

    def browseDirectories():
        programme_path = os.getcwd()
        if os.path.exists(programme_path+"/"+"Default_path.txt"):
            f = open("Default_path.txt", "r")
            start_path = str(f.read())
            if not os.path.exists(start_path):
                start_path = ""
                console.configure(text="")
                console.configure(text="Konfigurační soubor obsahuje neplatnou cestu")

        else:
            console.configure(text="")
            console.configure(text="Chybí konfigurační soubor s počáteční cestou...\n(Založte s názvem: Default_path.txt)")
            start_path=""

        if(start_path != ""):
            foldername_path = filedialog.askdirectory(initialdir = start_path,
                                                title = "Select a Directory",
                                                )
        else:
            foldername_path = filedialog.askdirectory(initialdir = "/",
                                                title = "Select a Directory",
                                                )

        check = Trideni.path_check(foldername_path)
        if check == False:
            console.configure(text="")
            console.configure(text = "Zadaná cesta: "+foldername_path+" nebyla nalezena")
        else:
            if foldername_path != "":
                entry1.delete("0","100")
                entry1.insert("0", foldername_path)
                console.configure(text="")
                console.configure(text = "Byla vložena cesta: " + foldername_path)
                

    def start():
        if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:
            console.configure(text = "Nevybrali jste žádný způsob třídění :-)")
            nothing = customtkinter.CTkImage(Image.open("images/nothing.png"),size=(1, 1))
            images.configure(image = nothing)
            name_example.configure(text = "")

        else:
            path = entry1.get() 
            if path != "":
                check = Trideni.path_check(path)
                if check == False:
                    console.configure(text = "Zadaná cesta: "+str(path)+" nebyla nalezena")
                else:
                    path = check
                    console.configure(text = str(path)+" je OK")
                    sort_files(path)
            else:
                console.configure(text = "Nebyla vložena cesta k souborům")

    def sort_files(path):
        selected_sort = 0
        if checkbox.get() == 1:
            selected_sort = 1
        if checkbox2.get() == 1:
            selected_sort = 2
        if checkbox3.get() == 1:
            selected_sort = 3
        if checkbox4.get() == 1:
            selected_sort = 4
        if checkbox5.get() == 1:
            selected_sort = 5
        if checkbox6.get() == 1:
            more_dirs = True
        else:
            more_dirs = False

        Trideni.output = []
        Trideni.output_console2 = []

        Trideni.whole_sorting_function(path,selected_sort,more_dirs,max_num_of_pallets,by_which_ID_num,prefix_func,prefix_Cam)
        output_text = ""
        output_text2 = ""
        for i in range(0,len(Trideni.output)):
            output_text = output_text + Trideni.output[i] + "\n"
        console.configure(text = output_text)

        for i in range(0,len(Trideni.output_console2)):
            output_text2 = output_text2 + Trideni.output_console2[i] + "\n"
        console2.configure(text = output_text2)


    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def selected(): #tridit podle typu souboru
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(1)
        checkbox2.deselect()
        checkbox3.deselect()
        checkbox4.deselect()
        checkbox5.deselect()

        labelx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=height_of_frame6+10,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=0,pady =0,padx=10)
        

    def selected2(): #tridit polde cisla funkce (ID)
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(2)
        checkbox.deselect()
        checkbox3.deselect()
        checkbox4.deselect()
        checkbox5.deselect()

        def set_prefix():
            global prefix_func
            input_1 = prefix_set.get()
            console_frame6_1.configure(text = f"Prefix nastaven na: {input_1}")
            prefix_func = input_1

        label1 = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=20,text = "Nastavte prefix adresářů:",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        prefix_set = customtkinter.CTkEntry(master = frame6,width=150,height=30, placeholder_text= prefix_func)
        prefix_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1 = customtkinter.CTkButton(master = frame6,width=50,height=30, text = "Uložit", command = lambda: set_prefix(),font=("Arial",12,"bold"))
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1=customtkinter.CTkLabel(master = frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)

        labelx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=30,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=3,pady =0,padx=10)
        checkbox_advance = customtkinter.CTkCheckBox(master = frame6,height=30, text = "Pokročilá nastavení",command = selected2_advance)
        checkbox_advance.grid(column =0,row=4,pady =0,padx=10)
        labelxx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=120,text = "",justify = "left",font=("Arial",12))
        labelxx.grid(column =0,row=5,pady =0,padx=10)

    def selected2_advance():
        clear_frame(frame6)

        def set_which_num_of_ID():
            global by_which_ID_num
            input3=num_set.get()
            if input3.isdigit():
                if int(input3) > 0:
                    by_which_ID_num = int(input3)
                    console_frame6_1.configure(text = f"Řídit podle {by_which_ID_num}. čísla v ID")
                else:
                    console_frame6_1.configure(text = "Mimo rozsah")
                    by_which_ID_num = ""
            else:
                by_which_ID_num = ""

        label1 = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=60,
                                        text = "Podle kterého čísla v ID se řídit:\n(např. poslední č. v ID = pozice dílu...)\nvolte první = 1 atd. (prázdné = celé ID)",
                                        justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        num_set = customtkinter.CTkEntry(master = frame6,height=30,width=150, placeholder_text= by_which_ID_num)
        num_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1 = customtkinter.CTkButton(master = frame6,height=30,width=50, text = "Uložit", command = lambda: set_which_num_of_ID(),font=("Arial",12,"bold"))
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1=customtkinter.CTkLabel(master = frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)
        
        labelx2 = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=30,text = "",justify = "left",font=("Arial",12))
        labelx2.grid(column =0,row=3,pady =0,padx=10)
        
        button_back = customtkinter.CTkButton(master = frame6,width=100,height=30, text = "Zpět", command = selected2,font=("Arial",12,"bold"))
        button_back.grid(column =0,row=5,pady =0,padx=10)

        labelx3 = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=80,text = "",justify = "left",font=("Arial",12))
        labelx3.grid(column =0,row=6,pady =0,padx=10)
        
        

    def selected3(): #tridit podle cisla kamery
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(3)   
        checkbox.deselect()
        checkbox2.deselect()
        checkbox4.deselect()
        checkbox5.deselect()

        def set_prefix():
            global prefix_Cam
            input_1 = prefix_set.get()
            console_frame6_1.configure(text = f"Prefix nastaven na: {input_1}")
            prefix_Cam = input_1


        label1 = customtkinter.CTkLabel(master = frame6,height=20,width=width_of_frame6,text = "Nastavte prefix adresářů:",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        prefix_set = customtkinter.CTkEntry(master = frame6,height=30,width=150, placeholder_text= prefix_Cam)
        prefix_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1 = customtkinter.CTkButton(master = frame6,height=30,width=50, text = "Uložit", command = lambda: set_prefix(),font=("Arial",12,"bold"))
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1=customtkinter.CTkLabel(master = frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)

        labelx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=180,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=3,pady =0,padx=10)
        

    def selected4(): #tridit podle obojiho
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(4)
        checkbox.deselect()
        checkbox2.deselect()
        checkbox3.deselect()
        checkbox5.deselect()

        labelx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=height_of_frame6+10,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=0,pady =0,padx=10)
        

    def selected5(): #hledani paru
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(5)
        checkbox.deselect()
        checkbox2.deselect()
        checkbox3.deselect()
        checkbox4.deselect()
        
        def set_pair_variable1():
            global max_num_of_pallets
            input_1 = pallets_set.get()
            if input_1.isdigit() == False:
                console_frame6_1.configure(text = "Nezadali jste číslo")
            elif int(input_1) <1:
                console_frame6_1.configure(text = "Mimo rozsah")
            else:
                console_frame6_1.configure(text = f"Počet palet nastaven na: {input_1}")
                max_num_of_pallets = input_1

        label1 = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=60,text = "Nastavte počet palet v oběhu:\nPro aut. detekci ponechte\ndef. hodnotu (55)",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        pallets_set = customtkinter.CTkEntry(master = frame6,width=150,height=30, placeholder_text= max_num_of_pallets)
        pallets_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1 = customtkinter.CTkButton(master = frame6,width=50,height=30, text = "Uložit", command = lambda: set_pair_variable1(),font=("Arial",12,"bold"))
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1=customtkinter.CTkLabel(master = frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)

        labelx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=140,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=3,pady =0,padx=10)
        

    def selected6():
        if checkbox6.get() == 1:
            #dirs_more = customtkinter.CTkImage(Image.open("images/more_dirs.png"),size=(754, 151))
            dirs_more = customtkinter.CTkImage(Image.open("images/more_dirs.png"),size=(553, 111))
            #dirs_more = customtkinter.CTkImage(Image.open("images/more_dirs.png"),size=(377, 76))
            images2.configure(image =dirs_more)   
            console2.configure(text = "nebo poslední složka obsahuje soubory přímo (neroztříděné)",font=("Arial",16,"bold"))
            console2.configure(font=("Arial",12))
        else:
            dirs_one = customtkinter.CTkImage(Image.open("images/dirs_ba.png"),size=(432, 133))
            #dirs_one = customtkinter.CTkImage(Image.open("images/dirs_ba.png"),size=(288, 89))
            images2.configure(image =dirs_one)
            console2.configure(text = "nebo obsahuje soubory přímo (neroztříděné)",font=("Arial",16,"bold"))
            console2.configure(font=("Arial",12))


    def view_image(which_one):
        if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:
            nothing = customtkinter.CTkImage(Image.open("images/nothing.png"),size=(1, 1))
            images.configure(image = nothing)
            name_example.configure(text = "")
        else:
            if which_one == 1:
                type_24 = customtkinter.CTkImage(Image.open("images/24_type.png"),size=(447, 170))
                images.configure(image =type_24)
                name_example.configure(text = "221013_092241_0000000842_21_&Cam1Img  => .Height <=  .bmp")
            if which_one == 2:
                func_24 = customtkinter.CTkImage(Image.open("images/24_func.png"),size=(725, 170))
                images.configure(image =func_24)
                name_example.configure(text = "221013_092241_0000000842_  => 21 <=  _&Cam1Img.Height.bmp")
            if which_one == 3:
                cam_24 = customtkinter.CTkImage(Image.open("images/24_cam.png"),size=(874, 170))
                images.configure(image =cam_24)
                name_example.configure(text = "221013_092241_0000000842_21_&  => Cam1 <=  Img.Height.bmp")
            if which_one == 4:
                both_24 = customtkinter.CTkImage(Image.open("images/24_both.png"),size=(900, 170))
                images.configure(image =both_24)
                name_example.configure(text = "221013_092241_0000000842_  => 21 <=  _&  => Cam1 <=  Img.Height.bmp")
            if which_one == 5:
                PAIRS = customtkinter.CTkImage(Image.open("images/25basic.png"),size=(530, 170))
                images.configure(image =PAIRS)
                name_example.configure(
                    text = "Nakopíruje nalezené dvojice souborů do složky s názvem PAIRS\n(např. obsluha vloží dvakrát stejnou paletu po sobě před kameru)\n2023_04_13-07_11_09_xxxx_=> 0020 <=_&Cam2Img.Height.bmp\n(funkce postupuje podle časové známky v názvu souboru, kdy byly soubory pořízeny)")
    def call_menu():
        list_of_frames = [frame,frame2,frame3,frame4,frame5,frame6]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        menu()

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=10,padx=5,fill="both",expand=False,side = "top")
    frame2 = customtkinter.CTkFrame(master=root)
    frame2.pack(pady=0,padx=5,fill="both",expand=False,side = "top")
    frame5 = customtkinter.CTkScrollableFrame(master=root)
    frame5.pack(pady=0,padx=5,fill="both",expand=True,side = "bottom")
    frame3 = customtkinter.CTkFrame(master=root,width=400)
    frame3.pack(pady=10,padx=5,fill="y",expand=False,side="left")
    frame4 = customtkinter.CTkScrollableFrame(master=root)
    frame4.pack(pady=10,padx=5,fill="both",expand=True,side="right")

    height_of_frame6 = 250
    width_of_frame6 = 200
    frame6 = customtkinter.CTkFrame(master=root,height=height_of_frame6,width = width_of_frame6)
    frame6.pack(pady=10,padx=0,fill="both",expand=False,side = "bottom")


    #logo = customtkinter.CTkImage(Image.open("logo2.bmp"),size=(571, 70))
    logo = customtkinter.CTkImage(Image.open("images/logo.png"),size=(961, 125))
    image_logo = customtkinter.CTkLabel(master = frame,text = "",image =logo)
    image_logo.pack()

    menu_button = customtkinter.CTkButton(master = frame2, width = 180, text = "MENU", command = lambda: call_menu(),font=("Arial",20,"bold"))
    menu_button.pack(pady =12,padx=10,anchor ="w",side="left")
    entry1 = customtkinter.CTkEntry(master = frame2,placeholder_text="Zadejte cestu k souborům z kamery (kde se nacházejí složky se soubory nebo soubory přímo)")
    entry1.pack(pady = 12,padx =0,anchor ="w",side="left",fill="both",expand=True)
    tree = customtkinter.CTkButton(master = frame2, width = 180,text = "EXPLORER", command = browseDirectories,font=("Arial",20,"bold"))
    tree.pack(pady = 12,padx =10,anchor ="w",side="left")

    checkbox = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle typů souborů",command = selected)
    checkbox.pack(pady =12,padx=10,anchor ="w")
    checkbox2 = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle čísla funkce (ID)",command = selected2)
    checkbox2.pack(pady =12,padx=10,anchor ="w")
    checkbox3 = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle čísla kamery",command = selected3)
    checkbox3.pack(pady =12,padx=10,anchor ="w")
    checkbox4 = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle čísla funkce i kamery",command = selected4)
    checkbox4.pack(pady =12,padx=10,anchor ="w")
    checkbox5 = customtkinter.CTkCheckBox(master = frame3, text = "Najít dvojice (soubory se stejným ID, v řadě za sebou)",command = selected5)
    checkbox5.pack(pady =12,padx=10,anchor ="w")

    checkbox6 = customtkinter.CTkCheckBox(master = frame4, text = "Projít subsložky?",command = selected6)
    checkbox6.pack(pady =12,padx=10,anchor="w")
    images2 = customtkinter.CTkLabel(master = frame4,text = "")
    images2.pack()
    console2 = customtkinter.CTkLabel(master = frame4,text = " ",font=("Arial",12))
    console2.pack(pady =5,padx=10)


    images = customtkinter.CTkLabel(master = frame5,text = "")
    images.pack()
    name_example = customtkinter.CTkLabel(master = frame5,text = "",font=("Arial",16,"bold"))
    name_example.pack(pady = 12,padx =10)
    button = customtkinter.CTkButton(master = frame5, text = "SPUSTIT", command = start,font=("Arial",20,"bold"))
    button.pack(pady =12,padx=10)
    button._set_dimensions(300,60)
    console = customtkinter.CTkLabel(master = frame5,text = " ",justify = "left",font=("Arial",15))
    console.pack(pady =10,padx=10)


    #default:
    checkbox.select()
    selected()
    view_image(1)
    selected6()

    root.mainloop()

menu()