import tkinter

# Get Tcl and Tk versions
tcl_version = tkinter.Tcl().eval('info patchlevel')
tk_version = tkinter.TkVersion

print("Tcl version:", tcl_version)
print("Tk version:", tk_version)
