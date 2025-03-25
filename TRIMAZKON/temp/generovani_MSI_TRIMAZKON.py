from cx_Freeze import setup, Executable
import sys
import os

# Include additional data files like images and the public.pem file
include_files = [
    ("images", "images"),  # Include entire 'images' folder
    ("convert_application", "convert_application"),
    ("public.pem", "public.pem"),  # Include public.pem file
    # ("Rights_maker.bat", "Rights_maker.bat"),  
]

# Define the base
base = "Win32GUI" if sys.platform == "win32" else None  # Hide console for GUI apps
# base = None


# Define the executable
exe = Executable(
    script="JHV_APP_GUI_v17.py",  # Main script to convert to EXE
    base=base,
    target_name="TRIMAZKON.exe",  # Name of the output EXE file
    icon="images/logo_TRIMAZKON.ico",  # Application icon
)

shortcut_table = [
    (
        "DesktopShortcut",  # Shortcut name
        "DesktopFolder",    # Location: Desktop
        "TRIMAZKON",       # Shortcut display name
        "TARGETDIR",       # Installation directory
        "[TARGETDIR]TRIMAZKON.exe",  # Executable path
        None,               # Arguments
        None,               # Description
        None,               # Hotkey
        None,               # Icon index
        "images/logo_TRIMAZKON.ico",  # Icon path
        "TARGETDIR",        # Working directory
        None,               # Advertised (should be None)
    )
]

msi_data = {"Shortcut": shortcut_table,}
            # "CustomAction": [
            #     ("PostInstall", None, "TARGETDIR", "cmd.exe /c start \"\" \"[TARGETDIR]/TRIMAZKON.exe\"")
            # ],
            # "InstallExecuteSequence": [
            #     ("PostInstall", "NOT Installed", 3599)  # Run after installation
            # ]}  # MSI data for shortcuts

# Setup configuration
setup(
    name="TRIMAZKON",
    version="4.3.1",
    description="TRIMAZKON v_4.3.1",
    executables=[exe],
    options={
        "build_exe": {
            "packages": [],  # Add required packages if needed
            "include_files": include_files,  # Add extra files
            "optimize": 2,  # Optimize bytecode
        },
        "bdist_msi": {
            "upgrade_code": "{12345678-1234-5678-1234-567812345678}",  # Unique GUID
            "add_to_path": False,  # Do not add to system PATH
            "install_icon": "images/logo_TRIMAZKON.ico",  # Installer icon
            "data": msi_data,

            # "all_users": True,  # This helps set the proper MSI window icon
            
        },            
    },
)