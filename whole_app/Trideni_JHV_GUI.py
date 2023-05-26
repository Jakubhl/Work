import customtkinter
from PIL import Image, ImageTk
import trideni_JHV as Trideni


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry("1200x900")
root.wm_iconbitmap('JHV.ico')
root.title("Třídění souborů z průmyslových kamer")

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


    Trideni.output = []
    Trideni.whole_sorting_function(path,selected_sort)
    output_text = "Třídění provedeno\n"
    for i in range(0,len(Trideni.output)):
        output_text = output_text + Trideni.output[i] + "\n"

    console.configure(text = output_text)
    """if checkbox5.get() == 1:
        Trideni.whole_sorting_function(path,5)  """  
def selected():
    view_image(1)
    checkbox2.deselect()
    checkbox3.deselect()
    checkbox4.deselect()
    #checkbox5.deselect()
def selected2():
    view_image(2)
    checkbox.deselect()
    checkbox3.deselect()
    checkbox4.deselect()
    #checkbox5.deselect()
def selected3():
    view_image(3)
    checkbox.deselect()
    checkbox2.deselect()
    checkbox4.deselect()
    #checkbox5.deselect()
def selected4():
    view_image(4)
    checkbox.deselect()
    checkbox2.deselect()
    checkbox3.deselect()
    #checkbox5.deselect()
"""def selected5():
    view_image(5)
    checkbox2.deselect()
    checkbox3.deselect()
    checkbox4.deselect()
    checkbox.deselect()"""

def view_image(which_one):
    #if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:
    if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get() == 0:
        nothing = customtkinter.CTkImage(Image.open("nothing.png"),size=(1, 1))
        images.configure(image = nothing)
        name_example.configure(text = "")

    if which_one == 1:
        type_24 = customtkinter.CTkImage(Image.open("24_type.png"),size=(447, 175))
        images.configure(image =type_24)
        name_example.configure(text = "221013_092241_0000000842_21_&Cam1Img  => .Height <=  .bmp")
    if which_one == 2:
        func_24 = customtkinter.CTkImage(Image.open("24_func.png"),size=(725, 184))
        images.configure(image =func_24)
        name_example.configure(text = "221013_092241_0000000842_  => 21 <=  _&Cam1Img.Height.bmp")
    if which_one == 3:
        cam_24 = customtkinter.CTkImage(Image.open("24_cam.png"),size=(874, 173))
        images.configure(image =cam_24)
        name_example.configure(text = "221013_092241_0000000842_21_&  => Cam1 <=  Img.Height.bmp")
    if which_one == 4:
        both_24 = customtkinter.CTkImage(Image.open("24_both.png"),size=(1106, 210))
        images.configure(image =both_24)
        name_example.configure(text = "221013_092241_0000000842_  => 21 <=  _&  => Cam1 <=  Img.Height.bmp")
    """if which_one == 5:
        manual_24 = customtkinter.CTkImage(Image.open("24_manual.png"),size=(1003, 128))
        images.configure(image =manual_24)"""


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20,padx=60,fill="both",expand=True)

logo = customtkinter.CTkImage(Image.open("logo2.bmp"),size=(400, 49))

image_logo = customtkinter.CTkLabel(master = frame,text = " ",image =logo)
image_logo.pack()

#step_1 = customtkinter.CTkLabel(master = frame,text = "1) Zadejte cestu k souborum z kamery\n(zkopírovat do schránky nabo vložit aplikaci přímo do požadované složky a stisknout enter)",
step_1 = customtkinter.CTkLabel(master = frame,text = "1) Zadejte cestu k souborům z kamery (kde se nacházejí složky se soubory nebo soubory přímo)",
justify = "left",font=("Arial",20,"bold"))
step_1.pack(pady = 12,padx =10,anchor ="w")

entry1 = customtkinter.CTkEntry(master = frame, width = 600,placeholder_text="Zadejde cestu ke složce pro analýzu")
entry1.pack(pady = 12,padx =10,anchor ="w")

step_2 = customtkinter.CTkLabel(master = frame,text = "2) Nastavte způsob třídění nebo ponechte základní nastavení",justify = "left",font=("Arial",20,"bold"))
step_2.pack(pady = 12,padx =10,anchor ="w")

checkbox = customtkinter.CTkCheckBox(master = frame, text = "Třídit podle typů souborů",command = selected)
checkbox.pack(pady =12,padx=10,anchor ="w")
checkbox2 = customtkinter.CTkCheckBox(master = frame, text = "Třídit podle čísla funkce",command = selected2)
checkbox2.pack(pady =12,padx=10,anchor ="w")
checkbox3 = customtkinter.CTkCheckBox(master = frame, text = "Třídit podle čísla kamery",command = selected3)
checkbox3.pack(pady =12,padx=10,anchor ="w")
checkbox4 = customtkinter.CTkCheckBox(master = frame, text = "Třídit podle čísla funkce i kamery",command = selected4)
checkbox4.pack(pady =12,padx=10,anchor ="w")
"""checkbox5 = customtkinter.CTkCheckBox(master = frame, text = "Manuálně nastavit počet zakrytých znaků pro rozhodování",command = selected5)
checkbox5.pack(pady =12,padx=10,anchor ="w")"""

#misto pro zobrazovani obrazku
images = customtkinter.CTkLabel(master = frame,text = "")
images.pack()
name_example = customtkinter.CTkLabel(master = frame,text = "",font=("Arial",16,"bold"))
name_example.pack(pady = 12,padx =10)

#default:
checkbox.select()
view_image(1)

button = customtkinter.CTkButton(master = frame, text = "SPUSTIT", command = start,font=("Arial",20,"bold"))
button.pack(pady =12,padx=10)
button._set_dimensions(300,60)

console = customtkinter.CTkLabel(master = frame,text = " ",font=("Arial",15))
console.pack(pady =12,padx=10)




root.mainloop()



