from openpyxl import Workbook
from openpyxl import load_workbook
import time

import customtkinter as ctk
from tkinter import Menu

def on_mouse_wheel(event):
    if event.delta > 0:
        option_menu._dropdown_menu.yposition(0)
    else:
        option_menu._dropdown_menu.yposition(10)

# Create the main window
# root = ctk.CTk()

# # Sample data for the OptionMenu
# options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Option 2", "Option 3", "Option 4", "Option 2", "Option 3", "Option 4", "Option 5", "Option 2", "Option 3", "Option 4", "Option 2", "Option 3", "Option 4", "Option 5", "Option 2", "Option 3", "Option 4", "Option 2", "Option 3", "Option 4", "Option 5", "Option 2", "Option 3", "Option 4", "Option 5", "Option 2", "Option 3", "Option 4", "Option 5", "Option 2", "Option 3", "Option 4", "Option 5", "Option 2", "Option 3", "Option 4", "Option 5", "Option 2", "Option 3", "Option 4", "Option 5", "Option 2", "Option 3", "Option 4", "Option 5"]

# # Create the CTkOptionMenu
# option_menu = ctk.CTkOptionMenu(master=root, values=options,dropdown_font=("Arial",30,"bold"))
# option_menu.pack(pady=20, padx=20)

# def clicked(e):
#     print("clicked")

# option_menu.bind("<Button-1>", clicked)
# option_menu._open_dropdown_menu()
# option_menu._dropdown_menu.bind("<MouseWheel>", lambda e: clicked)
# # .bind("<MouseWheel>", lambda e: clicked)
# # Bind the mouse wheel event to the OptionMenu
# root.bind_all("<MouseWheel>", on_mouse_wheel)

# # Run the main loop
# root.mainloop()

aa = "A5"
print(aa.replace("A","B"))