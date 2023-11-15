import customtkinter
import os
from PIL import Image, ImageTk
import trideni_JHV_v4_gui as Trideni
from tkinter import filedialog
import tkinter as tk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root=customtkinter.CTk()
root.geometry("1200x800")
root.wm_iconbitmap('JHV.ico')
root.title("Třídění souborů z průmyslových kamer")
#root.attributes('-fullscreen', True)

max_num_of_pallets = 55
ID_num_of_digits = 4
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
    #if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:
    if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get() == 0:
        console.configure(text = "Nevybrali jste žádný způsob třídění :-)")
        nothing = customtkinter.CTkImage(Image.open("nothing.png"),size=(1, 1))
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

    Trideni.whole_sorting_function(path,selected_sort,more_dirs,max_num_of_pallets,ID_num_of_digits)
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

def selected():
    clear_frame(frame6)
    console.configure(text = " ")
    view_image(1)
    checkbox2.deselect()
    checkbox3.deselect()
    checkbox4.deselect()
    checkbox5.deselect()
def selected2():
    clear_frame(frame6)
    console.configure(text = " ")
    view_image(2)
    checkbox.deselect()
    checkbox3.deselect()
    checkbox4.deselect()
    checkbox5.deselect()
def selected3():
    clear_frame(frame6)
    console.configure(text = " ")
    view_image(3)   
    checkbox.deselect()
    checkbox2.deselect()
    checkbox4.deselect()
    checkbox5.deselect()
def selected4():
    clear_frame(frame6)
    console.configure(text = " ")
    view_image(4)
    checkbox.deselect()
    checkbox2.deselect()
    checkbox3.deselect()
    checkbox5.deselect()
def selected5():
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
            console_frame6_1.configure(text = "")
            console_frame6_1.configure(text = "Nezadali jste číslo")
        else:
            console_frame6_1.configure(text = "")
            console_frame6_1.configure(text = f"Počet palet nastaven na: {input_1}")
            max_num_of_pallets = input_1

    def set_pair_variable2():
        global ID_num_of_digits
        input_2 = ID_digits_set.get()
        if input_2.isdigit() == False:
            console_frame6_2.configure(text = "")
            console_frame6_2.configure(text = "Nezadali jste číslo")
        else:   
            console_frame6_2.configure(text = "")
            console_frame6_2.configure(text = f"Počet cifer ID nastaven na: {input_2}")
            ID_num_of_digits = input_2


    label1 = customtkinter.CTkLabel(master = frame6,text = "Nastavte počet palet v oběhu:",justify = "left",font=("Arial",12))
    label1.pack(pady =1,padx=10)
    pallets_set = customtkinter.CTkEntry(master = frame6, placeholder_text= max_num_of_pallets)
    pallets_set.pack(pady =1,padx=10)
    button_save1 = customtkinter.CTkButton(master = frame6, text = "Uložit", command = lambda: set_pair_variable1(),font=("Arial",12,"bold"))
    button_save1.pack(pady =1,padx=10)
    console_frame6_1=customtkinter.CTkLabel(master = frame6,text = " ",justify = "left",font=("Arial",12))
    console_frame6_1.pack(pady =1,padx=10)

    label2 = customtkinter.CTkLabel(master = frame6,text = "Nastavte kolik cifer má ID:",justify = "left",font=("Arial",12))
    label2.pack(pady =1,padx=10)
    ID_digits_set = customtkinter.CTkEntry(master = frame6, placeholder_text= ID_num_of_digits)
    ID_digits_set.pack(pady =1,padx=10)
    button_save2 = customtkinter.CTkButton(master = frame6, text = "Uložit", command = lambda: set_pair_variable2(),font=("Arial",12,"bold"))
    button_save2.pack(pady =1,padx=10)
    console_frame6_2=customtkinter.CTkLabel(master = frame6,text = " ",justify = "left",font=("Arial",12))
    console_frame6_2.pack(pady =1,padx=10)
   

    
def selected6():
    if checkbox6.get() == 1:
        #dirs_more = customtkinter.CTkImage(Image.open("more_dirs.png"),size=(754, 151))
        dirs_more = customtkinter.CTkImage(Image.open("more_dirs.png"),size=(377, 76))
        images2.configure(image =dirs_more)   
        console2.configure(text = "nebo poslední složka obsahuje soubory přímo (neroztříděné)")
    else:
        #dirs_one = customtkinter.CTkImage(Image.open("dirs_ba.png"),size=(432, 133))
        dirs_one = customtkinter.CTkImage(Image.open("dirs_ba.png"),size=(288, 89))
        images2.configure(image =dirs_one)
        console2.configure(text = "nebo obsahuje soubory přímo (neroztříděné)")


def view_image(which_one):
    if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:
        nothing = customtkinter.CTkImage(Image.open("nothing.png"),size=(1, 1))
        images.configure(image = nothing)
        name_example.configure(text = "")
    if which_one == 1:
        type_24 = customtkinter.CTkImage(Image.open("24_type.png"),size=(447, 170))
        images.configure(image =type_24)
        name_example.configure(text = "221013_092241_0000000842_21_&Cam1Img  => .Height <=  .bmp")
    if which_one == 2:
        func_24 = customtkinter.CTkImage(Image.open("24_func.png"),size=(725, 170))
        images.configure(image =func_24)
        name_example.configure(text = "221013_092241_0000000842_  => 21 <=  _&Cam1Img.Height.bmp")
    if which_one == 3:
        cam_24 = customtkinter.CTkImage(Image.open("24_cam.png"),size=(874, 170))
        images.configure(image =cam_24)
        name_example.configure(text = "221013_092241_0000000842_21_&  => Cam1 <=  Img.Height.bmp")
    if which_one == 4:
        both_24 = customtkinter.CTkImage(Image.open("24_both.png"),size=(900, 170))
        images.configure(image =both_24)
        name_example.configure(text = "221013_092241_0000000842_  => 21 <=  _&  => Cam1 <=  Img.Height.bmp")
    if which_one == 5:
        PAIRS = customtkinter.CTkImage(Image.open("25basic.png"),size=(530, 170))
        images.configure(image =PAIRS)
        name_example.configure(text = "Nakopíruje nalezené dvojice souborů do složky s názvem PAIRS\n2023_04_13-07_11_09_xxxx_=> 0020 <=_&Cam2Img.Height.bmp")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=10,padx=5,fill="both",expand=False,side = "top")
frame2 = customtkinter.CTkFrame(master=root)
frame2.pack(pady=0,padx=5,fill="both",expand=False,side = "top")
frame5 = customtkinter.CTkScrollableFrame(master=root)
frame5.pack(pady=0,padx=5,fill="both",expand=True,side = "bottom")
frame3 = customtkinter.CTkFrame(master=root)
frame3.pack(pady=10,padx=5,fill="both",expand=True,side="left")
frame4 = customtkinter.CTkScrollableFrame(master=root)
frame4.pack(pady=10,padx=5,fill="both",expand=True,side="right")

frame6 = customtkinter.CTkFrame(master=root,height=250)
frame6.pack(pady=10,padx=0,fill="both",expand=False,side = "bottom")


logo = customtkinter.CTkImage(Image.open("logo2.bmp"),size=(571, 70))

image_logo = customtkinter.CTkLabel(master = frame,text = "",image =logo)
image_logo.pack()

entry1 = customtkinter.CTkEntry(master = frame2,placeholder_text="Zadejte cestu k souborům z kamery (kde se nacházejí složky se soubory nebo soubory přímo)")
entry1.pack(pady = 12,padx =10,anchor ="w",side="left",fill="both",expand=True)
tree = customtkinter.CTkButton(master = frame2, width = 200,text = "EXPLORER", command = browseDirectories,font=("Arial",20,"bold"))
tree.pack(pady = 12,padx =10,anchor ="w",side="left")




checkbox = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle typů souborů",command = selected)
checkbox.pack(pady =12,padx=10,anchor ="w")
checkbox2 = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle čísla funkce",command = selected2)
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
view_image(1)
selected6()

root.mainloop()



