import tkinter as tk
import funds
import left_frame as lf
import right_frame as rf
import lower_frame as lowf

image = "C:\\Users\\Van Phu Hoa\\PycharmProjects\\money_tracker\\background.png"
month = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}
database = sheetName = None


def create_window():
    global root_window, image, database, sheetName

    root_window = tk.Tk()
    root_window.title("Money Tracker")
    root_window.iconbitmap(
        "C:\\Users\\Van Phu Hoa\\PycharmProjects\\money_tracker\\icon.ico"
    )
    root_window.geometry("600x600")

    background_image = tk.PhotoImage(file=image)
    background_label = tk.Label(root_window, image=background_image)
    background_label.place(relx=0, rely=0, relheight=1, relwidth=1)

    name_app = tk.Text(root_window, font=('Transformers Movie', 70), bg='#1F2326', fg='white', bd=0)
    name_app.insert('end', """Money\n  Tracker""")
    name_app.place(relx=0.6, rely=0.05, relwidth=0.3, relheight=0.25)

    output = lowf.create_lower_frame(root_window)
    rf.create_right_frame(root_window, output)
    lf.create_left_frame(root_window, output)

    root_window.mainloop()
