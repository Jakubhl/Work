import psutil

def get_all_app_processes():
    pid_list = []
    num_of_apps = 0
    for process in psutil.process_iter(['pid', 'name']):
        # if process.info['name'] == "TRIMAZKON_test.exe":
        if process.info['name'] == "jhv_MAZ3.exe":
            print(process.info)
            pid_list.append(process.info['pid'])
            num_of_apps+=1
    
    return [num_of_apps,pid_list]

print(get_all_app_processes())


# import tkinter as tk
# from tkinter import messagebox

# def on_closing():
#     if messagebox.askokcancel("Quit", "Do you want to quit?"):
#         root.destroy()  # Close the application

# root = tk.Tk()
# root.title("Close Button Example")
# root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle the close button
# root.mainloop()