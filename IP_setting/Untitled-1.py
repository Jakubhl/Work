import win32api
import win32file

def list_mapped_disks():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    remote_drives = []
    for drive in drives:
        if win32file.GetDriveType(drive) == win32file.DRIVE_REMOTE:
            remote_drives.append(drive[0:1])
    
    return remote_drives

if __name__ == "__main__":
    mapped_disks = list_mapped_disks()
    for disk in mapped_disks:
        print(f"Disk: {disk}")
