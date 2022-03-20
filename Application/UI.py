import mysql.connector
from tkinter import *
from tkinter import messagebox

class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Weerasinghe2001',
    port='3306',
    database='smsschool'
)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
        self.conn.commit()

    def __del__(self):
        self.conn.close()
    def view(self):
        self.cur.execute("SELECT * FROM user")
        rows = self.cur.fetchall()
        return rows

    def insert(self, id, username, password):
        self.cur.execute("INSERT INTO user VALUES (%s,%s,%s)", (id, username, password,))
        self.conn.commit()
        self.view()

    def delete(self, id):
        self.cur.execute("DELETE FROM user WHERE id=%s", (id,))
        self.conn.commit()
        self.view()

    def search(self, id="", username=""):
        self.cur.execute("SELECT * FROM user WHERE id=%s OR username=%s", (id, username,))
        rows = self.cur.fetchall()
        return rows

db = DB()

def get_selected_row(event):
    global selected_tuple
    index = list1.curselection()
    selected_tuple = list1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[0])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[1])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[2])

def view_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)

def search_command():
    list1.delete(0, END)
    for row in db.search(id_text.get(), username_text.get()):
        list1.insert(END, row)


def add_command():
    db.insert(id_text.get(), username_text.get(), password_text.get())
    list1.delete(0, END)
    list1.insert(END, (id_text.get(), username_text.get(), password_text.get()))

def delete_command():
    db.delete(selected_tuple[0])

window = Tk()

window.title("Records")

def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        del dd

window.protocol("WM_DELETE_WINDOW", on_closing)

l1 = Label(window, text="ID")
l1.grid(row=0, column=0)

l2 = Label(window, text="Username")
l2.grid(row=0, column=2)

l3 = Label(window, text="Password")
l3.grid(row=1, column=0)

id_text = IntVar()
e1 = Entry(window, textvariable=id_text)
e1.grid(row=0, column=1)

username_text = StringVar()
e2 = Entry(window, textvariable=username_text)
e2.grid(row=0, column=3)

password_text = StringVar()
e3 = Entry(window, textvariable=password_text)
e3.grid(row=1, column=1)

list1 = Listbox(window, height=25, width=65)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(window, text="View all", width=12, command=view_command)
b1.grid(row=2, column=3)

b2 = Button(window, text="Search entry", width=12, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Add entry", width=12, command=add_command)
b3.grid(row=4, column=3)

b5 = Button(window, text="Delete selected", width=12, command=delete_command)
b5.grid(row=5, column=3)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=6, column=3)

window.mainloop()