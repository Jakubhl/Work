import customtkinter

# child_root=customtkinter.CTk()
# # x = self.root.winfo_rootx()
# # y = self.root.winfo_rooty()
# child_root.geometry(f"350x520")  
# child_root.title("Editování optiky: ")
# optic_type =                customtkinter.CTkLabel(master = child_root,text = "Typ objektivu:",font=("Arial",22,"bold"))
# new_name =                  customtkinter.CTkEntry(master = child_root,font=("Arial",22),width=300,height=50,corner_radius=0)
# button_next_st =            customtkinter.CTkButton(master = child_root,text = "Uložit",font=("Arial",22,"bold"),width = 200,height=50,corner_radius=0)
# button_prev_st =            customtkinter.CTkButton(master = child_root,text = "Uložit",font=("Arial",22,"bold"),width = 200,height=50,corner_radius=0)
# alternative_type =          customtkinter.CTkLabel(master = child_root,text = "Alternativa:",font=("Arial",22,"bold"))
# alternative_entry =         customtkinter.CTkOptionMenu(master = child_root,font=("Arial",22),dropdown_font=("Arial",22),width=300,height=50,corner_radius=0)
# note_label =                customtkinter.CTkLabel(master = child_root,text = "Poznámky:",font=("Arial",22,"bold"))
# notes_input =               customtkinter.CTkTextbox(master = child_root,font=("Arial",22),width=300,height=200)
# button_save =               customtkinter.CTkButton(master = child_root,text = "Uložit",font=("Arial",22,"bold"),width = 200,height=50,corner_radius=0,)
# button_continue =           customtkinter.CTkButton(master = child_root,text = "Pokračovat",font=("Arial",22,"bold"),width = 200,height=50,corner_radius=0)
# optic_type                  .pack(pady=(15,5),padx=10,anchor="w",expand=False,side = "top")
# # optic_type_entry            .pack(pady = 5, padx = 10,anchor="w",expand=False,side="top")
# new_name                    .pack(pady = 5, padx = 10,anchor="w",expand=False,side="top")
# button_next_st              .pack(pady = 5, padx = 10,anchor="w",expand=False,side="left")
# button_prev_st              .pack(pady = 5, padx = 10,anchor="w",expand=False,side="left")
# alternative_type            .pack(pady = 5, padx = 10,anchor="w",expand=False,side="top")
# alternative_entry           .pack(pady = 5, padx = 10,anchor="w",expand=False,side="top")
# note_label                  .pack(pady = 5, padx = 10,anchor="w",expand=False,side="top")
# notes_input                 .pack(pady = 5, padx = 10,expand=True,side="top")
# button_save                 .pack(pady = 5, padx = 10,expand=True,side="left",anchor="w")
# button_continue             .pack(pady = 5, padx = 10,expand=True,side="left",anchor="w")


# child_root.mainloop()
import customtkinter

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)
        block_widget =    customtkinter.CTkFrame(master=self,corner_radius=0,height=200,width =400,border_width= 2,border_color="#636363")
        block_widget.     pack(pady = (0,0),padx =0,expand = False,side = "top",anchor="w")
        block_name =      customtkinter.CTkLabel(master = block_widget,text = "ToplevelWindow",font=("Arial",25,"bold"),width=block_widget.cget("width") - 10,height=block_widget.cget("height") - 10,anchor="w")
        block_name.       pack(pady = 5,padx =5)


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")

        self.button_1 = customtkinter.CTkButton(self, text="open toplevel", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=20, pady=20)

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

if __name__ == "__main__":
    app = App()
    app.mainloop()