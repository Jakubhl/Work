
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

class tray_app_service:
    def __init__(self,task_list,deletion_log):
        self.main()
        
    # Function to create an icon
    def create_image(self):
        # Create a 64x64 icon
        image = Image.new('RGB', (64, 64), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.rectangle((16, 16, 48, 48), fill='blue')
        return image

    # Function for quitting the application
    def quit_application(self,icon, item):
        icon.stop()

    def add_command(self):
        self.icon.menu = Menu(
        MenuItem('New Action', lambda icon, item: print("Action triggered"))
        )

    # Create a menu
    def create_menu(self):
        self.menu = Menu(MenuItem('Quit', self.quit_application),
                    MenuItem('Log mazani', self.add_command))

    def main(self):
        # Create the tray icon
        self.create_menu()

        self.icon = Icon(
            "MyApplication",
            self.create_image(),
            "My Application Tooltip",
            self.menu
        )

        # Run the tray icon
        self.icon.run()

# CREATING TASK:
# name_of_task = "dailyscript_test"
# path_to_app = r"C:\Users\jakub.hlavacek.local\Desktop\JHV\Work\TRIMAZKON\pipe_server\untitled2.py"
# cmd_command = f"schtasks /Create /TN {name_of_task} /TR {path_to_app} /SC DAILY /ST 09:35"
# connection_status = subprocess.call(cmd_command,shell=True,text=True)

#DELETING TASK:
# name_of_task = "dailyscript_test"
# cmd_command = f"schtasks /Delete /TN {name_of_task} /F"
# connection_status = subprocess.call(cmd_command,shell=True,text=True)