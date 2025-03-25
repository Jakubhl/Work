from cx_Freeze import setup, Executable
import sys
import os

# Include additional data files like images and the public.pem file
include_files = [
    ("images", "images"),  # Include entire 'images' folder
    ("public.pem", "public.pem"),  # Include public.pem file
    ("Rights_maker.bat", "Rights_maker.bat"),  
]

# Define the base
base = "Win32GUI" if sys.platform == "win32" else None  # Hide console for GUI apps
# base = None


# Define the executable
exe = Executable(
    script="JHV_MAZ_GUI_v4.py",  # Main script to convert to EXE
    base=base,
    target_name="jhv_MAZ.exe",  # Name of the output EXE file
    icon="images/logo_TRIMAZKON.ico",  # Application icon
)

# Setup configuration
# setup(
#     name="jhv_MAZ",
#     version="1.0.6",
#     description="jhv_MAZ v1.0.6",
#     executables=[exe],
#     options={
#         "build_exe": {
#             "packages": [],  # Add required packages if needed
#             "include_files": include_files,  # Add extra files
#             "optimize": 2,  # Optimize bytecode
#         },
#         "bdist_msi": {
#             "upgrade_code": "{87654321-4321-8765-4321-678543218765}",  # Unique GUID
#             "add_to_path": False,  # Do not add to system PATH
#             "install_icon": "images/logo_TRIMAZKON.ico",  # Installer icon
#         },
#     },
# )