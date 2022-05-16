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
from tkinter.ttk import Progressbar
import time
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tkinter.filedialog import askopenfilename
import customtkinter
import pandas as pd
from tkinter import ttk
import tkinter as tk
import csv
from keras.layers import LSTM, Dense
from keras.models import Sequential
from numpy import array
import time

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

        self.entry = Entry(self, bd=0, width=35, font=('', 12), textvariable=self.Entry_var, bg='#161C30',fg='white')
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
        self._id = LabeledEntry(self,'Your first name here.', '', 'users.png', **{'bg': '#161C30'})
        self._id.place(x=40, y=300)
        self.psw = LabeledEntry(self, 'Password', '', 'users.png', **{'bg': '#161C30'})
        self.psw.entry['show'] = '*'  # hiide typing charcters
        self.psw.place(x=40, y=390)
        # show password
        self.psw.entry.bind("<Button-3>", showPassword)
        # on release
        self.psw.entry.bind("<ButtonRelease-3>", hidePassword)
        # login button

        self.login_btn = Button(self, text='Login', font=('arial', 22), width=9, fg='#161C30', bg='#ffffff',activebackground='#ffffff', bd=0)
        self.login_btn.place(x=3, y=490)
        # register button
        self.register_btn = Button(self, text='Register', font=('arial', 22), width=9, fg='#161C30', bg='#ffffff',activebackground='#ffffff', bd=0)
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
        default = {'bg': '#161C30'}
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
        self.login_btn = Button(self, text='Login', font=('arial', 22), width=9, fg='#161C30', bg='#ffffff',activebackground='#ffffff', bd=0)
        self.login_btn.place(x=3, y=490)
        # register button
        self.register_btn = Button(self, text='Register', font=('arial', 22), width=9, fg='#161C30', bg='#ffffff',activebackground='#ffffff', bd=0)
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
    root["bg"] = "#161C30"
    root.title("Main Menue")

    Label(root, text="Welcome To Genetrix", bg="black", fg="white", font=("monospace", 20, "bold"), width=40, bd=4,relief=RIDGE).pack(side=TOP, fill=X)
    customtkinter.CTkButton(root, text="PREDICTED DATA", bd=0, height=50, width=285, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22,),command=PredictionWindow).place(x=100, y=170)
    customtkinter.CTkButton(root, text="CLUSTERED DATA", bd=0, height=50, width=60, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22),command=ClusterWindow).place(x=100, y=240)
    customtkinter.CTkButton(root, text="DATA ANALYSIS", bd=0, height=50, width=284, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22),command=Graphs).place(x=100, y=310)
    customtkinter.CTkButton(root, text="ABOUT", bd=0, height=50, width=282, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22), command=nextwindow).place(x=100, y=380)
    customtkinter.CTkButton(root, text="EXIT", bd=0, height=50, width=282, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22), command=root.destroy).place(x=100, y=450)

    root.mainloop()

def PredictionWindow():
    root.destroy()
    def Model():
        data = df
        data = data.drop('Isolate name', 1)
        data = data.drop('Isolate ID', 1)
        data = data.drop('Location', 1)

        data['YYYY-MM-DD'] = pd.to_datetime(data['YYYY-MM-DD'], errors='ignore')

        data = data.sort_values(by='YYYY-MM-DD')

        gene_names = data['Gene name'].unique()

        print(data.head())

        def encode_seq(gene_name):
            output_name = (gene_name).lower() + '.csv'
            temp_data = []
            for index, i in data.iterrows():
                genome_length = 0
                temp_list = []
                if i['Gene name'] == gene_name:
                    for j in range(len(i['Sequence'])):
                        if i['Sequence'][j] == 'A':
                            temp_list.append('0')
                        elif i['Sequence'][j] == 'T':
                            temp_list.append('1')
                        elif i['Sequence'][j] == 'G':
                            temp_list.append('2')
                        else:
                            temp_list.append('3')
                    temp_data.append(temp_list)
                    genome_length = len(temp_data[0])

                    if len(temp_list) < genome_length:
                        temp_data.pop()

            for i in range(len(temp_data)):
                temp_data[i] = ''.join([str(item) for item in temp_data[i]])

            temp_data = list(dict.fromkeys(temp_data))

            with open(output_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Index', 'Seq'])
                for i in range(len(temp_data)):
                    writer.writerow([i, temp_data[i]])

        def xy_split(encoded_text, iter):
            X = []
            y = []
            for i in range(len(encoded_text[iter]) - 3):
                # X.append([encoded_text[i].tolist(), encoded_text[i+1].tolist(), encoded_text[i+2].tolist()])
                # y.append(encoded_text[i+3].tolist())
                seq_x, seq_y = encoded_text[iter][i:i + 3], encoded_text[iter][i + 3]
                temp_x = list(seq_x)
                temp_y = list(seq_y)

                temp_x = [float(x) for x in temp_x]
                temp_y = [float(y) for y in temp_y]

                X.append(temp_x)
                y.append(temp_y)

            return X, y

        def generate_postional(gene_name):
            data = pd.read_csv(gene_name + '.csv')

            data_array = []

            for i in range(len(data['Seq'])):
                data_array.append(data['Seq'][i])

            data_array_vertical = []
            for i in range(len(data_array[0])):
                temp = []
                for j in range(len(data_array)):
                    temp.append(data_array[j][i])

                data_array_vertical.append(temp)

            for k in range(len(data_array_vertical)):
                data_array_vertical[k] = ''.join([str(item) for item in data_array_vertical[k]])

            return data_array_vertical

        def model_training(X, y):
            model = Sequential()
            model.add(LSTM(50, activation='relu', input_shape=(3, 1)))
            model.add(Dense(1))
            model.compile(optimizer='SGD', loss='mse')

            # print('X Shape: ', X.shape)
            # X = X.reshape((X.shape[0], X.shape[1], 1))

            global history
            history = model.fit(X[:-1], y[:-1], epochs=25, verbose=0)

            return model

        for i in range(len(gene_names)):

            print('gene: ', gene_names[i])
            encode_seq(gene_names[i])

            vertical = generate_postional(gene_names[i])

            seq = []
            for m in range(len(vertical)):
                print("\nIteration: ", m, " of ", len(vertical), '\n')
                X, y = xy_split(vertical, m)

                X = array(X)
                y = array(y)

                X = X.reshape((X.shape[0], X.shape[1], 1))
                history = 0

                model = model_training(X, y)
                x_input = X[-1]
                x_input = array(x_input)
                x_input = x_input.reshape((1, 3, 1))
                yhat = model.predict(x_input, verbose=0)

                seq.append(yhat)

            seq1 = []
            for k in range(len(seq)):
                seq1.append(round(seq[k].tolist()[0][0]))

            temp_list = []
            print('temp: ', temp_list)
            for j in range(len(seq1)):
                if seq1[j] == 0:
                    temp_list.append('A')
                elif seq1[j] == 1:
                    temp_list.append('T')
                elif seq1[j] == 2:
                    temp_list.append('G')
                else:
                    temp_list.append('C')
            final_seq = ''.join([str(item) for item in temp_list])
            print('final seq: ', final_seq)
            lbl.config(text="Sequence: " + final_seq)
            with open('predictions.txt', 'a') as f:
                string = gene_names[i] + ': ' + final_seq + '\n'
                f.write(string)

    def ProgressBar():
        class Root(Tk):
            def __init__(self):
                super(Root, self).__init__()
                self.title("Progress Bar")
                self.minsize(400, 100)
                self["bg"] = "#161C30"
                self.buttonFrame = ttk.LabelFrame(self, text="")
                self.buttonFrame.place(x=150, y=80)
                self.progressBar()
                self.run_progressbar()

            def progressBar(self):
                self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=286, mode='determinate')
                self.progress_bar.place(x=60, y=50)

            def run_progressbar(self):
                self.progress_bar["maximum"] = 100

                for i in range(101):
                    time.sleep(0.05)
                    self.progress_bar["value"] = i
                    self.progress_bar.update()
                self.destroy()
                Model()
                self.progress_bar["value"] = 0

        root = Root()
        root.mainloop()

    def SelectGene():
        global frame
        global lbl
        root.destroy()
        frame = tk.Tk()
        frame.title("TextBox Input")
        frame.geometry('350x170')
        frame["bg"] = "#161C30"
        def printInput():
            inp = inputtxt.get(1.0, "end-1c")
            lbl.config(text="Sequence: " + inp)
            print(inp)

        inputtxt = tk.Text(frame, height=1, width=20)

        inputtxt.pack()

        printButton = customtkinter.CTkButton(frame, text="Input", command=printInput)
        printButton.pack()
        ModelButton = customtkinter.CTkButton(frame, text="Predict", command=ProgressBar)
        ModelButton.place(x=116,y=75)
        ModelButtonBack = customtkinter.CTkButton(frame, text="Back", command=ModelBack)
        ModelButtonBack.place(x=116,y=115)

        lbl = tk.Label(frame, text="")
        lbl.pack()
        frame.mainloop()

    def DataSet():
        global df
        global root
        root = Tk()
        root.geometry("203x390")
        root["bg"] = "#161C30"
        style = ttk.Style()
        style.theme_use('clam')
        my_frame = Frame(root)  # create frame
        my_frame.pack(pady=20)
        my_tree = ttk.Treeview(my_frame)  # create treeview

        df = pd.read_csv(askopenfilename())  # path

        customtkinter.CTkButton(root, text="Select Gene", bd=0, height=50, width=180, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22,), command=SelectGene).pack()
        customtkinter.CTkButton(root, text="Back", bd=0, height=50, width=182, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22,), command=SelectGeneBack).place(x=10,y=330)
        my_tree["column"] = list(df.columns)  # setup new treeview
        my_tree["show"] = "headings"

        for column in my_tree["column"]:  # Loop thru column list
            my_tree.heading(column, text=column, anchor=CENTER)

        # put data in treeview
        df1 = df['Gene name'].drop_duplicates()
        for rows in df1:
            my_tree.insert("", "end", value=rows)

        my_tree.pack()  # pack the treeview finally
        root.mainloop()

    DataSet()

def ModelBack():
    frame.destroy()
    Analysis()

def SelectGeneBack():
    root.destroy()
    Analysis()

def Graphs():
    root.destroy()
    global root2
    root2 = Tk()
    root2.geometry("540x708")
    root2.resizable(False, False)
    root2["bg"] = "#161C30"
    root2.title("Genetrix")

    Label(root2, text="Welcome To Genetrix Plots", bg="black", fg="white", font=("monospace", 20, "bold"), width=40, bd=4,relief=RIDGE).pack(side=TOP, fill=X)
    customtkinter.CTkButton(root2, text="BARPLOT", bd=0, height=50, width=510, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22,), command=BarPlot).place(x=18, y=170)
    customtkinter.CTkButton(root2, text="CLUSTERPLOT", bd=0, height=50, width=510, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22),command=ClusterPlot).place(x=18, y=240)
    customtkinter.CTkButton(root2, text="CLUSTERS BASED ON LOCATIONS", bd=0, height=50, width=284, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22),command=LocationPlot).place(x=18, y=310)
    customtkinter.CTkButton(root2, text="CLUSTERS BASED ON GENE NAME", bd=0, height=50, width=282, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22),command=GenePlot).place(x=18, y=380)
    customtkinter.CTkButton(root2, text="BACK", bd=0, height=50, width=515, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22), command=MainBack).place(x=18, y=450)

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
        fig = Figure(figsize=(15, 5.75), dpi=100)
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
    window.geometry("1100x650")

    # button that displays the plot
    customtkinter.CTkButton(master=window, height=2, width=10, text="Browse file 1",command=get_data_frame1).place(x=280,y=0)
    customtkinter.CTkButton(master=window, height=2, width=10, text="Browse file 2",command=get_data_frame2).place(x=400,y=0)
    customtkinter.CTkButton(master=window, command=plot, height=2, width=10, text="Plot").pack()
    customtkinter.CTkButton(master=window, command=BarplotBack, height=2, width=10, text="Back").place(x=1000,y=0)

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
        fig = Figure(figsize=(15, 5.75), dpi=100)

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
    window3.geometry("1100x650")

    # button that displays the plot
    customtkinter.CTkButton(master=window3, height=2, width=10, text="Browse file 1",command=get_data_frame3).place(x=280,y=0)
    customtkinter.CTkButton(master=window3, height=2, width=10, text="Browse file 2",command=get_data_frame4).place(x=400,y=0)
    customtkinter.CTkButton(master=window3, command=plot, height=2, width=10, text="Plot").pack()
    customtkinter.CTkButton(master=window3, command=ClusterPlotBack, height=2, width=10, text="Back").place(x=1000,y=0)

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
    window4.geometry("1100x740")

    # button that displays the plot
    customtkinter.CTkButton(master=window4, height=2, width=10, text="Browse file 1",command=get_data_frame5).place(x=280,y=0)
    customtkinter.CTkButton(master=window4, height=2, width=10, text="Browse file 2",command=get_data_frame6).place(x=400,y=0)
    customtkinter.CTkButton(master=window4, command=plot, height=2, width=10, text="Plot").pack()
    customtkinter.CTkButton(master=window4, command=LocationPlotBack, height=2, width=10, text="Back").place(x=1000,y=0)

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
        fig = Figure(figsize=(15, 5.75), dpi=100)

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
    window5.geometry("1100x650")

    # button that displays the plot
    customtkinter.CTkButton(master=window5, height=2, width=10, text="Browse file 1",command=get_data_frame7).place(x=280,y=0)
    customtkinter.CTkButton(master=window5, height=2, width=10, text="Browse file 2",command=get_data_frame8).place(x=400,y=0)
    customtkinter.CTkButton(master=window5, command=plot, height=2, width=10, text="Plot").pack()
    customtkinter.CTkButton(master=window5, command=GenePlotBack, height=2, width=10, text="Back").place(x=1000,y=0)
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

def get_data_frame9():
    global df_a9
    global col
    file_name = askopenfilename()
    df_a9 = pd.read_csv(file_name)
    col = list(df_a9)
    print(col)

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
            customtkinter.CTkButton(window, text="Browse", command=get_data_frame,height=1,width=7).place(x=300,y=0)
            self.button3 = customtkinter.CTkButton(window, text="Plot", command=self.plot,height=1,width=7).pack()

            self.fig = Figure(figsize=(8, 6.3))
            self.a = self.fig.add_subplot(111)
            customtkinter.CTkButton(window, text="Back", command=BackClustered,height=1,width=7).place(x=740,y=0)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
            self.canvas.get_tk_widget().pack()

        def plot(self):
            self.a.cla()
            le = LabelEncoder()
            df["Gene name"] = le.fit_transform(df["Gene name"])

            scaler = MinMaxScaler()

            scaler.fit(df[['DNAENC']])
            df['DNAENC'] = scaler.transform(df[['DNAENC']])

            scaler.fit(df[['Gene name']])
            df['Gene name'] = scaler.transform(df[['Gene name']])

            km = KMeans(n_clusters=3)
            y_predicted = km.fit_predict(df[['Gene name', 'DNAENC']])
            df['cluster'] = y_predicted
            df1 = df[df.cluster == 0]
            df2 = df[df.cluster == 1]
            df3 = df[df.cluster == 2]

            self.a.scatter(df1['Gene name'], df1['DNAENC'], color='green',label='cluster1')
            self.a.scatter(df2['Gene name'], df2['DNAENC'], color='red', label='cluster2')
            self.a.scatter(df3['Gene name'], df3['DNAENC'], color='yellow', label='cluster3')
            self.a.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='purple', marker='*',label='centroid')

            self.a.set_title ("Scatter Plot", fontsize=16)
            self.a.set_ylabel("DNAENC", fontsize=14)
            self.a.set_xlabel("Gene name", fontsize=14)
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