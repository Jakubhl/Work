import os
import subprocess

supported_formats = [".ifz"]
output = []
folder_with_bmp = "konvertovane_BMP"
folder_with_jpg = "konvertovane_JPG"

whole_app_path = os.getcwd()
application_path = whole_app_path + "/convert_application/"


def path_check(path_raw):
    path=path_raw
    backslash = "\ "
    if backslash[0] in path:
        newPath = path.replace(os.sep, '/')
        path = newPath

    if path.endswith('/') == False:
        newPath = path + "/"
        path = newPath

    if not os.path.exists(path):
        return False

    else:
        return path

application_path = path_check(application_path)
application_path = application_path + "IfzToBitmap.exe"



def whole_converting_function(path_given,output_img_format,folder_with_bmp_name,folder_with_jpg_name):
    """
    Funkce pro konvertování souborů

    """
    folder_with_bmp = folder_with_bmp_name
    folder_with_jpg = folder_with_jpg_name
    def make_dir(name,path):
        if not os.path.exists(path + name): #pokud uz neni vytvorena, vytvor...
            os.mkdir(path + name + "/")

    def get_files_to_convert():
        files_to_convert = []
        for files in os.listdir(path_given):
            if supported_formats[0] in files:
                if not files in files_to_convert:
                    files_to_convert.append(path_given+files)

        return files_to_convert
    
    def form_console_command(files_to_convert,which_format):
        command = ""
        converted_files = 0
        if len(files_to_convert) != 0:
            command = str(application_path) + " byrtobmp " + files_to_convert[0] + " "
            converted_files +=1
            if len(files_to_convert) != 1:
                i=0
                for files in files_to_convert:
                    converted_files +=1
                    i+=1
                    if i>1:
                        command = command + " " + files

            if which_format == "bmp":
                make_dir(folder_with_bmp,path_given)
                command = command + " /o:" + path_given + folder_with_bmp

            if which_format == "jpg":
                make_dir(folder_with_jpg,path_given)
                command = command + " /o:" + path_given + folder_with_jpg + " /f:jpg"
            
            output.append(f"Bylo konvertováno: {converted_files} souborů do formátu: {which_format}")
            output.append("Konvertování bylo dokončeno\n")
            return command
        else:
            output.append("Vložená cesta neobsahuje žádné soubory typu .ifz")
            return False

        
    def main():
        #output.append(f"\nProbíhá konvertování souborů v cestě: {path_given}\n\n")
        found_files = get_files_to_convert()
        if output_img_format == "jpg":
            cmd_command = form_console_command(found_files,"jpg")
        if output_img_format == "bmp":
            cmd_command = form_console_command(found_files,"bmp")
        
        if cmd_command != False:
            subprocess.run(cmd_command) #spusteni cmd prompt

    main()
    return output
#whole_converting_function("C:/Users/kubah/Desktop/JHV/konvertor_ifz/IfzToBitmap/pokusy/")
