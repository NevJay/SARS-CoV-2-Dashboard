import tkinter
from tkinter import *
import sqlite3
import tkinter.messagebox as mb
from tkinter import *
import sqlite3
import tkinter.messagebox as mb
from tkinter import filedialog, ttk
from tkinter.filedialog import askopenfilename

import customtkinter
import tk as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import pandas as pd
from tkinter import *
from tkinter.ttk import Progressbar
import time

from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder


def showPassword(event):
    wdgt = event.widget
    wdgt['show'] = ''

def hidePassword(event):
    wdgt = event.widget
    wdgt['show'] = '*'

class LabeledEntry(LabelFrame):
    """label fram containig a entry and error display label and a label to add image
    some parameters:
    parent,
    lbltext :  acts as placeholder,
    err_msg :  by default none if wanted to warn add values get erased as Entry get the focus
    imglcn:  location for icon
     """

    def __init__(self, master, lbltext, err_msg, imglcn=None, *args, **kwargs):
        LabelFrame.__init__(self, master, *args, **kwargs)
        self.config(bd=0, text=lbltext,fg='white')

        self.lbltext = lbltext
        self.err_msg = err_msg

        # variable to hold entry data
        self.Entry_var = StringVar()

        self.ico = PhotoImage(file=imglcn)
        self.imglbl = Label(self, bd=0, image=self.ico, **kwargs)

        self.entry = Entry(self, bd=0, width=35, font=('', 12), textvariable=self.Entry_var, bg='#221a1a',fg='white')
        # frame draws a line just below entry
        self.line = Frame(self, bd=0, width=50, height=2, bg='black')
        # id any error occurs use this to deiplay
        self.error = Label(self, bd=0, fg='white', anchor='nw', text=self.err_msg, **kwargs)

        # packing labels
        self.error.pack(side='bottom', anchor='nw', fill='x')
        self.imglbl.pack(side='left', anchor='nw', fill='y', ipadx=8)
        self.entry.pack(anchor='nw', fill='both', expand=1)
        self.line.pack(anchor='nw', fill='x')
        # binnding
        self.entry.bind("<FocusIn>", self.F_in)
        self.entry.bind("<FocusOut>", self.F_out)

    def F_in(self, event):
        if self.Entry_var.get() == self.lbltext:
            pass
        else:
            self.error['text'] = ' '
            self.line['bg'] = 'black'

    def F_out(self, event):
        # if entry is empty
        if self.Entry_var.get().strip() == '':
            self.line['bg'] = 'red'
            self.error['text'] = '\tthis is required field'

class LoginPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        # change title
        self.master.title('Login System')
        # icons used
        self.bg = PhotoImage(file='g898.png')

        # main background image
        Label(self, image=self.bg).pack()

        # take id input and password
        self._id = LabeledEntry(self,'Your first name here.', '', 'users.png', **{'bg': '#221a1a'})
        self._id.place(x=40, y=300)
        self.psw = LabeledEntry(self, 'Password', '', 'users.png', **{'bg': '#221a1a'})
        self.psw.entry['show'] = '*'  # hiide typing charcters
        self.psw.place(x=40, y=390)
        # show password
        self.psw.entry.bind("<Button-3>", showPassword)
        # on release
        self.psw.entry.bind("<ButtonRelease-3>", hidePassword)
        # login button

        self.login_btn = Button(self, text='Login', font=('arial', 22), width=9, fg='#221a1a', bg='#ff443a',activebackground='#ff443a', bd=0)
        self.login_btn.place(x=3, y=490)
        # register button
        self.register_btn = Button(self, text='Register', font=('arial', 22), width=9, fg='#221a1a', bg='#ff443a',activebackground='#ff443a', bd=0)
        self.register_btn.place(x=305, y=568)

# register page interface for the app
class RegisterPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        # change title
        self.master.title('Register')
        # icons used
        self.bg = PhotoImage(file='g898.png')


        # main background image
        Label(self, image=self.bg).pack()

        # take id input and password
        default = {'bg': '#221a1a'}
        self.fname = LabeledEntry(self, 'First name', '', 'users.png', **default)
        # lower the width of entry
        self.fname.entry['width'] = 15
        self.fname.place(x=40, y=300)

        self.lanme = LabeledEntry(self, 'Last name', '', 'users.png', **default)
        # lower the width of entry
        self.lanme.entry['width'] = 15
        self.lanme.place(x=220, y=300)

        self.psw = LabeledEntry(self, 'Password', '', 'users.png', **default)
        # lower the width of entry
        self.psw.entry.config(width=15, show='*')
        self.psw.place(x=40, y=390)

        self.retype_psw = LabeledEntry(self, 'Retype password', '', 'users.png', **default)
        # lower the width of entry
        self.retype_psw.entry.config(width=15, show='*')
        self.retype_psw.place(x=220, y=390)
        # bind a function to hide or show password on right click
        # on press
        self.retype_psw.entry.bind("<Button-3>", showPassword)
        # on release
        self.retype_psw.entry.bind("<ButtonRelease-3>", hidePassword)

        # login button
        self.login_btn = Button(self, text='Login', font=('arial', 22), width=9, fg='#221a1a', bg='#ff443a',activebackground='#ff443a', bd=0)
        self.login_btn.place(x=3, y=490)
        # register button
        self.register_btn = Button(self, text='Register', font=('arial', 22), width=9, fg='#221a1a', bg='#ff443a',activebackground='#ff443a', bd=0)
        self.register_btn.place(x=305, y=568)

    def on_register(self):
        a = self.fname.Entry_var.get().strip()  # remove spaces before and after usinf strip()
        b = self.lanme.Entry_var.get().strip()  # remove spaces before and after usinf strip()
        c = self.psw.Entry_var.get().strip()  # remove spaces before and after usinf strip()
        d = self.retype_psw.Entry_var.get().strip()  # remove spaces before and after usinf strip()
        if a == b == c == d == '':
            mb.showinfo(message='All fields are required')
        elif c != d:
            mb.showinfo(message='Retyped password did not matched')
        else:
            db = sqlite3.connect("myDatabse.db")  # connect to databse

            # Qry_for_creating tables = """ CREATE TABLE Register(
            # Fname varchar(100),
            # Lname varchar(100),
            # Psw   varchar(100)
            #  )  """

            Qry = """INSERT INTO Register(Fname,Lname,Psw) VALUES(?,?,?)"""
            entry_vals = (a, b, c)

            cursor = db.cursor()  # create cursor
            cursor.execute(Qry, entry_vals)  # execute the query using the cursor
            db.commit()  # commit all changes to database

            ask = mb.askyesno(message='Regsitration was succesfull!', detail='Do you want to Login!')
            return ask

class mainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self["highlightthickness"]=0
        self.resizable(0,0) #no more adjustable window
        self.geometry('+350+0')
        #grid both pages at the same position
        self.register_page = RegisterPage(self)
        self.register_page.grid(row=0,column=0)
        #bind button functions
        self.register_page.login_btn['command']=self.goto_LoginPage
        self.register_page.register_btn['command']=self.on_registerPage_click_Register

        self.login_page = LoginPage(self)
        self.login_page.grid(row=0,column=0)
        #functins of button on the pages
        self.login_page.login_btn['command']=self.on_loginPage_click_Login
        self.login_page.register_btn['command']=self.goto_registerPage
        #add some warning
        self.login_page.psw.error['text']='\tpress and hold right key to show password'

    def goto_registerPage(self):
        #raise register_page up to the login
        self.register_page.tkraise()

    def goto_LoginPage(self):
        #return to login page
        self.login_page.tkraise()

    def on_registerPage_click_Register(self):
        #if user is on register page and clicks to regsiter btn
        result=self.register_page.on_register()
            # if result is true
        if result:
            self.goto_LoginPage()
        else:
            print('adding failed')

    def on_loginPage_click_Login(self):
        #if user is on login page and clicks to login btn
        a=self.login_page._id.Entry_var.get().strip()
        b=self.login_page.psw.Entry_var.get().strip()

        if a==b=='':
            #if fields are empty
            mb.showinfo(message='Fill all required fields')
        else:
            db=sqlite3.connect("myDatabse.db")#connect to databse
            cursor=db.cursor()#create cursor

            Qry="""SELECT * FROM Register WHERE Fname=? AND Psw=? """
            entry_vals=(a,b,)

            #execute the query using the cursor
            cursor.execute(Qry,entry_vals)
            #get db results
            db_res = cursor.fetchall()
            if db_res==[]:
                ask=mb.askyesno(message='We could not fine any results',detail='Do you want to register?')
                #if yes to register go to register page
                if ask:
                    self.goto_registerPage()
            else:
                self.destroy()
                Analysis()

def Analysis():
    global root
    root = Tk()
    root.geometry("465x708")
    root.resizable(False, False)
    root["bg"] = "#221a1a"
    root.title("Main Menue")

    Label(root, text="Welcome To Genetrix", bg="black", fg="white", font=("monospace", 20, "bold"), width=40, bd=4,relief=RIDGE).pack(side=TOP, fill=X)
    customtkinter.CTkButton(root, text="PREDICTED DATA", bd=0, height=50, width=285, text_color="#221a1a",fg_color="#ff443a", text_font=('arial', 22,),command=ProgressBarWindow).place(x=100, y=170)
    customtkinter.CTkButton(root, text="CLUSTERED DATA", bd=0, height=50, width=60, text_color="#221a1a",fg_color="#ff443a", text_font=('arial', 22),command=ClusterWindow).place(x=100, y=240)
    customtkinter.CTkButton(root, text="DATA ANALYSIS", bd=0, height=50, width=284, text_color="#221a1a",fg_color="#ff443a", text_font=('arial', 22),command=Graphs).place(x=100, y=310)
    customtkinter.CTkButton(root, text="ABOUT", bd=0, height=50, width=282, text_color="#221a1a", fg_color="#ff443a",text_font=('arial', 22), command=nextwindow).place(x=100, y=380)
    customtkinter.CTkButton(root, text="EXIT", bd=0, height=50, width=282, text_color="#221a1a", fg_color="#ff443a",text_font=('arial', 22), command=root.destroy).place(x=100, y=450)

    root.mainloop()

def ProgressBarWindow():
    root.destroy()
    ProgressBar()

def Graphs():
    root.destroy()
    global root2
    root2 = Tk()
    root2.geometry("540x708")
    root2.resizable(False, False)
    root2["bg"] = "#221a1a"
    root2.title("Genetrix")

    Label(root2, text="Welcome To Genetrix Plots", bg="black", fg="white", font=("monospace", 20, "bold"), width=40, bd=4,relief=RIDGE).pack(side=TOP, fill=X)
    customtkinter.CTkButton(root2, text="BARPLOT", bd=0, height=50, width=510, text_color="#221a1a",fg_color="#ff443a", text_font=('arial', 22,), command=BarPlot).place(x=18, y=170)
    customtkinter.CTkButton(root2, text="CLUSTERPLOT", bd=0, height=50, width=510, text_color="#221a1a",fg_color="#ff443a", text_font=('arial', 22),command=ClusterPlot).place(x=18, y=240)
    customtkinter.CTkButton(root2, text="CLUSTERS BASED ON LOCATIONS", bd=0, height=50, width=284, text_color="#221a1a",fg_color="#ff443a", text_font=('arial', 22),command=LocationPlot).place(x=18, y=310)
    customtkinter.CTkButton(root2, text="CLUSTERS BASED ON GENE NAME", bd=0, height=50, width=282, text_color="#221a1a", fg_color="#ff443a",text_font=('arial', 22),command=GenePlot).place(x=18, y=380)
    customtkinter.CTkButton(root2, text="BACK", bd=0, height=50, width=515, text_color="#221a1a", fg_color="#ff443a",text_font=('arial', 22), command=MainBack).place(x=18, y=450)

    root2.mainloop()

def MainBack():
    root2.destroy()
    Analysis()

def get_data_frame1():
    global df_a1
    global col
    file_name = askopenfilename()
    df_a1 = pd.read_csv(file_name)
    col = list(df_a1)
    print(col)

def get_data_frame2():
    global df_a2
    global col
    file_name = askopenfilename()
    df_a2 = pd.read_csv(file_name)
    col = list(df_a2)
    print(col)

def BarPlot():
    root2.destroy()
    def plot():
        # the figure that will contain the plot
        fig = Figure(figsize=(15, 6.7), dpi=100)
        df_a=df_a1
        df_a.head(2)

        df_v = df_a2
        df_v.head(2)

        df = pd.merge(df_a, df_v, left_index=True, right_index=True)
        df.head(2)

        location = df["Location"]
        location = pd.DataFrame(location)
        location = pd.DataFrame(location.value_counts().sort_index()).reset_index()
        location.columns = ["Location", "Total Cases"]
        # print(location.value_counts().sum)

        len(df_v.index)

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.bar(location["Location"], location["Total Cases"])
        plot1.set_title('Number of Mutations based on Location')
        plot1.set_xlabel('Location')
        plot1.set_ylabel('Number of Mutations')
        plot1.set_xticklabels(location["Location"], rotation=25, fontsize=6)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

    def BarplotBack():
        window.destroy()
        Analysis()


    # the main Tkinter window
    window = Tk()

    # setting the title
    window.title('Plotting in Tkinter')

    # dimensions of the main window
    window.geometry("1500x750")

    # button that displays the plot
    Button(master=window, command=get_data_frame1, height=2, width=10, text="Browse file 1").place(x=450,y=0)
    Button(master=window, command=get_data_frame2, height=2, width=10, text="Browse file 2").place(x=580,y=0)
    Button(master=window, command=plot, height=2, width=10, text="Plot").pack()
    Button(master=window, command=BarplotBack, height=2, width=10, text="Back").place(x=1300,y=0)

    # run the gui
    window.mainloop()

def get_data_frame3():
    global df_a3
    global col
    file_name = askopenfilename()
    df_a3 = pd.read_csv(file_name)
    col = list(df_a3)
    print(col)

def get_data_frame4():
    global df_a4
    global col
    file_name = askopenfilename()
    df_a4 = pd.read_csv(file_name)
    col = list(df_a4)
    print(col)

def ClusterPlot():
    root2.destroy()
    def plot():
        # the figure that will contain the plot
        fig = Figure(figsize=(15, 6.7), dpi=100)

        df_a = df_a3
        df_a.head(2)

        df_v = df_a4
        df_v.head(2)

        df = pd.merge(df_a, df_v, left_index=True, right_index=True)
        df.head(2)

        cluster = df["Cluster"]
        cluster = pd.DataFrame(cluster)
        cluster = pd.DataFrame(cluster.value_counts().sort_index()).reset_index()
        cluster.columns = ["Cluster", "Count"]
        cluster

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.bar(cluster["Cluster"], cluster["Count"])
        plot1.set_title('ClusterPlot')
        plot1.set_xlabel('Location')
        plot1.set_ylabel('Count')

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window3)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, window3)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
    def ClusterPlotBack():
        window3.destroy()
        Analysis()

    # the main Tkinter window
    window3 = Tk()

    # setting the title
    window3.title('Plotting in Tkinter')

    # dimensions of the main window
    window3.geometry("1500x750")

    # button that displays the plot
    Button(master=window3, command=get_data_frame3, height=2, width=10, text="Browse file 1").place(x=450,y=0)
    Button(master=window3, command=get_data_frame4, height=2, width=10, text="Browse file 2").place(x=580,y=0)
    Button(master=window3, command=plot, height=2, width=10, text="Plot").pack()
    Button(master=window3, command=ClusterPlotBack, height=2, width=10, text="Back").place(x=1300,y=0)

    # run the gui
    window3.mainloop()
def get_data_frame5():
    global df_a5
    global col
    file_name = askopenfilename()
    df_a5 = pd.read_csv(file_name)
    col = list(df_a5)
    print(col)

def get_data_frame6():
    global df_a6
    global col
    file_name = askopenfilename()
    df_a6 = pd.read_csv(file_name)
    col = list(df_a6)
    print(col)

def LocationPlot():
    root2.destroy()
    def plot():
        # the figure that will contain the plot
        fig = Figure(figsize=(15, 6.7), dpi=100)

        df_a = df_a5
        df_a.head(2)

        df_v = df_a6
        df_v.head(2)

        df = pd.merge(df_a, df_v, left_index=True, right_index=True)
        df.head(2)

        clus = df[(df["Cluster"] == 0) | (df["Cluster"] == 1) | (df["Cluster"] == 2) | (df["Cluster"] == 3)]
        clus.head(2)

        location_and_cluster = clus.groupby(["Location", "Cluster"])["Cluster"].agg(["count"]).reset_index()
        location_and_cluster

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.bar(location_and_cluster["Location"], location_and_cluster["count"])
        plot1.set_title('Mutations and Clusters based on location')
        plot1.set_xlabel('Location')
        plot1.set_ylabel('Mutations in each Cluster')
        plot1.set_xticklabels(location_and_cluster["Location"], rotation = 35, fontsize=7)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window4)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, window4)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
    def LocationPlotBack():
        window4.destroy()
        Analysis()

    # the main Tkinter window
    window4 = Tk()

    # setting the title
    window4.title('Plotting in Tkinter')

    # dimensions of the main window
    window4.geometry("1500x750")

    # button that displays the plot
    Button(master=window4, command=get_data_frame5, height=2, width=10, text="Browse file 1").place(x=450,y=0)
    Button(master=window4, command=get_data_frame6, height=2, width=10, text="Browse file 2").place(x=580,y=0)
    Button(master=window4, command=plot, height=2, width=10, text="Plot").pack()
    Button(master=window4, command=LocationPlotBack, height=2, width=10, text="Back").place(x=1300,y=0)

    # run the gui
    window4.mainloop()

def get_data_frame7():
    global df_a7
    global col
    file_name = askopenfilename()
    df_a7 = pd.read_csv(file_name)
    col = list(df_a7)
    print(col)

def get_data_frame8():
    global df_a8
    global col
    file_name = askopenfilename()
    df_a8 = pd.read_csv(file_name)
    col = list(df_a8)
    print(col)


def GenePlot():
    root2.destroy()
    def plot():
        # the figure that will contain the plot
        fig = Figure(figsize=(15, 6.7), dpi=100)

        df_a = df_a7
        df_a.head(2)

        df_v = df_a8
        df_v.head(2)

        df = pd.merge(df_a, df_v, left_index=True, right_index=True)
        df.head(2)

        clus = df[(df["Cluster"] == 0) | (df["Cluster"] == 1) | (df["Cluster"] == 2) | (df["Cluster"] == 3)]
        clus.head(2)

        location_and_cluster = clus.groupby(["Location", "Cluster"])["Cluster"].agg(["count"]).reset_index()
        location_and_cluster

        genename_and_cluster = clus.groupby(["Gene name", "Cluster"])["Cluster"].agg(["count"]).reset_index()
        genename_and_cluster

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.bar(genename_and_cluster["Gene name"], genename_and_cluster["count"])
        plot1.set_title('Mutation Clusters based on Gene name')
        plot1.set_xlabel('Gene name')
        plot1.set_ylabel('Mutations in each Cluster')
        plot1.set_xticklabels(genename_and_cluster["Gene name"], rotation=45, fontsize=6)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window5)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, window5)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
    def GenePlotBack():
        window5.destroy()
        Analysis()

    # the main Tkinter window
    window5 = Tk()

    # setting the title
    window5.title('Plotting in Tkinter')

    # dimensions of the main window
    window5.geometry("1500x750")

    # button that displays the plot
    Button(master=window5, command=get_data_frame7, height=2, width=10, text="Browse file 1").place(x=450,y=0)
    Button(master=window5, command=get_data_frame8, height=2, width=10, text="Browse file 2").place(x=580,y=0)
    Button(master=window5, command=plot, height=2, width=10, text="Plot").pack()
    Button(master=window5, command=GenePlotBack, height=2, width=10, text="Back").place(x=1300,y=0)

    # run the gui
    window5.mainloop()

def nextwindow():
    win = Tk()
    # Set the geometry of tkinter frame
    win.geometry("700x400")
    # Create a text widget and wrap by words
    text = Text(win, wrap=WORD)
    text.insert(INSERT,"SARS-CoV-2-Dashboard \n \n The rapid spread of the coronavirus disease 2019 (COVID19) pandemic, which was caused by the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) coronavirus, has resulted in 95,932,739 confirmed cases. As of January 20, 2021, there had been 2 054 853 cases and 2,054, 853 fatalities. In the twenty-first century, there have been three significant outbreaks of fatal pneumonia this century. SARS-CoV (2002), Middle East, caused by b-coronaviruses MERS-CoV (respiratory syndrome coronavirus) (2012), and SARS-CoV-2 is a virus that causes SARS (2019). Clustering is a Machine Learning Technique that involves the grouping of data points. Given a set of data points, researchers can use a clustering algorithm to classify each data point into a specific group. Creating mutation clusters which depend on certain features of the virus will be easier using clustering algorithms. There is much research conducted regarding mutation clustering (other types of viruses and diseases) following few of them directly regarding SARS CoV-2 mutations. In this research, researchers try to go beyond gene-based clustering of CoV-2 mutations to predict the manner Covid-19 mutates next using analytical techniques.")
    text.pack()
    win.mainloop()

def ProgressBar():
    class Root(Tk):
        def __init__(self):
            super(Root, self).__init__()
            self.title("Progress Bar")
            self.minsize(400, 100)

            self.buttonFrame = ttk.LabelFrame(self, text="")
            self.buttonFrame.place(x=150,y=80)
            self.progressBar()

        def progressBar(self):

            self.button1 = ttk.Button(self.buttonFrame, text = "Predict", command = self.run_progressbar)
            self.button1.grid(column =0, row = 0)
            self.progress_bar = ttk.Progressbar(self, orient = 'horizontal', length = 286, mode = 'determinate')
            self.progress_bar.place(x=60,y=50)

        def run_progressbar(self):
            def newwindow():
                root = Tk()
                root.geometry("465x708")
                root.resizable(False, False)
                root["bg"] = "#221a1a"
                root.title("Main Menue")
            self.progress_bar["maximum"] = 100

            for i in range(101):
                time.sleep(0.05)
                self.progress_bar["value"] = i
                self.progress_bar.update()
            self.destroy()
            newwindow()
            self.progress_bar["value"] = 0
    root = Root()
    root.mainloop()

def get_data_frame():
    global df
    global col
    file_name = askopenfilename()
    df = pd.read_csv(file_name)
    col = list(df)
    print(col)

def Cluster():
    def BackClustered():
        window.destroy()
        Analysis()
    class mclass:
        def __init__(self, window):
            self.window = window
            Button(window, text="Browse", command=get_data_frame,height=1,width=7).place(x=170,y=0)
            self.button3 = Button(window, text="Plot", command=self.plot,height=1,width=7).pack()

            self.fig = Figure(figsize=(6, 6))
            self.a = self.fig.add_subplot(111)
            Button(window, text="Back", command=BackClustered,height=1,width=7).place(x=500,y=0)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
            self.canvas.get_tk_widget().pack()


        def plot(self):
            self.a.cla()
            le = LabelEncoder()
            df["Isolate ID"] = le.fit_transform(df["Isolate ID"])

            km = KMeans(n_clusters=3)
            y_predicted = km.fit_predict(df[['Isolate ID', 'DNAENC']])
            df['cluster'] = y_predicted
            df1 = df[df.cluster == 0]
            df2 = df[df.cluster == 1]
            df3 = df[df.cluster == 2]


            self.a.scatter(df1['Isolate ID'], df1['DNAENC'], color='green',label='cluster1')
            self.a.scatter(df2['Isolate ID'], df2['DNAENC'], color='red', label='cluster2')
            self.a.scatter(df3['Isolate ID'], df3['DNAENC'], color='yellow', label='cluster3')

            self.a.set_title ("Scatter Plot", fontsize=16)
            self.a.set_ylabel("Y", fontsize=14)
            self.a.set_xlabel("X", fontsize=14)
            self.canvas.draw()

    window = Tk()
    start = mclass(window)
    window.mainloop()


def ClusterWindow():
    root.destroy()
    Cluster()

#run

App = mainApp()
App.mainloop()