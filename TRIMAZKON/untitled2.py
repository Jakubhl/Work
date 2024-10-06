import customtkinter

def drawing_option_window():
    def close_window(window):
        window.destroy()
    
    def rgb_to_hex(rgb,one_color = False):
        if not one_color:
            return "#%02x%02x%02x" % rgb
        elif one_color == "red":
            return ("#%02x" % rgb) + "0000"
        elif one_color == "green":
            return "#00" + ("%02x" % rgb) + "00"
        elif one_color == "blue":
            return "#0000" + ("%02x" % rgb)
        
    def hex_to_rgb(hex_color):
        # Remove the '#' character if present
        hex_color = hex_color.lstrip('#')
        # Convert the hex string into RGB tuple
        return list(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def update_color(*args):
        nonlocal current_color_frame

        red = int(color_R.get())
        red_hex = rgb_to_hex(red,one_color="red")
        current_color_val.configure(text = str(red))
        color_R.configure(progress_color = red_hex,button_color = red_hex,button_hover_color = red_hex)

        green = int(color_G.get())
        green_hex = rgb_to_hex(green,one_color="green")
        current_color_val2.configure(text = str(green))
        color_G.configure(progress_color = green_hex,button_color = green_hex,button_hover_color = green_hex)

        blue = int(color_B.get())
        blue_hex = rgb_to_hex(blue,one_color="blue")
        current_color_val3.configure(text = str(blue))
        color_B.configure(progress_color = blue_hex,button_color = blue_hex,button_hover_color = blue_hex)

        current_color_frame.configure(fg_color = rgb_to_hex((red,green,blue)))
        drawing_color = rgb_to_hex((red,green,blue))
        line_frame.configure(fg_color = drawing_color)

    def update_thickness(*args):
        drawing_thickness = int(*args)
        current_thickness.configure(text = str(drawing_thickness))
        line_frame.configure(height = drawing_thickness)

    def switch_draw_mode():
        nonlocal draw_circle
        nonlocal draw_line

        if draw_circle.get() == 1:
            draw_mode = "circle"
            draw_line.deselect()
        else:
            draw_mode = "line"
            draw_circle.deselect()

    def clear_canvas():
        pass
        # main_frame.delete("drawing")

    window = customtkinter.CTkToplevel()
    # window.after(200, lambda: window.iconbitmap(app_icon))
    window_height = 500
    window_width = 700
    # x = root.winfo_rootx()
    # y = root.winfo_rooty()
    window.geometry(f"{window_width}x{window_height}")
    window.title("Možnosti malování")


    top_frame =         customtkinter.CTkFrame(master = window,corner_radius=0,height=120)
    current_color_frame = customtkinter.CTkFrame(master = top_frame,corner_radius=0,border_width=2,height=100,width=100)
    slider_frame =      customtkinter.CTkFrame(master = top_frame,corner_radius=0,width=500)
    top_frame.          pack(pady=0,padx=0,fill="x",expand=False,side = "top")
    top_frame.pack_propagate(0)

    slider_frame.       pack(pady=(10,0),padx=(5,0),expand=False,side = "left")
    slider_frame.pack_propagate(0)
    current_color_frame.pack(pady=(10,0),padx=10,expand=False,side = "left",anchor = "w")

    frame_R =           customtkinter.CTkFrame(master = slider_frame,height=20,corner_radius=0,border_width=0)
    color_label =       customtkinter.CTkLabel(master = frame_R,text = "R: ",justify = "left",font=("Arial",16,"bold"))
    color_R =           customtkinter.CTkSlider(master=frame_R,width=400,height=15,from_=0,to=255,command= lambda e: update_color(e))
    current_color_val = customtkinter.CTkLabel(master = frame_R,text = "0",justify = "left",font=("Arial",16,"bold"))
    color_label.pack(pady=5,padx=5,expand=False,side = "left")
    color_R.pack(pady=5,padx=5,expand=False,side = "left")
    current_color_val.pack(pady=5,padx=5,expand=False,side = "left")
    color_R.set(0.0)
    
    frame_G =           customtkinter.CTkFrame(master = slider_frame,height=20,corner_radius=0,border_width=0)
    color_label =       customtkinter.CTkLabel(master = frame_G,text = "G: ",justify = "left",font=("Arial",16,"bold"))
    color_G =           customtkinter.CTkSlider(master=frame_G,width=400,height=15,from_=0,to=255,command= lambda e: update_color(e))
    current_color_val2 = customtkinter.CTkLabel(master = frame_G,text = "0",justify = "left",font=("Arial",16,"bold"))
    color_label.pack(pady=5,padx=5,expand=False,side = "left")
    color_G.pack(pady=5,padx=5,expand=False,side = "left")
    current_color_val2.pack(pady=5,padx=5,expand=False,side = "left")
    color_G.set(0.0)

    frame_B =           customtkinter.CTkFrame(master = slider_frame,height=20,corner_radius=0,border_width=0)
    color_label =       customtkinter.CTkLabel(master = frame_B,text = "B: ",justify = "left",font=("Arial",16,"bold"))
    color_B =           customtkinter.CTkSlider(master=frame_B,width=400,height=15,from_=0,to=255,command= lambda e: update_color(e))
    current_color_val3 = customtkinter.CTkLabel(master = frame_B,text = "0",justify = "left",font=("Arial",16,"bold"))
    color_label.pack(pady=5,padx=5,expand=False,side = "left")
    color_B.pack(pady=5,padx=5,expand=False,side = "left")
    current_color_val3.pack(pady=5,padx=5,expand=False,side = "left")
    color_B.set(0.0)

    bottom_frame = customtkinter.CTkFrame(master = window,corner_radius=0) 
    shape_checkboxes = customtkinter.CTkFrame(master = bottom_frame,corner_radius=0,fg_color="#292929") 
    draw_circle = customtkinter.CTkCheckBox(master = shape_checkboxes, text = "Kruh",command = lambda: switch_draw_mode(),font=("Arial",20))
    draw_line = customtkinter.CTkCheckBox(master = shape_checkboxes, text = "Osa",command = lambda: switch_draw_mode(),font=("Arial",20))
    draw_circle.pack(pady=0,padx=5,expand=False,side = "left")
    draw_line.pack(pady=0,padx=5,expand=False,side = "left")

    bottom_frame_label = customtkinter.CTkLabel(master = bottom_frame,text = "Nastavení tloušťky čáry:",justify = "left",font=("Arial",18,"bold"),anchor="w")

    thickness_frame = customtkinter.CTkFrame(master = bottom_frame,corner_radius=0,fg_color="#292929",height=55) 
    thickness = customtkinter.CTkSlider(master=thickness_frame,width=450,height=15,from_=1,to=50,command= lambda e: update_thickness(e))
    current_thickness = customtkinter.CTkLabel(master = thickness_frame,text = "0",justify = "left",font=("Arial",16,"bold"))
    line_frame = customtkinter.CTkFrame(master = thickness_frame,corner_radius=0,fg_color="black",height=1,width = 100) 
    thickness.pack(pady=5,padx=5,expand=False,side = "left")
    current_thickness.pack(pady=5,padx=5,expand=False,side = "left")
    line_frame.pack(pady=5,padx=5,expand=False,side = "left")
    thickness.set(0.0)

    cursor_button = customtkinter.CTkButton(master = bottom_frame,text = "Kurzor uprostřed",font=("Arial",22,"bold"),width = 150,height=40,corner_radius=0,command=lambda: clear_canvas())
    clear_all = customtkinter.CTkButton(master = bottom_frame,text = "Vyčistit",font=("Arial",22,"bold"),width = 150,height=40,corner_radius=0,command=lambda: clear_canvas())

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

    # current_color_frame.configure(fg_color = drawing_color)
    # previous_color = hex_to_rgb(drawing_color)
    # color_R.set(previous_color[0])
    # color_G.set(previous_color[1])
    # color_B.set(previous_color[2])
    draw_line.select()

    button_exit = customtkinter.CTkButton(master = window,text = "Zrušit",font=("Arial",22,"bold"),width = 200,height=50,corner_radius=0,command=lambda: close_window(window))
    button_exit.pack(pady = 10, padx = 10,expand=False,side="bottom",anchor = "e")

    # root.bind("<Button-1>",lambda e: close_window(window))
    window.update()
    window.update_idletasks()
    window.focus_force()
    window.grab_set()
    # window.grab_release()

    window.focus()

drawing_option_window()
k = input("jojojoj")