import customtkinter

child_root=customtkinter.CTk()
# x = self.root.winfo_rootx()
# y = self.root.winfo_rooty()
child_root.geometry(f"350x520")  
child_root.title("Editování optiky: ")
block_frame =               customtkinter.CTkFrame(master=child_root,fg_color="#181818",height=50,width=200,border_width= 2,corner_radius=0)
controller_name_label =     customtkinter.CTkLabel(master=block_frame,text = "FFFFFFF",height=50,width=200,font=("Arial",22,"bold"),fg_color="green")
block_frame.                pack(fill = "both")

controller_name_label.      pack(pady=5,padx = 5)


child_root.mainloop()
import customtkinter

# class ToplevelWindow(customtkinter.CTkToplevel):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.geometry("400x300")

#         self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
#         self.label.pack(padx=20, pady=20)
#         block_widget =    customtkinter.CTkFrame(master=self,corner_radius=0,height=200,width =400,border_width= 2,border_color="#636363")
#         block_widget.     pack(pady = (0,0),padx =0,expand = False,side = "top",anchor="w")
#         block_name =      customtkinter.CTkLabel(master = block_widget,text = "ToplevelWindow",font=("Arial",25,"bold"),width=block_widget.cget("width") - 10,height=block_widget.cget("height") - 10,anchor="w")
#         block_name.       pack(pady = 5,padx =5)


# class App(customtkinter.CTk):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.geometry("500x400")

#         self.button_1 = customtkinter.CTkButton(self, text="open toplevel", command=self.open_toplevel)
#         self.button_1.pack(side="top", padx=20, pady=20)

#         self.toplevel_window = None

#     def open_toplevel(self):
#         if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
#             self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
#         else:
#             self.toplevel_window.focus()  # if window exists focus it

# if __name__ == "__main__":
#     app = App()
#     app.mainloop()