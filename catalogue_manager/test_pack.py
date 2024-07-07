import customtkinter

import xml.etree.ElementTree as ET

# Example data
stations = [{'name': 'Název stanice', 'inspection_description': '- popis inspekce\n', 'camera_list': "[{'type': '', 'controller': '', 'controller_color': '', 'controller_info': '', 'cable': '', 'optics_list': [{'type': '', 'alternative': '', 'accessory_list': [], 'description': '\\n', 'row_count': 0}], 'description': '\\n', 'row_count': 1}]"}, {'name': 'Název stanicedd', 'inspection_description': '- popis inspekcedd\n', 'camera_list': "[{'type': '', 'controller': 'Kontroler 1  (FH-2050)', 'controller_color': '#1E90FF', 'controller_info': '', 'cable': '', 'optics_list': [{'type': '3Z4S-LE SV-1614H', 'alternative': '3Z4S-LE SV-1614H', 'accessory_list': [{'type': 'HDD', 'dimension': '', 'description': 'dddd\\n'}], 'description': '\\n', 'row_count': 1}], 'description': '\\n', 'row_count': 1}]"}]
# print(stations[0]["camera_list"])


camera_list = stations[0]["camera_list"]
camera_list = camera_list.split(",")
# print(camera_list)

new_camera=[]
new_optics = []
new_accessory = []
optic_array = False
accessory_array = False
for items in camera_list:
    print(items)
    if "optics_list" in items:
        optic_array = True
    if "accessory_list" in items:
        accessory_array = True

    if optic_array and not accessory_array:
        if "optics_list" in items:
            items += ":"
            new_optics.append(items)
        
    elif accessory_array:
        new_accessory.append(items)
    else:
        new_camera.append(items)
# print("")
# print(new_camera)
# print(new_optics)
# print(new_accessory)

def filer_array(array):
    output = []
    for items in array:
        items_splitted = items.split(":")
        forbidden_keys = ["\'","{","}","[","]"," "]
        for objects in items_splitted:
            for keys in forbidden_keys:
                objects = objects.replace(keys,"")

            output.append(objects)
    return output

def make_object(array):
    array = filer_array(array)
    tag_array = []
    value_array = []
    for i in range(0,len(array)):
        if i % 2 == 0:
            tag_array.append(array[i])
        else:
            value_array.append(array[i])
    print("tag",tag_array)
    print("val",value_array)

    new_object = {}
    for i in range(0,len(tag_array)):
        new_object[tag_array[i]] = value_array[i]

    print(new_object)


new_optics = stations[0]["camera_list"].split("[")[1]
make_object(new_camera)
make_object(new_optics)
# make_object(new_accessory)

# new_obj = 

# class ToplevelWindow(customtkinter.CTkToplevel):'
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