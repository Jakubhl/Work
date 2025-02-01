import psutil
import shutil
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

# print(get_all_app_processes())¨

def calc_cutoffdays_given(self):
    given_day = str(self.cutoff_date_given[0])
    given_month = str(self.cutoff_date_given[1])
    if len(given_day) == 1:
        given_day = "0" + given_day
    if len(given_month) == 1:
        given_month = "0" + given_month

    cutoff_date = str(self.cutoff_date_given[2])+given_month+given_day
    readable_cutoff_date = given_day + "." + given_month + "." + str(self.cutoff_date_given[2])
    print(cutoff_date,readable_cutoff_date)
    return [cutoff_date,readable_cutoff_date]

 def del_dirs_by_creation():
    deleted_directores = 0
    directories_checked = 0
    folder_list = [entry.name for entry in os.scandir(self.path) if entry.is_dir()]
    print(folder_list)
    cutoff_days = self.calc_cutoffdays_given()
    cutoff_days = cutoff_days[0]
    
    for i in range(0,len(folder_list)):
        directories_checked +=1
        folder_date = self.get_mod_date_of_file(self.path,folder_list[i])
        print(folder_date)



# import tkinter as tk
# from tkinter import messagebox

# def on_closing():
#     if messagebox.askokcancel("Quit", "Do you want to quit?"):
#         root.destroy()  # Close the application

# root = tk.Tk()
# root.title("Close Button Example")
# root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle the close button
# root.mainloop()