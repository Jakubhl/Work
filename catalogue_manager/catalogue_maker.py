import customtkinter
import tkinter as tk
import openpyxl
from openpyxl import load_workbook
import xlwings as xw
from openpyxl.worksheet.copier import WorksheetCopy

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root=customtkinter.CTk()
root.geometry("1200x900")
root.title("Catalogue maker v1.0")

class Catalogue_gui:
    def __init__(self,root):
        self.root = root
        self.station_count = 1
        self.camera_count = 2
        self.widget_count = [[1,1]]


        self.create_widgets_horizontal()

    def clear_frame(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def make_block(self,master_widget,height,width,fg_color,text,side):
        station_widget =    customtkinter.CTkFrame(master=master_widget,corner_radius=0,fg_color=fg_color,height=height,width =width,border_width= 2,border_color="white")
        station_widget.     pack(pady = (0,0),padx =0,expand = False,side = side,anchor="w")
        station_name =      customtkinter.CTkLabel(master = station_widget,text = text,font=("Arial",25,"bold"),height=height-15,width =width-15)
        station_name.       pack(pady = 5,padx =5,anchor="n",expand=False)
        return station_widget
    

    def widget_info(self,args,widget_tier,btn):
        print(widget_tier)
        station_index = int(widget_tier[:2])
        if len(widget_tier) == 2: #01-99 stanice
            if btn == "add_line":
                print("nova stanice")
                self.widget_count.append([1,1])
                self.make_project_widgets()

            elif btn == "add_object":
                print("nova kamera")
                self.widget_count[station_index][0] = self.widget_count[station_index][0] + 1
                self.make_project_widgets()
        
        if len(widget_tier) == 4: #0101-9999 kamery
            if btn == "add_line":
                print("nova kamera")
                self.widget_count[station_index][0] = self.widget_count[station_index][0] + 1
                self.make_project_widgets()

            elif btn == "add_object":
                print("nova optika")
                self.widget_count[station_index][1] = self.widget_count[station_index][1] + 1
                self.make_project_widgets()

        print(self.widget_count)


    def make_block_buttons(self,master_widget,tier):#,btn_add_line:str,btn_add_object:str
        button_add_line = customtkinter.CTkButton(master = master_widget, width = 25,height=25,text = "+",font=("Arial",15,"bold"),corner_radius=0,fg_color="green")
        button_add_line.pack(pady = 5, padx = 5,anchor="w",expand=True,side="left")

        button_add_object = customtkinter.CTkButton(master = master_widget, width = 25,height=25,text = "+",font=("Arial",15,"bold"),corner_radius=0,fg_color="green")
        button_add_object.pack(pady = 5, padx = 5,anchor="e",expand=True,side="left")

        button_add_line.bind("<Button-1>",lambda e, widget_tier=tier, btn = "add_line": self.widget_info(e, widget_tier,btn))
        button_add_object.bind("<Button-1>",lambda e, widget_tier=tier, btn = "add_object": self.widget_info(e, widget_tier,btn))

        master_widget.update()
        # print(master_widget._current_height)

    def create_widgets(self):
        self.clear_frame(self.root)
        menu_cards =            customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#636363",height=50)
        main_widgets =          customtkinter.CTkFrame(master=self.root,corner_radius=0)
        self.project_tree =     customtkinter.CTkScrollableFrame(master=self.root,corner_radius=0)
        menu_cards              .pack(pady=0,padx=5,fill="x",expand=False,side = "top")
        # main_widgets          .pack(pady=0,padx=5,fill="x",expand=False,side = "top")
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

        self.project_column =   customtkinter.CTkFrame(master=self.project_tree,corner_radius=0,border_width=0)
        self.project_column     .pack(pady=0,padx=0,fill="y",expand=False,side = "left")
        self.camera_column =    customtkinter.CTkFrame(master=self.project_tree,corner_radius=0,border_width=0)    
        self.camera_column      .pack(pady=0,padx=0,fill="y",expand=False,side = "left")
        self.optic_column =     customtkinter.CTkFrame(master=self.project_tree,corner_radius=0,border_width=0)    
        self.optic_column       .pack(pady=0,padx=0,fill="y",expand=False,side = "left")
        # station_widget = self.make_block(master_widget=self.project_tree,height=70,width=300,fg_color="black",side = "top",text="St 010")
        # self.make_block_buttons(master_widget=station_widget,tier=1)
    
        # self.make_block(master_widget=self.project_tree,height=200,width=300,fg_color="black",side = "top",text="kontola založení")
        # self.make_block(master_widget=self.project_tree,height=200,width=300,fg_color="black",side = "left",text="kontrola podložení")
        # self.make_block(master_widget=self.project_tree,height=100,width=300,fg_color="black",side = "top",text="typ kamery\nkontroler")
        # self.make_block(master_widget=self.project_tree,height=100,width=300,fg_color="black",side = "left",text="typ kamery\nkontroler")
        # self.make_block(master_widget=self.project_tree,height=50,width=300,fg_color="black",side = "top",text="kabel\n10 m")
        # self.make_block(master_widget=self.project_tree,height=50,width=300,fg_color="black",side = "left",text="prislusenstvi2")
        self.make_project_widgets()
        

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

    def make_project_widgets(self):
        self.clear_frame(self.project_column)
        self.clear_frame(self.camera_column)
        self.clear_frame(self.optic_column)



        for i in range(0,len(self.widget_count)):
            # if station_count < 10 ...
            station_tier =  "0" + str(i) #01-99

            

            optic_count = self.widget_count[i][1]
            camera_widget_growth = ((optic_count*100)-100)

            camera_count = self.widget_count[i][0]
            station_widget_growth = ((camera_count*100)-100) + camera_widget_growth

            station_widget = self.make_block(master_widget=self.project_column,height=70+station_widget_growth,width=300,fg_color="black",side = "top",text=station_tier)
            self.make_block_buttons(master_widget=station_widget,tier=station_tier)

            for x in range(0,camera_count):
                camera_tier =  station_tier + "0" + str(x) #0101-9999
                camera_widget = self.make_block(master_widget=self.camera_column,height=70+camera_widget_growth,width=300,fg_color="black",side = "top",text=camera_tier)
                self.make_block_buttons(master_widget=camera_widget,tier=camera_tier)

                for y in range(0,optic_count):
                    optic_tier =  camera_tier + "0" + str(y) #010101-999999
                    camera_widget = self.make_block(master_widget=self.optic_column,height=70,width=300,fg_color="black",side = "top",text=optic_tier)
                    self.make_block_buttons(master_widget=camera_widget,tier=optic_tier)

class Manage_excel:
    def __init__(self):
        # self.change_vba_script()
        pass

    def merge_cells(self,sheet_name:str,file_path:str,cell_range:str):
        """
        cell range format: A1:A2
        """
        wb = load_workbook(filename=file_path, read_only=False, keep_vba=True)
        ws = wb["Sheet1"]

        # Merge cells
        ws.merge_cells('A1:A2')  # Merge cells A1 to B2
        # ws['A1'] = 'Merged Cells'  # Add content to the merged cells

        # Save the workbook
        wb.save(filename='formular2.xlsm')
        wb.close()

    def update_sheet_vba_code(self,file_path, sheet_name, new_code):
        app = xw.App(visible=False)
        wb = app.books.open(file_path)
        vb_project = wb.api.VBProject
        sheet = wb.sheets[sheet_name]
        code_module = vb_project.VBComponents(sheet.name).CodeModule
        code_module.DeleteLines(1, code_module.CountOfLines)
        code_module.AddFromString(new_code)
        wb.save()
        wb.close()
        app.quit()

    def change_vba_script(self):
       # Create a new Excel workbook and select the active sheet

        # Define the VBA code to be added
        sheet_name="Sheet1"
        file_path="formular2.xlsm"
        vba_code = """
        Private Sub Worksheet_BeforeRightClick(ByVal Target As Range, Cancel As Boolean)
            ' Define the cell you chraplavý kašel want to toggle
            Dim targetCell As Range
            Set targetCell = Me.Range("A1") ' Change "A1" to the cell reference you want to toggle

            ' Read text values from hidden worksheet
            Dim text1 As String
            Dim text2 As String
            text1 = Worksheets("HiddenSheet").Range("AAA1").Value
            text2 = Worksheets("HiddenSheet").Range("AAA2").Value

            ' Read toggle status from hidden worksheet
            Dim toggle_status As Integer
            toggle_status = Worksheets("HiddenSheet").Range("AAA3").Value

            ' Check if the right-clicked cell is the target cell
            If Not Intersect(Target, targetCell) Is Nothing Then
                ' Toggle the cell value
                If toggle_status = 1 Then
                    Worksheets("HiddenSheet").Range("AAA1").Value = targetCell.Value
                    targetCell.Value = text2
                    toggle_status = 0
                Else
                    Worksheets("HiddenSheet").Range("AAA2").Value = targetCell.Value
                    targetCell.Value = text1
                    toggle_status = 1
                End If

                ' Update toggle status on hidden worksheet
                Worksheets("HiddenSheet").Range("AAA3").Value = toggle_status
                ' Cancel the default right-click menu
                Cancel = True
            End If
        End Sub
        """

        self.update_sheet_vba_code(file_path, sheet_name, new_code=vba_code)



Catalogue_gui(root)
# Manage_excel()

root.mainloop()