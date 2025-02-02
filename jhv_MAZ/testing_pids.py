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

string = "platnost vypršela:"
print(string.replace("platnost","nic"))