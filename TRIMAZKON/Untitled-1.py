
import customtkinter
import tkinter as tk
from PIL import Image
import psutil
import socket
import threading
import time
import os
import time
import ctypes
import sys
import re


import ctypes
import subprocess
import sys
import time
# customtkinter.set_appearance_mode("dark")
# customtkinter.set_default_color_theme("dark-blue")
# root=customtkinter.CTk()
# root.geometry("1200x900")
# root.state("zoomed")
# root.title("TRIMAZKON v_3.6.2")
# # Configure the column to allow the label to expand horizontally
# project_tree =     customtkinter.CTkScrollableFrame(master=root,corner_radius=0)
# project_tree.      pack(pady=5,padx=5,fill="both",expand=True,side = "top")
# column1 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "Projekt: ",font=("Arial",20,"bold"))
# column2 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "IPv4 adresa: ",font=("Arial",20,"bold"))
# column3 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "Poznámky: ",font=("Arial",20,"bold"))
# column1.pack(pady = 5,padx =10,side = "left",anchor = "n",expand = True)
# column2.pack(pady = 5,padx =10,side = "left",anchor = "n",expand = True)
# column3.pack(pady = 5,padx =10,side = "left",anchor = "n",expand = True)
# column1 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "Projekt: ",font=("Arial",20,"bold"))
# column2 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "IPv4 adresa: ",font=("Arial",20,"bold"))
# column3 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "Poznámky: ",font=("Arial",20,"bold"))
# column1.pack(pady = 5,padx =10,side = "top",anchor = "s",expand = False)
# column2.pack(pady = 5,padx =10,side = "left",anchor = "s",expand = True)
# column3.pack(pady = 5,padx =10,side = "left",anchor = "s",expand = True)

# string = "RESULT: b'\r\nWindows IP Configuration\r\n\r\n\r\nEthernet adapter Ethernet 5:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n\r\nWireless LAN adapter P\xfdipojen\xa1 k m\xa1stn\xa1 s\xa1ti* 1:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n\r\nWireless LAN adapter P\xfdipojen\xa1 k m\xa1stn\xa1 s\xa1ti* 2:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n\r\nEthernet adapter Ethernet 2:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n\r\nWireless LAN adapter Wi-Fi:\r\n\r\n   Connection-specific DNS Suffix  . : \r\n   IPv6 Address. . . . . . . . . . . : 2a00:11b1:1080:128d:6697:34a9:cb75:cfcb\r\n   Temporary IPv6 Address. . . . . . : 2a00:11b1:1080:128d:cd97:8ea1:3d4f:3b33\r\n   Link-local IPv6 Address . . . . . : fe80::541d:930c:6cbc:7daf%10\r\n   IPv4 Address. . . . . . . . . . . : 192.168.48.52\r\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\r\n   Default Gateway . . . . . . . . . : fe80::3c4c:4eff:fe6f:a9d1%10\r\n                                       192.168.48.208\r\n\r\nEthernet adapter Ethernet:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n'"
# # root.mainloop()
# ipv4_pattern = re.compile(r'IPv4 Address[.\s]*: ([\d.]+)')
# # Dictionary to store interface names and their IPv4 addresses
# ipv4_addresses = []
# # Split the output by lines
# lines = string.splitlines()
# # lines = result2.splitlines()
# current_interface = None
# # Iterate over each line to find interface names and IPv4 addresses
# for line in lines:
#     if line.strip():
#         # Detect interface name
#         if line[0].isalpha():
#             current_interface = line.strip()
#         else:
#             # Detect IPv4 address for the current interface
#             match = ipv4_pattern.search(line)
#             if match and current_interface:
#                 ipv4_addresses.append(current_interface)
#                 ipv4_addresses.append(match.group(1))
#                 print(current_interface,match.group(1))
#                 #ipv4_addresses[current_interface] = match.group(1)
# def filter_input(data):
#     forbidden_formats = [".","xml","xlsm","xlsx"]
#     for formats in forbidden_formats:
#         data = data.replace(formats,"")
#     print(data)
#     return data
# filter_input("blabla.xlsm")
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk

class DrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw Circles and Lines")
        # self.root.state("zoomed")

        # Create canvas
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(expand=True,fill="both")
        self.canvas.update()
        self.canvas.update_idletasks()
        self.max_width = self.canvas.winfo_width()
        self.max_height = self.canvas.winfo_height()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.zoom = 1
        self.previous_zoom = 1
        self.draw_mode = "line"  # or "circle"
        self.start_x = None
        self.start_y = None
        self.last_image_x = 0
        self.last_image_y = 0
        self.previous_zoomed_x = 0
        self.previous_zoomed_y = 0
        self.file_list = []
        for files in os.listdir("images"):
            self.file_list.append(files)
        self.image_increment = 0

        self.btn_line = tk.Button(root, text="Draw Line", command=self.set_draw_mode_line)
        self.btn_line.pack(side=tk.LEFT)
        self.btn_circle = tk.Button(root, text="Draw Circle", command=self.set_draw_mode_circle)
        self.btn_circle.pack(side=tk.LEFT)

        def next_image(e):

            if self.image_increment < len(self.file_list):
                self.image_increment+=1
                self.show_image()

        def previous_image(e):
            if self.image_increment > 0:
                self.image_increment-=1
                self.show_image()

        def zoom_image(e):
            zoom_increment = 0.5
            step_increment = 200
            
    
            self.previous_zoom = self.zoom 
            direction = -e.delta
            if direction < 0:
                if int(self.image_width*(self.zoom+zoom_increment)) < self.max_width:
                    self.last_image_x = 0
                    self.show_image()
                    return
                self.zoom += zoom_increment
            else:
                if int(self.image_width*(self.zoom-zoom_increment)) < self.max_width:
                    self.last_image_x = 0
                    self.show_image()
                    return
                self.zoom -= zoom_increment

            previous_dimensions = self.max_width*self.previous_zoom 
            current_dimensions = self.max_width*self.zoom
            image_growth = abs(current_dimensions - previous_dimensions)
            print(image_growth)

            if e.x <= self.max_width/2:
                mouse_pos_x = 1-(e.x/(self.max_width/2))/2
            elif e.x >= self.max_width/2:
                mouse_pos_x = -((e.x/(self.max_width/2))/2)

            if e.y <= self.max_height/2:
                mouse_pos_y= 1-(e.y/(self.max_height/2))/2
            elif e.y >= self.max_height/2:
                mouse_pos_y = -((e.y/(self.max_height/2))/2)

            print("mosuee",mouse_pos_y)

            if direction < 0:  # Zooming in
                # step_size = (step_increment * (mouse_pos_x/100)) + image_growth/2
                step_size = (image_growth/2 * (mouse_pos_x/100))
            else:  # Zooming out
                step_size = -(step_increment * (mouse_pos_x/100)) + image_growth/2

            # if direction < 0:
            #     step_size = ((step_increment)) + ((step_increment)* (mouse_pos_x/100))
            # else:
            #     step_size = -(((step_increment)) + ((step_increment)* (mouse_pos_x/100)))

            # print("step size: ",step_size)
            # # step_size = 120 * (self.zoom/2)
            # # step_size = (mouse_pos_x/100)*(image_growth/2)
            # # step_size = mouse_pos_x + image_growth/2

            # if direction < 0:
                #--------priblizuju s kurzorem napravo--------
            minus_x_boundary = -self.image_width*self.zoom + self.max_width

            
            if e.x > self.image_width/2 + 0.1*self.max_width:
                print("zoom right")
                if (self.last_image_x - step_size) > minus_x_boundary:
                    if (self.last_image_x - step_size) < 0:
                        self.last_image_x -= step_size
                    else:
                        self.last_image_x = 0
                else:
                    self.last_image_x = minus_x_boundary

            #--------priblizuju s kurzorem nalevo--------
            elif e.x < self.image_width/2 - 0.1*self.max_width:
                print("zoom left")
                if self.last_image_x + step_size < 0:
                    if self.last_image_x+ step_size > minus_x_boundary:
                        self.last_image_x += step_size
                    else:
                        self.last_image_x = minus_x_boundary
                else:
                    self.last_image_x = 0

            # --------priblizuju s kurzorem uprostřed--------
            elif e.x < self.image_width/2 or e.x > self.image_width/2:
                if direction <0:
                    print("zoom center in")
                    if self.last_image_x - image_growth/2 > minus_x_boundary:
                        self.last_image_x -= image_growth/2
                    else:
                        self.last_image_x = minus_x_boundary

                else:
                    print("zoom center out")
                    if (self.last_image_x + image_growth/2) < 0.0:
                        self.last_image_x += image_growth/2
                    else:
                        self.last_image_x = 0


            # else:
            #     step_size = (100*self.zoom + mouse_pos_x)
            #     #--------oddaluju s kurzorem napravo--------
            #     if e.x > self.image_width/2 + 0.1*self.max_width:
            #         print("right")
            #         minus_x_boundary = -self.image_width*self.zoom + self.max_width
            #         if (self.last_image_x - step_size) > minus_x_boundary:
            #             self.last_image_x -= step_size
            #         else:
            #             self.last_image_x = minus_x_boundary
                        
            #     #--------oddaluju s kurzorem nalevo--------
            #     elif e.x < self.image_width/2 - 0.1*self.max_width:
            #         print("left")

            #         if (self.last_image_x+step_size) > 0:
            #             self.last_image_x = 0
            #         else:
            #             self.last_image_x += step_size

            #     #--------oddaluju s kurzorem uprostřed--------
            #     elif e.x < self.image_width/2 or e.x > self.image_width/2:
            #         print("center")
            #         self.last_image_x += image_growth/2

            self.show_image()

        self.root.bind("<Right>",next_image)
        self.root.bind("<Left>",previous_image)
        self.root.bind("<MouseWheel>",zoom_image)
        self.show_image()

    
    def show_image(self):
        self.image = Image.open("images/"+self.file_list[self.image_increment])
        # print("image size: ",self.image.size)

        self.canvas.update()
        self.canvas.update_idletasks()

        self.image_width, image_height = self.image.size
        if self.image_width > image_height:
            image_ration = self.image_width/image_height
        self.image_width = self.max_width
        image_height = int(self.image_width/image_ration) 

        self.zoomed_width = int(self.image_width*self.zoom)
        self.zoomed_height = int(image_height*self.zoom)
        self.previous_zoomed_x = int(self.image_width*self.previous_zoom)
        self.previous_zoomed_y = int(image_height*self.previous_zoom)

        resized = self.image.resize(size=(self.zoomed_width, self.zoomed_height))
        self.tk_image = ImageTk.PhotoImage(resized)

        self.image_id = self.canvas.create_image(self.last_image_x, self.last_image_y, anchor=tk.NW, image=self.tk_image,tag = "lower")
        self.canvas.tag_lower(self.image_id)

        print("frame dim: ",self.canvas.winfo_width(),self.canvas.winfo_height())
        print("zoomed dim: ",self.zoomed_width,self.zoomed_height)
        print("new image size: ",self.image_width,image_height)

    def set_draw_mode_line(self):
        self.draw_mode = "line"

    def set_draw_mode_circle(self):
        self.draw_mode = "circle"

    def on_click(self, event):
        # Save the start position
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        # Clear the canvas (if you want to see only the final shape)
        self.canvas.delete("temp_shape")

        if self.draw_mode == "line":
            # Draw a line from the start position to the current position
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="black", tags="temp_shape")
        elif self.draw_mode == "circle":
            # Draw an oval (circle) based on the start position and current position
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline="black", tags="temp_shape")

    def on_release(self, event):
        # Finalize the shape
        self.canvas.delete("temp_shape")

        if self.draw_mode == "line":
            # Draw the final line
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="black")
        elif self.draw_mode == "circle":
            # Draw the final circle
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline="black")

# Create the main window and run the application
# root = tk.Tk()
# app = DrawApp(root)
# root.mainloop()
# config = customtkinter.CTkScrollableFrame.configure()
# print(config)

# for i in range(10,16):
#     print(i)
#     if str(i).isdigit():
#         print("ano")

# def filter_unwanted_chars(to_filter_data, directory = False):
#     unwanted_chars = ["\n","\"","\'","[","]"]
#     if directory:
#         unwanted_chars = ["\n","\"","\'","[","]","\\","/"]
#     # for chars in unwanted_chars:
#     filtered_data = ""
#     for letters in to_filter_data:
#         if letters not in unwanted_chars:
#             filtered_data += letters
#     return filtered_data

# data = r"['bmp', 'png']"
# new_data = filter_unwanted_chars(data)
# print(new_data)

image_paths = [r"C:/Users/jakub.hlavacek.local/Desktop/Screenshot 2024-09-23 135409.png",r"C:\Users\jakub.hlavacek.local\Desktop\JHV\W",r"C:\Users\jakub.hlavacek.local\Desktop\JHV\W"]
print(image_paths[0].split("/")[-1])
noname = image_paths[0].replace(str(image_paths[0].split("/")[-1]),"")
print(noname)
