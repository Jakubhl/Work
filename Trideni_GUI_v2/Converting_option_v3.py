import os
import subprocess
import time

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
application_path = "\"" + application_path + "IfzToBitmap.exe" + "\""

#only_view_image:bool,ifz_image_name:str

class whole_converting_function:
    """
    Funkce pro konvertování souborů

    """
    def __init__(self,path_given,output_img_format,folder_with_bmp_name,folder_with_jpg_name,view_in_browser=None,selected_file = None):
        self.folder_with_bmp = folder_with_bmp_name
        self.folder_with_jpg = folder_with_jpg_name
        self.path_given = path_given
        self.view_in_browser = view_in_browser
        self.selected_file = selected_file
        self.output_img_format = output_img_format
        self.output = []
        self.supported_formats = [".ifz"]
        self.finish = False
        self.converted_files = 0
        self.processing_time = 0
        if self.view_in_browser == True:
            self.main()

    def make_dir(self,name,path):
        if not os.path.exists(path + name): #pokud uz neni vytvorena, vytvor...
            os.mkdir(path + name + "/")

    def get_files_to_convert(self):
        files_to_convert = []
        for files in os.listdir(self.path_given):
            if self.supported_formats[0] in files:
                if not files in files_to_convert:
                    #files_to_convert.append(self.path_given+files)
                    files_to_convert.append(files)

        return files_to_convert
    
    def form_console_command(self,files_to_convert,which_format,silent=None):
        command = ""
        if len(files_to_convert) != 0:
            command = str(application_path) + " byrtobmp " + files_to_convert[0] + " "
            self.converted_files +=1
            if len(files_to_convert) != 1:
                i=0
                for files in files_to_convert:
                    self.converted_files +=1
                    i+=1
                    if i>1:
                        command = command + " " + files

            if which_format == "bmp":
                self.make_dir(self.folder_with_bmp,self.path_given)
                # cesta v uvozovkach kvuli vykonani v cmd
                command = command + " /o:" + "\""  + self.path_given + self.folder_with_bmp + "\""

            if which_format == "jpg":
                self.make_dir(self.folder_with_jpg,self.path_given)
                command = command + " /o:" + "\"" + self.path_given + self.folder_with_jpg+ "\"" + " /f:jpg"
            
            if silent == None:
                self.output.append(f"- Bylo konvertováno: {self.converted_files-1} souborů do formátu: {which_format}")
                self.output.append("- Konvertování bylo dokončeno\n")
            
            #if self.view_in_browser == True:
            command += " /h" #nezobrazovat nacitani

            return command
        else:
            if silent == None:
                self.output.append("- Vložená cesta neobsahuje žádné soubory typu .ifz")
            return False

    def main(self):
        #output.append(f"\nProbíhá konvertování souborů v cestě: {self.path_given}\n\n")
        if self.view_in_browser == True:
            found_files = []
            if type(self.selected_file) == list:
                for i in range(0,len(self.selected_file)):
                    found_files.append(self.selected_file[i])
            else:
                found_files.append(self.selected_file)
            cmd_command = self.form_console_command(found_files,"bmp",True)
            
            if cmd_command != False:
                subprocess.run(cmd_command, cwd=self.path_given) #spusteni cmd prompt
        else:
            found_files = self.get_files_to_convert()
            if self.output_img_format == "jpg":
                cmd_command = self.form_console_command(found_files,"jpg")
            if self.output_img_format == "bmp":
                cmd_command = self.form_console_command(found_files,"bmp")
            
            if cmd_command != False:
                self.processing_time = (self.converted_files-1)/10
                subprocess.run(cmd_command, cwd=self.path_given) #spusteni cmd prompt
        self.finish = True

