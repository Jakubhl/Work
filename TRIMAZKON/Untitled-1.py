import sys
from plyer import notification

# CREATING TASK:
# name_of_task = "dailyscript_test"
# path_to_app = r"C:\Users\jakub.hlavacek.local\Desktop\JHV\Work\TRIMAZKON\pipe_server\untitled2.py"
# cmd_command = f"schtasks /Create /TN {name_of_task} /TR {path_to_app} /SC DAILY /ST 09:35"
# connection_status = subprocess.call(cmd_command,shell=True,text=True)

#DELETING TASK:
# name_of_task = "dailyscript_test"
# cmd_command = f"schtasks /Delete /TN {name_of_task} /F"
# connection_status = subprocess.call(cmd_command,shell=True,text=True)

print(len(str("")))
all_string = "|||Datum: 17.12.2024 10:12:26||Zkontrolováno: 161 souborů||Starších: 153 souborů||Smazáno: 0 souborů"
print(all_string.split("|||"))
splitted = all_string.split("|||")
splitted.pop(0)
print(splitted[0].split("||"))
output_data = ["xx","xxf","xxx","sga"]
output_message_clear = f"Provedeno: {output_data[3]}\nZkontrolováno: {output_data[0]} souborů\nStarších: {output_data[1]} souborů\nSmazáno: {output_data[2]} souborů"

notification.notify(
        title="Bylo provedeno automatické mazání",
        message=output_message_clear,
        app_name="TRIMAZKON",
        timeout=5,
        app_icon = 'images/logo_TRIMAZKON.ico'
    )

# from win10toast_click import ToastNotifier

# Callback function to handle the click event
# def on_notification_click():
#     print("Notification was clicked!")
#     return True

# # Create a ToastNotifier instance
# toaster = ToastNotifier()

# # Show the notification and set the click callback
# try:
#     toaster.show_toast(
#         "My Application",                    # Notification title
#         output_message_clear,  # Notification message
#         icon='images/logo_TRIMAZKON.ico',
#         duration=10,                         # Duration in seconds
#         threaded=True,                       # Allows the program to keep running
#         callback_on_click=lambda:on_notification_click()  # Function to call on click
#     )
# except Exception as e:
#     pass
