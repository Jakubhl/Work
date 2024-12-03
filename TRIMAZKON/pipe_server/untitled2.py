
import customtkinter
import psutil 
import os
import pywintypes

import win32pipe
import win32file
import threading
import time
import tkinter as tk

class system_pipeline_communication:
    def __init__(self,root):
        self.root = root
        self.current_pid = None
        self.start_server()

    def server(self,pipe_input):
        pipe_name = fr'\\.\pipe\{pipe_input}'
        while True:
            print(f"Waiting for a client to connect on {pipe_name}...") 
            pipe = win32pipe.CreateNamedPipe(
                pipe_name,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1,
                512,
                512,
                0,
                None
            )

            win32pipe.ConnectNamedPipe(pipe, None)
            print("Client connected.")

            try:
                while True:
                    hr, data = win32file.ReadFile(pipe, 64 * 1024)
                    received_data = data.decode()
                    print(f"Received: {received_data}")
                    self.root.after(0,draw.command_landed,received_data)

            except pywintypes.error as e:
                if e.args[0] == 109:  # ERROR_BROKEN_PIPE
                    print("Client disconnected.")
            finally:
                # Close the pipe after disconnection
                win32file.CloseHandle(pipe)
            # Loop back to wait for new client connections

    def client(self,pipe_name_given,command):
        time.sleep(1)  # Wait for the server to start
        pipe_name = fr'\\.\pipe\{pipe_name_given}'
        handle = win32file.CreateFile(
            pipe_name,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )

        print("Connected to server.")
        if command == "green":
            message = "nastav zelenou"
        elif command == "red":
            message = "nastav cervenou"

        win32file.WriteFile(handle, message.encode())
        print("Message sent.")

    def start_server(self):
        self.current_pid = os.getpid()
        self.pipe_name = f"mypipe_{self.current_pid}"
        running_server = threading.Thread(target=self.server, args=(self.pipe_name,), daemon=True)
        running_server.start()
        
    def get_all_app_processes(self):
        pid_list = []
        num_of_apps = 0
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == "TRIMAZKON_test.exe":
                pid_list.append(process.info['pid'])
                num_of_apps+=1
        
        return [num_of_apps,pid_list]

    def call_checking(self,command):
        checking = self.get_all_app_processes()
        print("SYSTEM application processes: ",checking)
        # if it is running more then one application, execute
        if checking[0]>1:
            pid_list = checking[1]
            # try to send command to every process which has application name
            for pids in pid_list:
                if pids != self.current_pid:
                    try:
                        pipe_name = f"mypipe_{pids}"
                        self.client(pipe_name,command)
                    except Exception:
                        pass

# root = tk.Tk()
# root.withdraw()
# pipeline_duplex = system_pipeline_communication(root)


class drawing_option_window:
    def __init__(self,root,pipe_name):
        self.root = root
        self.pipe_name = pipe_name
        self.create_widgets()

    def close_window(self,window):
        window.destroy()
    
    def rgb_to_hex(self,rgb,one_color = False):
        if not one_color:
            return "#%02x%02x%02x" % rgb
        elif one_color == "red":
            return ("#%02x" % rgb) + "0000"
        elif one_color == "green":
            return "#00" + ("%02x" % rgb) + "00"
        elif one_color == "blue":
            return "#0000" + ("%02x" % rgb)
        
    def hex_to_rgb(self,hex_color):
        # Remove the '#' character if present
        hex_color = hex_color.lstrip('#')
        # Convert the hex string into RGB tuple
        return list(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def update_color(self,*args):
        red = int(self.color_R.get())
        red_hex = self.rgb_to_hex(red,one_color="red")
        self.current_color_val.configure(text = str(red))
        self.color_R.configure(progress_color = red_hex,button_color = red_hex,button_hover_color = red_hex)

        green = int(self.color_G.get())
        green_hex = self.rgb_to_hex(green,one_color="green")
        self.current_color_val2.configure(text = str(green))
        self.color_G.configure(progress_color = green_hex,button_color = green_hex,button_hover_color = green_hex)

        blue = int(self.color_B.get())
        blue_hex = self.rgb_to_hex(blue,one_color="blue")
        self.current_color_val3.configure(text = str(blue))
        self.color_B.configure(progress_color = blue_hex,button_color = blue_hex,button_hover_color = blue_hex)

        self.current_color_frame.configure(fg_color = self.rgb_to_hex((red,green,blue)))
        drawing_color = self.rgb_to_hex((red,green,blue))
        self.line_frame.configure(fg_color = drawing_color)

    def update_thickness(self,*args):
        drawing_thickness = int(*args)
        self.current_thickness.configure(text = str(drawing_thickness))
        self.line_frame.configure(height = drawing_thickness)

    def switch_draw_mode(self):
        if self.draw_circle.get() == 1:
            draw_mode = "circle"
            self.draw_line.deselect()
        else:
            draw_mode = "line"
            self.draw_circle.deselect()

    def clear_canvas(self):
        pass
        # main_frame.delete("drawing")

    def command_landed(self,message):
        if "nastav cervenou" in message:
            self.color_R.set(255.0)
            self.color_G.set(0.0)
            self.color_B.set(0.0)
        if "nastav zelenou" in message:
            self.color_R.set(0.0)
            self.color_G.set(255.0)
            self.color_B.set(0.0)

        self.update_color("")

    def create_widgets(self):
        window = customtkinter.CTkToplevel()
        # window.after(200, lambda: window.iconbitmap(app_icon))
        window_height = 500
        window_width = 700
        # x = root.winfo_rootx()
        # y = root.winfo_rooty()
        window.geometry(f"{window_width}x{window_height}")
        window.title("Možnosti malování" + str(self.pipe_name))


        top_frame =         customtkinter.CTkFrame(master = window,corner_radius=0,height=120)
        self.current_color_frame = customtkinter.CTkFrame(master = top_frame,corner_radius=0,border_width=2,height=100,width=100)
        slider_frame =      customtkinter.CTkFrame(master = top_frame,corner_radius=0,width=500)
        top_frame.          pack(pady=0,padx=0,fill="x",expand=False,side = "top")
        top_frame.pack_propagate(0)

        slider_frame.       pack(pady=(10,0),padx=(5,0),expand=False,side = "left")
        slider_frame.pack_propagate(0)
        self.current_color_frame.pack(pady=(10,0),padx=10,expand=False,side = "left",anchor = "w")

        frame_R =           customtkinter.CTkFrame(master = slider_frame,height=20,corner_radius=0,border_width=0)
        color_label =       customtkinter.CTkLabel(master = frame_R,text = "R: ",justify = "left",font=("Arial",16,"bold"))
        self.color_R =           customtkinter.CTkSlider(master=frame_R,width=400,height=15,from_=0,to=255,command= lambda e: self.update_color(e))
        self.current_color_val = customtkinter.CTkLabel(master = frame_R,text = "0",justify = "left",font=("Arial",16,"bold"))
        color_label.pack(pady=5,padx=5,expand=False,side = "left")
        self.color_R.pack(pady=5,padx=5,expand=False,side = "left")
        self.current_color_val.pack(pady=5,padx=5,expand=False,side = "left")
        self.color_R.set(0.0)
        
        frame_G =           customtkinter.CTkFrame(master = slider_frame,height=20,corner_radius=0,border_width=0)
        color_label =       customtkinter.CTkLabel(master = frame_G,text = "G: ",justify = "left",font=("Arial",16,"bold"))
        self.color_G =           customtkinter.CTkSlider(master=frame_G,width=400,height=15,from_=0,to=255,command= lambda e: self.update_color(e))
        self.current_color_val2 = customtkinter.CTkLabel(master = frame_G,text = "0",justify = "left",font=("Arial",16,"bold"))
        color_label.pack(pady=5,padx=5,expand=False,side = "left")
        self.color_G.pack(pady=5,padx=5,expand=False,side = "left")
        self.current_color_val2.pack(pady=5,padx=5,expand=False,side = "left")
        self.color_G.set(0.0)

        frame_B =           customtkinter.CTkFrame(master = slider_frame,height=20,corner_radius=0,border_width=0)
        color_label =       customtkinter.CTkLabel(master = frame_B,text = "B: ",justify = "left",font=("Arial",16,"bold"))
        self.color_B =           customtkinter.CTkSlider(master=frame_B,width=400,height=15,from_=0,to=255,command= lambda e: self.update_color(e))
        self.current_color_val3 = customtkinter.CTkLabel(master = frame_B,text = "0",justify = "left",font=("Arial",16,"bold"))
        color_label.pack(pady=5,padx=5,expand=False,side = "left")
        self.color_B.pack(pady=5,padx=5,expand=False,side = "left")
        self.current_color_val3.pack(pady=5,padx=5,expand=False,side = "left")
        self.color_B.set(0.0)

        bottom_frame = customtkinter.CTkFrame(master = window,corner_radius=0) 
        shape_checkboxes = customtkinter.CTkFrame(master = bottom_frame,corner_radius=0,fg_color="#292929") 
        self.draw_circle = customtkinter.CTkCheckBox(master = shape_checkboxes, text = "Kruh",command = lambda: self.switch_draw_mode(),font=("Arial",20))
        self.draw_line = customtkinter.CTkCheckBox(master = shape_checkboxes, text = "Osa",command = lambda: self.switch_draw_mode(),font=("Arial",20))
        self.draw_circle.pack(pady=0,padx=5,expand=False,side = "left")
        self.draw_line.pack(pady=0,padx=5,expand=False,side = "left")

        bottom_frame_label = customtkinter.CTkLabel(master = bottom_frame,text = "Nastavení tloušťky čáry:",justify = "left",font=("Arial",18,"bold"),anchor="w")

        thickness_frame = customtkinter.CTkFrame(master = bottom_frame,corner_radius=0,fg_color="#292929",height=55) 
        thickness = customtkinter.CTkSlider(master=thickness_frame,width=450,height=15,from_=1,to=50,command= lambda e: self.update_thickness(e))
        self.current_thickness = customtkinter.CTkLabel(master = thickness_frame,text = "0",justify = "left",font=("Arial",16,"bold"))
        self.line_frame = customtkinter.CTkFrame(master = thickness_frame,corner_radius=0,fg_color="black",height=1,width = 100) 
        thickness.pack(pady=5,padx=5,expand=False,side = "left")
        self.current_thickness.pack(pady=5,padx=5,expand=False,side = "left")
        self.line_frame.pack(pady=5,padx=5,expand=False,side = "left")
        thickness.set(0.0)

        cursor_button = customtkinter.CTkButton(master = bottom_frame,text = "nastav cervenou",font=("Arial",22,"bold"),width = 150,height=40,corner_radius=0,command=lambda: pipeline_duplex.call_checking("red"))
        clear_all = customtkinter.CTkButton(master = bottom_frame,text = "nastav zelenou",font=("Arial",22,"bold"),width = 150,height=40,corner_radius=0,command=lambda: pipeline_duplex.call_checking("green"))

        frame_R.pack(pady=0,padx=0,expand=False,side = "top",fill="x")
        frame_G.pack(pady=0,padx=0,expand=False,side = "top",fill="x")
        frame_B.pack(pady=0,padx=0,expand=False,side = "top",fill="x")

        bottom_frame.pack(pady=0,padx=0,fill="x",expand=False,side = "top")
        bottom_frame_label.pack(pady=5,padx=5,expand=False,side = "top",fill="x",anchor = "w")
        thickness_frame.pack(pady=(5,0),padx=5,expand=False,side = "top",fill="x")
        thickness_frame.pack_propagate(0)
        shape_checkboxes.pack(pady=5,padx=5,expand=False,side = "top",fill="x")
        cursor_button.pack(pady=(20,5),padx=5,expand=False,side = "top",fill="x")
        clear_all.pack(pady=5,padx=5,expand=False,side = "top",fill="x")

        # self.current_color_frame.configure(fg_color = drawing_color)
        # previous_color = hex_to_rgb(drawing_color)
        # self.color_R.set(previous_color[0])
        # self.color_G.set(previous_color[1])
        # self.color_B.set(previous_color[2])
        self.draw_line.select()
        button_exit = customtkinter.CTkButton(master = window,text = "Zrušit",font=("Arial",22,"bold"),width = 200,height=50,corner_radius=0,command=lambda: self.close_window(window))
        button_exit.pack(pady = 10, padx = 10,expand=False,side="bottom",anchor = "e")

        # root.bind("<Button-1>",lambda e: close_window(window))
        window.update()
        window.update_idletasks()
        # window.focus_force()
        # window.grab_set()
        # window.grab_release()
        # window.withdraw()

        # window.focus()

# draw = drawing_option_window(root,pipeline_duplex.pipe_name)
# root.mainloop()
# k = input("jojojoj")
def calc_days_in_month(current_month):
    months_30days = [4,6,9,11]
    if current_month == 2:
        days_in_month = 28
    elif current_month in months_30days:
        days_in_month = 30
    else:
        days_in_month = 31
        
    return days_in_month

def get_cutoff_date(days):

    # current_date = Deleting.get_current_date()
    current_date = "03.12.2024"
    # current_day, current_month, current_year = current_date[1].split(".")
    current_day, current_month, current_year = current_date.split(".")
    day = int(current_day)
    month = int(current_month)
    year = int(current_year)

    while days > 0:
        day -= 1
        if day == 0:
            month -= 1
            if month ==0:
                month = 12
                year -= 1
            day = calc_days_in_month(month)

        days -= 1
    return [day,month,year]

def get_max_days():
    # print(self.cutoff_date)
    day = 31
    month = 12
    year = 2023
    # current_date = Deleting.get_current_date()
    current_date = "01.01.2024"
    # current_day, current_month, current_year = current_date[1].split(".")
    current_day, current_month, current_year = current_date.split(".")
    year_div = int(current_year) - int(year)
    month_div = int(current_month) - int(month)
    month_div += year_div*12

    day_div = int(current_day) - int(day)
    for i in range(0,month_div):
        day_div += calc_days_in_month(month)
        month +=1
        if month > 12:
            month=1

    # for month in range(int(current_month),13):
    #     print("month: ",month)
    #     day_div += calc_days_in_month(month)
    #     month +=1
    #     if month > 12:
    #         month=1
    # if year_div > 0:
    #     for month in range(1,13):
    #         print("month: ",month)
    #         day_div += calc_days_in_month(month)
    #         month +=1
    #         if month > 12:
    #             month=1 


    # print(f"starší o: {year_div} roky")
    # print(f"starší o: {month_div} mes")
    # print(f"starší o: {day_div} dni")
def check_input(input_char):
    def wrong_format():
        return False

    if not ":" in input_char:
        wrong_format()
    elif len(input_char.split(":")) != 2:
        wrong_format()
    elif len(str(input_char.split(":")[1])) != 2:
        wrong_format()
    elif int(input_char.split(":")[0]) > 23 or int(input_char.split(":")[0]) < 0 or int(input_char.split(":")[1]) > 59 or int(input_char.split(":")[1]) < 0:
        wrong_format()  

check_input("15:00")