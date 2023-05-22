import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry("1200x700")
root.wm_iconbitmap('JHV.ico')
root.title("Třídění souborů z průmyslových kamer")


def start():
    if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:
        print("Nic jste nevybrali :-)")
    else:
        print("jo")


def selected():
    view_image(1)
    checkbox2.deselect()
    checkbox3.deselect()
    checkbox4.deselect()
    checkbox5.deselect()
def selected2():
    view_image(2)
    checkbox.deselect()
    checkbox3.deselect()
    checkbox4.deselect()
    checkbox5.deselect()
def selected3():
    view_image(3)
    checkbox.deselect()
    checkbox2.deselect()
    checkbox4.deselect()
    checkbox5.deselect()
def selected4():
    view_image(4)
    checkbox.deselect()
    checkbox2.deselect()
    checkbox3.deselect()
    checkbox5.deselect()
def selected5():
    view_image(5)
    checkbox2.deselect()
    checkbox3.deselect()
    checkbox4.deselect()
    checkbox.deselect()

def view_image(which_one):
    if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:

        nothing = customtkinter.CTkImage(Image.open("nothing.png"),size=(400, 70))
        images.configure(image = nothing)

    if which_one == 1:
        type_24 = customtkinter.CTkImage(Image.open("24_type.png"),size=(400, 70))
        images.configure(image =type_24)

    if which_one == 2:
        func_24 = customtkinter.CTkImage(Image.open("24_func.png"),size=(400, 70))
        images.configure(image =func_24)

    if which_one == 3:
        cam_24 = customtkinter.CTkImage(Image.open("24_cam.png"),size=(400, 70))
        images.configure(image =cam_24)

    if which_one == 4:
        both_24 = customtkinter.CTkImage(Image.open("24_both.png"),size=(400, 70))
        images.configure(image =both_24)

    if which_one == 5:
        manual_24 = customtkinter.CTkImage(Image.open("24_manual.png"),size=(400, 70))
        images.configure(image =manual_24)

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

step_2 = customtkinter.CTkLabel(master = frame,text = "2) Nastavte kritéria třídění nebo ponechte základní nastavení",justify = "left",font=("Arial",20,"bold"))
step_2.pack(pady = 12,padx =10,anchor ="w")

checkbox = customtkinter.CTkCheckBox(master = frame, text = "Třídit podle typů souborů",command = selected)
checkbox.pack(pady =12,padx=10,anchor ="w")
checkbox2 = customtkinter.CTkCheckBox(master = frame, text = "Třídit podle čísla funkce",command = selected2)
checkbox2.pack(pady =12,padx=10,anchor ="w")
checkbox3 = customtkinter.CTkCheckBox(master = frame, text = "Třídit podle čísla kamery",command = selected3)
checkbox3.pack(pady =12,padx=10,anchor ="w")
checkbox4 = customtkinter.CTkCheckBox(master = frame, text = "Třídit podle čísla funkce i kamery",command = selected4)
checkbox4.pack(pady =12,padx=10,anchor ="w")
checkbox5 = customtkinter.CTkCheckBox(master = frame, text = "Manuálně nastavit počet zakrytých znaků pro rozhodování",command = selected5)
checkbox5.pack(pady =12,padx=10,anchor ="w")

#misto pro zobrazovani obrazku
images = customtkinter.CTkLabel(master = frame,text = " ")
images.pack()

#default:
checkbox.select()
view_image(1)

button = customtkinter.CTkButton(master = frame, text = "SPUSTIT", command = start)
button.pack(pady =12,padx=10)




root.mainloop()



