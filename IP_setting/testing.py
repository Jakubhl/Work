import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("600x400")  # Set initial window size

    # Create three frames
    frame1 = tk.Frame(root, bg='lightblue')
    frame2 = tk.Frame(root, bg='lightgreen')
    frame3 = tk.Frame(root, bg='lightcoral')

    # Place frames in the grid
    frame1.grid(row=0, column=0, sticky='nsew')
    frame2.grid(row=0, column=1, sticky='nsew')
    frame3.grid(row=0, column=2, sticky='nsew')

    # Configure grid columns and rows to have equal weight
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()