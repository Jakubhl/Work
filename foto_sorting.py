import os
import shutil

#path = input("enter the path to folder, (e.g.: D:/JHV/Kamery/JHV_Data/L_St_145/B/): ")
path = "D:/JHV/Kamery/JHV_Data/L_St_145/A - Copy/"

folder_name = ['3D','Normal','NOK']
names = os.listdir(path)
normal_count = 0
height_count = 0
nok_count = 0
arr_normal_cut = []
arr_height_cut = []
arr_normal = []
arr_height = []

print("checking/ creating folders...")

for x in range(0,2):
    if not os.path.exists(path + folder_name[x]):
        os.makedirs(path + folder_name[x])

print("making arrays...")

for files in names:
    
    if ".Normal" in files:
        arr_normal.append(files)
        arr_normal_cut.append(files[0:26])
        normal_count+=1

    if ".Height" in files:
        arr_height.append(files)
        arr_height_cut.append(files[0:26])
        height_count+=1

print("sorting into folders...")

for i in range (0,normal_count):    
    if arr_normal_cut[i] not in arr_height_cut:
        if not os.path.exists(path + folder_name[2]):
            os.makedirs(path + folder_name[2])
        print(arr_normal[i] + ' -> NOK')
        nok_count += 1
        shutil.move(path + arr_normal[i], path + folder_name[2] + '/' + arr_normal[i]) # -> NOK (solo) dir
    else:
        shutil.move(path + arr_normal[i], path + folder_name[1] + '/' + arr_normal[i]) # -> OK - .Normal dir 
        
for j in range (0,height_count):
    if arr_height_cut[j] not in arr_normal_cut:
        if not os.path.exists(path + folder_name[2]):
            os.makedirs(path + folder_name[2])
        print(arr_height[j] + ' -> NOK')
        nok_count += 1
        shutil.move(path + arr_height[j], path + folder_name[2] + '/' + arr_height[j]) # -> NOK (solo) dir
    else:
        shutil.move(path + arr_height[j], path + folder_name[0] + '/' + arr_height[j]) # -> OK - .Height, 3D dir

print("sorting done")
print("number of nok files: ",nok_count)
        


    

