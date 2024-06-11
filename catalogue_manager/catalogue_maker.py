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
        self.root.after(0, lambda:self.root.state('zoomed'))
        # self.optic_count = []
        # self.camera_count = []
        self.station_list = []


        self.create_main_widgets()

    def clear_frame(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def switch_widget_info(self,args,widget_tier,widget):
        station_index = int(widget_tier[:2])
        if len(widget_tier) == 2: #01-99 stanice
            if widget._text == str(self.station_list[station_index]["inspection_description"]):
                widget.configure(text=str(self.station_list[station_index]["name"]))
            else:
                widget.configure(text=str(self.station_list[station_index]["inspection_description"]))
        
        elif len(widget_tier) == 4: # 0101-9999 kamery
            camera_index = int(widget_tier[2:])
            if widget._text == str(self.station_list[station_index]["camera_list"][camera_index]["type"]):
                details = str(self.station_list[station_index]["camera_list"][camera_index]["controller"]) + "\n"
                details = details + str(self.station_list[station_index]["camera_list"][camera_index]["description"])

                widget.configure(text=details)
            else:
                widget.configure(text=str(self.station_list[station_index]["camera_list"][camera_index]["type"]))

        elif len(widget_tier) == 6: # 010101-999999 optika
            camera_index = int(widget_tier[2:4])
            optic_index = int(widget_tier[4:])
            if widget._text == str(self.station_list[station_index]["camera_list"][camera_index]["optics_list"][optic_index]["type"]):
                details = str(self.station_list[station_index]["camera_list"][camera_index]["optics_list"][optic_index]["alternative"]) + "\n"
                details = details + str(self.station_list[station_index]["camera_list"][camera_index]["optics_list"][optic_index]["description"])
                widget.configure(text=details)
            else:
                widget.configure(text=str(self.station_list[station_index]["camera_list"][camera_index]["optics_list"][optic_index]["type"]))

        elif len(widget_tier) == 8: # 01010101-99999999 prislusenstvi
            camera_index = int(widget_tier[2:4])
            optic_index = int(widget_tier[4:6])
            accessory_index = int(widget_tier[6:])
            if widget._text == str(self.station_list[station_index]["camera_list"][camera_index]["optics_list"][optic_index]["accessory_list"][accessory_index]["type"]):
                details = str(self.station_list[station_index]["camera_list"][camera_index]["optics_list"][optic_index]["accessory_list"][accessory_index]["dimension"]) + "\n"
                details = details + str(self.station_list[station_index]["camera_list"][camera_index]["optics_list"][optic_index]["accessory_list"][accessory_index]["description"])
                widget.configure(text=details)
            else:
                widget.configure(text=str(self.station_list[station_index]["camera_list"][camera_index]["optics_list"][optic_index]["accessory_list"][accessory_index]["type"]))
            
    def make_block(self,master_widget,height,width,fg_color,text,side,dummy_block = False,tier = ""):
        if dummy_block:
            dummy_block_widget =    customtkinter.CTkFrame(master=master_widget,corner_radius=0,height=height,width =width,fg_color="#212121")
            dummy_block_widget.     pack(pady = (0,0),padx =0,expand = False,side = side,anchor="w")
            return dummy_block
        else:
            block_widget =    customtkinter.CTkFrame(master=master_widget,corner_radius=0,fg_color=fg_color,height=height,width =width,border_width= 2,border_color="#636363")
            block_widget.     pack(pady = (0,0),padx =0,expand = False,side = side,anchor="w")
            block_name =      customtkinter.CTkLabel(master = block_widget,text = text,font=("Arial",25,"bold"),height=height-15,width =width-15)
            block_name.       pack(pady = 5,padx =5,anchor="n",expand=False)

            block_widget.bind("<Button-1>",lambda e, widget_tier=tier,widget = block_name: self.switch_widget_info(e, widget_tier,widget))
            block_name.bind("<Button-1>",lambda e, widget_tier=tier,widget = block_name: self.switch_widget_info(e, widget_tier,widget))
            return block_widget
    

    """def widget_info(self,args,widget_tier,btn):
        print(widget_tier)
        station_index = int(widget_tier[:2])
        print(station_index)
        if len(widget_tier) == 2: #01-99 stanice
            if btn == "add_line":
                print("nova stanice")
                self.station_list.append([[1]]) #pridani stanice, pole = kamera a jednou optikou
                self.make_project_widgets()

            elif btn == "add_object":
                print("nova kamera")
                self.station_list[station_index].append([1])
                self.make_project_widgets()
        
        if len(widget_tier) == 4: #0101-9999 kamery
            if btn == "add_object":
                print("nova optika")
                camera_index = int(widget_tier[2:])
                print(camera_index,"cmaera index")
                self.station_list[station_index][camera_index][0] = int(self.station_list[station_index][camera_index][0]) + 1
                self.make_project_widgets()

        print(self.station_list)
"""
    
    def make_new_object(self,which_one,object_to_edit = None,cam_index = None,optic_index = None):
        """
        which_one:
        - station
        - camera
        - optic
        - accessory
        """
        if which_one == "station":
            # accessory = {
            #     "type": "typ prislusenstvi",
            #     "dimension":"rozmery/ velikost",
            #     "description":"pozn",
            # }
            optic = {
                "type": "typ optiky",
                "alternative":"tele",
                "accessory_list": [],
                "description":"hubou mele",
            }
            
            camera = {
                "type": "typ kamery",
                "controller": "kontroler",
                "optics_list": [optic],
                "description": "pozn",
            }
            station = {
                "name": "Název stanice",
                "inspection_description": "blablablabla",
                "camera_list": [camera],
            }

            return station
        
        elif which_one == "camera":
            # accessory = {
            #     "type": "typ prislusenstvi",
            #     "dimension":"rozmery/ velikost",
            #     "description":"pozn",
            # }
            optic = {
                "type": "typ optiky",
                "alternative":"tele",
                "accessory_list": [],
                "description":"hubou mele",
            }
            camera = {
                "type": "typ kamery",
                "controller": "kontroler",
                "optics_list": [optic],
                "description": "pozn",
            }

            object_to_edit["camera_list"].append(camera)
            return object_to_edit
        
        elif which_one == "optic":
            # accessory = {
            #     "type": "typ prislusenstvi",
            #     "dimension":"rozmery/ velikost",
            #     "description":"pozn",
            # }
            optic = {
                "type": "typ optiky",
                "alternative":"tele",
                "accessory_list": [],
                "description":"hubou mele",
            }

            object_to_edit["camera_list"][cam_index]["optics_list"].append(optic)
            return object_to_edit
        
        elif which_one == "accessory":
            accessory = {
                "type": "typ prislusenstvi",
                "dimension":"rozmery/ velikost",
                "description":"pozn",
            }

            object_to_edit["camera_list"][cam_index]["optics_list"][optic_index]["accessory_list"].append(accessory)
            return object_to_edit

    def manage_widgets(self,args,widget_tier,btn):
        station_index = int(widget_tier[:2])
        if len(widget_tier) == 2: #01-99 stanice
            if btn == "add_line": # nova stanice
                new_station = self.make_new_object("station")
                self.station_list.append(new_station)
                self.make_project_widgets()

            elif btn == "add_object": # nova kamera ke stanici 0101-9999 kamery
                station_with_new_camera = self.make_new_object("camera",object_to_edit = self.station_list[station_index])
                self.station_list[station_index] = station_with_new_camera
                self.make_project_widgets()
        
        elif len(widget_tier) == 4: # 0101-9999 kamery, nove bude pridano: 010101-999999 optika
            if btn == "add_object": # nova optika kamery
                camera_index = int(widget_tier[2:])
                camera_with_new_optics = self.make_new_object("optic",object_to_edit = self.station_list[station_index],cam_index = camera_index)
                self.station_list[station_index] = camera_with_new_optics
                self.make_project_widgets()

        elif len(widget_tier) == 6: # 010101-999999 optika, nove bude pridano: 01010101-99999999 prislusenstvi
            if btn == "add_object": # nove prislusenstvi ka kamere
                camera_index = int(widget_tier[2:4])
                optic_index = int(widget_tier[4:])
                camera_with_new_accessoryes = self.make_new_object("accessory",object_to_edit = self.station_list[station_index],cam_index = camera_index,optic_index = optic_index)
                self.station_list[station_index] = camera_with_new_accessoryes
                self.make_project_widgets()

        # print("STATION_LIST: ",self.station_list)
    

    def make_block_buttons(self,master_widget,tier:str,station:bool,accessory=False):#,btn_add_line:str,btn_add_object:str
        button_add_line = customtkinter.CTkButton(master = master_widget, width = 25,height=25,text = "+",font=("",15),corner_radius=0,fg_color="#009933",hover_color="green")
        if station:
            button_add_line.pack(pady = 5, padx = (5,0),anchor="w",expand=False,side="left")
        button_edit_object = customtkinter.CTkButton(master = master_widget,text = "🖌",font=("",15),width = 25,height=25,corner_radius=0)
        button_edit_object.pack(pady = 5, padx = (5,0),anchor="w",expand=False,side="left")
        button_edit_color = customtkinter.CTkButton(master = master_widget,text = "🎨",font=("",15),width = 25,height=25,corner_radius=0)
        button_edit_color.pack(pady = 5, padx = (5,0),anchor="w",expand=False,side="left")
        button_del_object = customtkinter.CTkButton(master = master_widget, width = 25,height=25,text = "×",font=("",15),corner_radius=0,fg_color="#cc0000",hover_color="red")
        button_del_object.pack(pady = 5, padx = (5,0),anchor="w",expand=True,side="left")
        button_add_object = customtkinter.CTkButton(master = master_widget, width = 25,height=25,text = "+",font=("",15),corner_radius=0,fg_color="#009933",hover_color="green")
        if not accessory:
            button_add_object.pack(pady = 5, padx = 5,anchor="e",expand=True,side="left")

        if station:
            button_add_line.bind("<Button-1>",lambda e, widget_tier=tier, btn = "add_line": self.manage_widgets(e, widget_tier,btn))
        if not accessory:
            button_add_object.bind("<Button-1>",lambda e, widget_tier=tier, btn = "add_object": self.manage_widgets(e, widget_tier,btn))
        
        

        master_widget.update()
        # print(master_widget._current_height)

    """def old__create_widgets(self):
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
"""
    
    def create_main_widgets(self):
        self.clear_frame(self.root)
        column_labels =             customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#636363",height=50)
        self.project_tree =         customtkinter.CTkScrollableFrame(master=self.root,corner_radius=0)
        column_labels               .pack(pady=0,padx=5,fill="x",expand=False,side = "top")
        self.project_tree           .pack(pady=5,padx=5,fill="both",expand=True,side = "top")
        stations_column_header =    customtkinter.CTkLabel(master = column_labels,text = "Stanice",font=("Arial",25,"bold"),bg_color="#212121",width=275,height=50)
        stations_column_header      .pack(pady=(15,0),padx=10,expand=False,side = "left")
        camera_column_header =      customtkinter.CTkLabel(master = column_labels,text = "Kamera",font=("Arial",25,"bold"),bg_color="#212121",width=275,height=50)
        camera_column_header        .pack(pady=(15,0),padx=10,expand=False,side = "left")
        optics_column_header =      customtkinter.CTkLabel(master = column_labels,text = "Objektiv",font=("Arial",25,"bold"),bg_color="#212121",width=275,height=50)
        optics_column_header        .pack(pady=(15,0),padx=10,expand=False,side = "left")
        accessory_column_header =   customtkinter.CTkLabel(master = column_labels,text = "Příslušenství",font=("Arial",25,"bold"),bg_color="#212121",width=275,height=50)
        accessory_column_header     .pack(pady=(15,0),padx=10,expand=False,side = "left")
        

        self.project_column =   customtkinter.CTkFrame(master=self.project_tree,corner_radius=0,border_width=0)
        self.project_column     .pack(pady=0,padx=0,fill="y",expand=False,side = "left")
        self.camera_column =    customtkinter.CTkFrame(master=self.project_tree,corner_radius=0,border_width=0)    
        self.camera_column      .pack(pady=0,padx=0,fill="y",expand=False,side = "left")
        self.optic_column =     customtkinter.CTkFrame(master=self.project_tree,corner_radius=0,border_width=0)    
        self.optic_column       .pack(pady=0,padx=0,fill="y",expand=False,side = "left")
        self.accessory_column = customtkinter.CTkFrame(master=self.project_tree,corner_radius=0,border_width=0)    
        self.accessory_column   .pack(pady=0,padx=0,fill="y",expand=False,side = "left")
        self.station_list.append(self.make_new_object("station"))
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

    """def old_make_project_widgets(self):
        self.clear_frame(self.project_column)
        self.clear_frame(self.camera_column)
        self.clear_frame(self.optic_column)
        print(self.station_list)
        for i in range(0,len(self.station_list)):
            # if station_count < 10 ...

            station_tier =  "0" + str(i) #01-99 
            camera_count = len(self.station_list[i])
            station_widget_growth = ((camera_count*100)-100)# + camera_widget_growth

            # rust velikosti widgetu se pocita odzadu
            all_st_optics_count = 0
            for items in self.station_list[i]:
                all_st_optics_count += items[0]
            station_widget_growth = ((all_st_optics_count*100)-100)# + camera_widget_growth

            station_widget = self.make_block(master_widget=self.project_column,height=70+station_widget_growth,width=300,fg_color="black",side = "top",text=station_tier)
            self.make_block_buttons(master_widget=station_widget,tier=station_tier,station=True)

            for x in range(0,camera_count):
                optic_count = self.station_list[i][x][0]
                camera_widget_growth = ((optic_count*100)-100)
                camera_tier =  station_tier + "0" + str(x) #0101-9999
                camera_widget = self.make_block(master_widget=self.camera_column,height=70+camera_widget_growth,width=300,fg_color="black",side = "top",text=camera_tier)
                self.make_block_buttons(master_widget=camera_widget,tier=camera_tier,station=False)


                for y in range(0,optic_count):
                    optic_tier =  camera_tier + "0" + str(y) #010101-999999
                    optic_widget = self.make_block(master_widget=self.optic_column,height=70,width=300,fg_color="black",side = "top",text=optic_tier)
                    self.make_block_buttons(master_widget=optic_widget,tier=optic_tier,station=False)

                    # for z in range(0,optic_count):
                    #     accessory_tier =  optic_tier + "0" + str(z) #01010101-99999999
                    #     accessory_widget = self.make_block(master_widget=self.optic_column,height=70,width=300,fg_color="black",side = "top",text=optic_tier)
                    #     self.make_block_buttons(master_widget=accessory_widget,tier=accessory_tier,station=False)
"""
    
    def check_widget_growth(self,widget:str,station_index,camera_index=None,optics_index=None):
        """
        widget:
        - station
        - camera
        - optics
        """
        all_st_optics_count = 0
        all_st_accessory_count = 0
        if widget == "station":
            # station_camera_list = self.station_list[station_index]["camera_list"]
            # camera_count = len(station_camera_list)
            # station_widget_growth_cam = ((camera_count*100)-100)# + camera_widget_growth
            
            for camera in self.station_list[station_index]["camera_list"]:
                all_st_optics_count += len(camera["optics_list"])
            station_widget_growth_optics = ((all_st_optics_count*100)-100)

            
            for camera in self.station_list[station_index]["camera_list"]:
                for optics in camera["optics_list"]:
                    all_st_accessory_count += len(optics["accessory_list"])
            station_widget_growth_accessory = 0
            if all_st_accessory_count>1:
                station_widget_growth_accessory = ((all_st_accessory_count*100)-100)
            
            # return max(station_widget_growth_cam,station_widget_growth_optics,station_widget_growth_accessory)
            # return max(station_widget_growth_optics,station_widget_growth_accessory)
            return station_widget_growth_optics+station_widget_growth_accessory

        elif widget == "camera":
            all_st_optics_count = len(self.station_list[station_index]["camera_list"][camera_index]["optics_list"])
            station_widget_growth_optics = ((all_st_optics_count*100)-100)

            for optics in self.station_list[station_index]["camera_list"][camera_index]["optics_list"]:
                all_st_accessory_count += len(optics["accessory_list"])

            station_widget_growth_accessory = 0
            if all_st_accessory_count>0:
                station_widget_growth_accessory = ((all_st_accessory_count*100)-100)
            
            # return max(station_widget_growth_optics,station_widget_growth_accessory)
            return station_widget_growth_optics + station_widget_growth_accessory
        
        elif widget == "optics":
            all_st_accessory_count = len(self.station_list[station_index]["camera_list"][camera_index]["optics_list"][optics_index]["accessory_list"])
            station_widget_growth_accessory = ((all_st_accessory_count*100)-100)
            
            station_widget_growth_accessory = 0
            if all_st_accessory_count>0:
                station_widget_growth_accessory = ((all_st_accessory_count*100)-100)
            
            return station_widget_growth_accessory

    def make_project_widgets(self):
        self.clear_frame(self.project_column)
        self.clear_frame(self.camera_column)
        self.clear_frame(self.optic_column)
        self.clear_frame(self.accessory_column)

        # creating stations ------------------------------------------------------------------------------------------------------------------------------
        for i in range(0,len(self.station_list)):
            station_name = self.station_list[i]["name"]
            if i < 10:
                station_tier =  "0" + str(i) #01-99 
            else:
                station_tier =  str(i) #01-99

            station_camera_list = self.station_list[i]["camera_list"]
            camera_count = len(station_camera_list)

            station_widget_growth = self.check_widget_growth("station",station_index=i)
            station_widget = self.make_block(master_widget=self.project_column,height=70+station_widget_growth,width=300,fg_color="#111111",side = "top",text=station_name,tier=station_tier)
            self.make_block_buttons(master_widget=station_widget,tier=station_tier,station=True)
            # creating cameras ------------------------------------------------------------------------------------------------------------------------------
            for x in range(0,camera_count):
                camera_type = station_camera_list[x]["type"]
                station_camera_optic_list = station_camera_list[x]["optics_list"]
                optic_count = len(station_camera_optic_list)
                # camera_widget_growth = ((optic_count*100)-100)
                if x < 10:
                    camera_tier =  station_tier + "0" + str(x) #0101-9999
                else:    
                    camera_tier =  station_tier + str(x) #0101-9999

                camera_widget_growth = self.check_widget_growth("camera",station_index=i,camera_index=x)
                camera_widget = self.make_block(master_widget=self.camera_column,height=70+camera_widget_growth,width=300,fg_color="#111111",side = "top",text=camera_type,tier = camera_tier)
                self.make_block_buttons(master_widget=camera_widget,tier=camera_tier,station=False)

                # creating optics ------------------------------------------------------------------------------------------------------------------------------
                for y in range(0,optic_count):
                    optic_type = station_camera_optic_list[y]["type"]
                    accessory_list = station_camera_optic_list[y]["accessory_list"]
                    accessory_count = len(accessory_list)
                    if y < 10:
                        optic_tier =  camera_tier + "0" + str(y) #010101-999999
                    else:
                        optic_tier =  camera_tier + str(y) #010101-999999

                    optic_widget_growth = self.check_widget_growth("optics",station_index=i,camera_index=x,optics_index=y)
                    optic_widget = self.make_block(master_widget=self.optic_column,height=70+optic_widget_growth,width=300,fg_color="#111111",side = "top",text=optic_type,tier=optic_tier)
                    self.make_block_buttons(master_widget=optic_widget,tier=optic_tier,station=False)

                    # creating accessories ------------------------------------------------------------------------------------------------------------------------------
                    for z in range(0,accessory_count):
                        accessory_type = accessory_list[z]["type"]
                        if z < 10:
                            accessory_tier =  optic_tier + "0" + str(z) #01010101-99999999
                        else:
                            accessory_tier =  optic_tier + str(z) #01010101-99999999

                        accessory_widget = self.make_block(master_widget=self.accessory_column,height=70,width=300,fg_color="#111111",side = "top",text=accessory_type,tier = accessory_tier)
                        self.make_block_buttons(master_widget=accessory_widget,tier=accessory_tier,station=False,accessory=True)
                    if accessory_count == 0:
                        accessory_widget = self.make_block(master_widget=self.accessory_column,height=100,width=300,fg_color="#111111",side = "top",text="",dummy_block=True)
        
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