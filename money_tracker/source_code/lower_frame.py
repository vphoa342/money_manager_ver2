import tkinter as tk


def create_lower_frame(root_window):
    global output
    # lower frame
    low_frame = tk.Frame(root_window, bg="white")
    low_frame.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.5)
    output = tk.Text(low_frame)
    output.place(relx=0, rely=0)
    return output
