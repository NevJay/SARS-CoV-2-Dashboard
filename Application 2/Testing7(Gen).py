from tkinter import *
from tkinter.filedialog import askopenfilename
import customtkinter
import pandas as pd


def get_data_frame11():
    global df_a11
    global col
    file_name = askopenfilename()
    df_a11 = pd.read_csv(file_name)
    col = list(df_a11)
    print(col)

def Graphs():
    #root.destroy()
    global root2
    root2 = Tk()
    root2.geometry("480x708")
    root2.resizable(False, False)
    root2["bg"] = "#161C30"
    root2.title("Genetrix")

    Label(root2, text="Welcome To Genetrix Analysis", bg="black", fg="white", font=("monospace", 20, "bold"), width=40, bd=4,relief=RIDGE).pack(side=TOP, fill=X)
    customtkinter.CTkButton(root2, text="BROWSE", bd=0, height=50, width=250, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22),command=get_data_frame11).place(x=110, y=240)
    customtkinter.CTkButton(root2, text="ANALYSE", bd=0, height=50, width=250, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22)).place(x=110, y=310)
    customtkinter.CTkButton(root2, text="GENERATE", bd=0, height=50, width=250, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22)).place(x=110, y=380)
    customtkinter.CTkButton(root2, text="BACK", bd=0, height=50, width=250, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22), command="MainBack").place(x=110, y=450)

    root2.mainloop()

Graphs()