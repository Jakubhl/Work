import customtkinter
import tkinter as tk
import openpyxl
import xlwings as xw

# customtkinter.set_appearance_mode("dark")
# customtkinter.set_default_color_theme("dark-blue")
# root=customtkinter.CTk()
# root.geometry("1200x900")
# root.title("Catalogue maker v1.0")

class Catalogue_gui:
    def __init__(self):
        # self.root = root
        # self.create_widgets()
        self.excel_file_path = "C:/Users/jakub.hlavacek.local/Desktop/JHV/Work/catalogue_manager/Databáze_po_mém4.xlsx"
        # self.create_widgets_horizontal()
        self.manage_excel()

    def clear_frame(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def make_block(self,master_widget,height,width,fg_color,text,side):
        station_widget =    customtkinter.CTkFrame(master=master_widget,corner_radius=0,fg_color=fg_color,height=height,width =width,border_width= 2,border_color="white")
        # station_widget.   grid(column = 0,row=0,pady = (10,0),padx =0,sticky = tk.W)
        station_widget.     pack(pady = (0,0),padx =0,expand = True,side = side,anchor="w")

        # station_widget.   grid_propagate(0)
        # canvas =            customtkinter.CTkCanvas(master = station_widget,height=height-10,width =width-10)
        # text_ID = canvas.create_text(5, 5, anchor="nw", angle=90,text = text,font=("Arial",20,"bold"))
        # canvas.       pack(pady = 5,padx =5,anchor="n",expand=True)
        # canvas.tag_raise(text_ID)
        
        station_name =      customtkinter.CTkLabel(master = station_widget,text = text,font=("Arial",20,"bold"),height=height-15,width =width-15)
        # # station_name.     grid(column = 0,row=0,pady = (10,0),padx =10,sticky = tk.NSEW)
        station_name.       pack(pady = 5,padx =5,anchor="n",expand=True)
        return station_widget

    def create_widgets(self):
        self.clear_frame(self.root)
        menu_cards =            customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#636363",height=50)
        main_widgets =          customtkinter.CTkFrame(master=self.root,corner_radius=0)
        self.project_tree =     customtkinter.CTkScrollableFrame(master=self.root,corner_radius=0)
        menu_cards              .pack(pady=0,padx=5,fill="x",expand=False,side = "top")
        # main_widgets            .pack(pady=0,padx=5,fill="x",expand=False,side = "top")
        self.project_tree       .pack(pady=5,padx=5,fill="both",expand=True,side = "top")
        # project_tree.grid(column = 0,row=0,pady = 5,padx =10,sticky = tk.W)

        station1_widget = self.make_block(master_widget=self.project_tree,height=50,width=300,fg_color="blue",text="St 010",side = "top")
        controler1 = self.make_block(master_widget=station1_widget,height=50,width=290,fg_color="white",side="left",text="Kontroler 1\n(FH-2050)")
        camera1 = self.make_block(master_widget=controler1,height=50,width=290,fg_color="gray",side="left",text="Kamera1\n(FH-SC02)")
        self.make_block(master_widget=camera1,height=50,width=280,fg_color="black",side="top",text="kabel\n10 m")
        camera2 = self.make_block(master_widget=controler1,height=50,width=290,fg_color="gray",side="left",text="Kamera2\n(FH-SC02)")
        self.make_block(master_widget=camera2,height=50,width=280,fg_color="black",side="top",text="Optika\nxxxxxx")
        self.make_block(master_widget=camera2,height=50,width=280,fg_color="black",side="top",text="kabel\n100 m")
        self.make_block(master_widget=camera2,height=50,width=280,fg_color="black",side="top",text="drzak\nxxxxxx")

        controler2 = self.make_block(master_widget=station1_widget,height=50,width=290,fg_color="white",side="left",text="Kontroler 2\n(FH-2050)")
        self.make_block(master_widget=controler2,height=50,width=290,fg_color="gray",side="top",text="Kamera1\n(FH-SC02)")
        self.make_block(master_widget=controler2,height=50,width=290,fg_color="gray",side="top",text="Kamera2\n(FH-SC02)")

        station2_widget = self.make_block(master_widget=self.project_tree,height=50,width=300,fg_color="blue",text="St 020",side = "top")
        controler1 = self.make_block(master_widget=station2_widget,height=50,width=290,fg_color="white",side="left",text="Kontroler 1\n(FH-2050)")
        self.make_block(master_widget=controler1,height=50,width=290,fg_color="gray",side="top",text="Kamera3\n(FH-SC02)")

        controler2 = self.make_block(master_widget=station2_widget,height=50,width=290,fg_color="white",side="left",text="Kontroler 2\n(FH-2050)")
        self.make_block(master_widget=controler2,height=50,width=290,fg_color="gray",side="top",text="konzole\n(xxxx)")

        def maximalize_window(e):
            self.root.update_idletasks()
            current_width = int(self.root.winfo_width())
            # netrigguj fullscreen zatimco pisu do vstupniho textovyho pole
            if self.focused_entry_widget(): # pokud nabindovane pismeno neni vepisovano do entry widgetu
                return
            if int(current_width) > 1200:
                #self.root.after(0, lambda:self.root.state('normal'))
                self.root.state('normal')
                self.root.geometry(f"260x500+{0}+{0}")
                # self.root.geometry("210x500")
                self.save_setting_parameter(parameter="change_def_window_size",status=2)
            elif int(current_width) ==260:
                self.root.geometry("1200x900")
                self.save_setting_parameter(parameter="change_def_window_size",status=0)
            else:
                #self.root.after(0, lambda:self.root.state('zoomed'))
                self.root.state('zoomed')
                self.save_setting_parameter(parameter="change_def_window_size",status=1)

        self.root.bind("<f>",lambda e: maximalize_window(e))
    def create_widgets_horizontal(self):
        self.clear_frame(self.root)
        menu_cards =            customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#636363",height=50)
        self.project_tree =     customtkinter.CTkScrollableFrame(master=self.root,corner_radius=0)
        menu_cards              .pack(pady=0,padx=5,fill="x",expand=False,side = "top")
        self.project_tree       .pack(pady=5,padx=5,fill="both",expand=True,side = "top")

        self.make_block(master_widget=self.project_tree,height=400,width=300,fg_color="black",side = "left",text="St 010")
        self.make_block(master_widget=self.project_tree,height=200,width=300,fg_color="black",side = "top",text="kontola založení")
        self.make_block(master_widget=self.project_tree,height=200,width=300,fg_color="black",side = "left",text="kontrola podložení")
        self.make_block(master_widget=self.project_tree,height=100,width=300,fg_color="black",side = "top",text="typ kamery\nkontroler")
        self.make_block(master_widget=self.project_tree,height=100,width=300,fg_color="black",side = "left",text="typ kamery\nkontroler")
        self.make_block(master_widget=self.project_tree,height=50,width=300,fg_color="black",side = "top",text="kabel\n10 m")
        self.make_block(master_widget=self.project_tree,height=50,width=300,fg_color="black",side = "left",text="prislusenstvi2")


        

        def maximalize_window(e):
            self.root.update_idletasks()
            current_width = int(self.root.winfo_width())
            # netrigguj fullscreen zatimco pisu do vstupniho textovyho pole
            if self.focused_entry_widget(): # pokud nabindovane pismeno neni vepisovano do entry widgetu
                return
            if int(current_width) > 1200:
                #self.root.after(0, lambda:self.root.state('normal'))
                self.root.state('normal')
                self.root.geometry(f"260x500+{0}+{0}")
                # self.root.geometry("210x500")
                self.save_setting_parameter(parameter="change_def_window_size",status=2)
            elif int(current_width) ==260:
                self.root.geometry("1200x900")
                self.save_setting_parameter(parameter="change_def_window_size",status=0)
            else:
                #self.root.after(0, lambda:self.root.state('zoomed'))
                self.root.state('zoomed')
                self.save_setting_parameter(parameter="change_def_window_size",status=1)

        self.root.bind("<f>",lambda e: maximalize_window(e))

    def manage_excel(self):
       # Create a new Excel workbook and select the active sheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sheet1"

        # Define the initial content of the target cell
        ws["A1"] = "Original Text"

        # Save the workbook
        wb.save("example.xlsx")

        # Open the workbook with xlwings to add VBA code
        try:
            app = xw.App(visible=False)
            wb_xlwings = app.books.open("example.xlsx")
            ws_xlwings = wb_xlwings.sheets['Sheet1']
            
            # Add VBA code to the workbook
            vba_code = """
            Private Sub Worksheet_SelectionChange(ByVal Target As Range)
                Dim cell As Range
                Set cell = Range("A1")
                
                If Not Intersect(Target, cell) Is Nothing Then
                    If cell.Value = "Original Text" Then
                        cell.Value = "New Text"
                    Else
                        cell.Value = "Original Text"
                    End If
                End If
            End Sub
            """

            # Insert VBA code into the worksheet module
            ws_vba = wb_xlwings.api.VBProject.VBComponents(ws_xlwings.name).CodeModule
            ws_vba.DeleteLines(1, ws_vba.CountOfLines)  # Clear existing code
            ws_vba.AddFromString(vba_code)

            # Save and close the workbook
            wb_xlwings.save()
            wb_xlwings.close()
        finally:
            app.quit()



Catalogue_gui()

# root.mainloop()