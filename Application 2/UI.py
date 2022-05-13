import tkinter
from tkinter import *
import sqlite3
import tkinter.messagebox as mb
from tkinter import *
import sqlite3
import tkinter.messagebox as mb
from tkinter import filedialog

import customtkinter
import tk as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import pandas as pd

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
				Analysis()


def Analysis():
	global root
	root = Tk()
	root.geometry("465x708")
	root.resizable(False, False)
	root["bg"] = "#161C30"
	root.title("Main Menue")

	Label(root, text="Welcome To Genetrix", bg="black", fg="white", font=("monospace", 20, "bold"), width=40, bd=4,relief=RIDGE).pack(side=TOP, fill=X)
	customtkinter.CTkButton(root, text="PREDICTED DATA", bd=0, height=50, width=285, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22,)).place(x=100, y=170)
	customtkinter.CTkButton(root, text="CLUSTERED DATA", bd=0, height=50, width=60, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22)).place(x=100, y=240)
	customtkinter.CTkButton(root, text="DATA ANALYSIS", bd=0, height=50, width=284, text_color="#221a1a",fg_color="#ffffff", text_font=('arial', 22),command=Graphs).place(x=100, y=310)
	customtkinter.CTkButton(root, text="ABOUT", bd=0, height=50, width=282, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22), command=nextwindow).place(x=100, y=380)
	customtkinter.CTkButton(root, text="EXIT", bd=0, height=50, width=282, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22), command=root.destroy).place(x=100, y=450)

	root.mainloop()

def Graphs():
	root.destroy()
	global root2
	root2 = Tk()
	root2.geometry("540x708")
	root2.resizable(False, False)
	root2["bg"] = "#161C30"
	root2.title("Genetrix")

	Label(root2, text="Welcome To Genetrix Plots", bg="black", fg="white", font=("monospace", 20, "bold"), width=40, bd=4,relief=RIDGE).pack(side=TOP, fill=X)
	customtkinter.CTkButton(root2, text="BARPLOT", bd=0, height=50, width=510, text_color="#221a1a",fg_color="#ff443a", text_font=('arial', 22,), command=BarPlot).place(x=18, y=170)
	customtkinter.CTkButton(root2, text="CLUSTERPLOT", bd=0, height=50, width=510, text_color="#221a1a",fg_color="#ff443a", text_font=('arial', 22),command=ClusterPlot).place(x=18, y=240)
	customtkinter.CTkButton(root2, text="CLUSTERS BASED ON LOCATIONS", bd=0, height=50, width=284, text_color="#221a1a",fg_color="#ff443a", text_font=('arial', 22)).place(x=18, y=310)
	customtkinter.CTkButton(root2, text="CLUSTERS BASED ON GENE NAME", bd=0, height=50, width=282, text_color="#221a1a", fg_color="#ff443a",text_font=('arial', 22)).place(x=18, y=380)
	customtkinter.CTkButton(root2, text="BACK", bd=0, height=50, width=515, text_color="#221a1a", fg_color="#ff443a",text_font=('arial', 22), command=MainBack).place(x=18, y=450)

	root2.mainloop()

def MainBack():
	root2.destroy()
	Analysis()


def BarPlot():
	root2.destroy()
	def plot():
		# the figure that will contain the plot
		fig = Figure(figsize=(15, 6), dpi=100)

		df_a = pd.read_csv("output1.csv")
		df_a.head(2)

		df_v = pd.read_csv("output2.csv")
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
	plot_button = Button(master=window, command=plot, height=2, width=10, text="Plot")
	plot_button2 = Button(master=window, command=BarplotBack, height=2, width=10, text="Back")

	# place the button
	# in main window
	plot_button.pack()
	plot_button2.pack()
	# run the gui
	window.mainloop()

def ClusterPlot():
	root2.destroy()
	def plot():
		# the figure that will contain the plot
		fig = Figure(figsize=(15, 6), dpi=100)

		df_a = pd.read_csv("output1.csv")
		df_a.head(2)

		df_v = pd.read_csv("output2.csv")
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
	def BarplotBack():
		window3.destroy()
		Analysis()

	# the main Tkinter window
	window3 = Tk()

	# setting the title
	window3.title('Plotting in Tkinter')

	# dimensions of the main window
	window3.geometry("1500x750")

	# button that displays the plot
	plot_button = Button(master=window3, command=plot, height=2, width=10, text="Plot")
	plot_button2 = Button(master=window3, height=2, width=10, text="Back",command=BarplotBack)

	# place the button
	# in main window
	plot_button.pack()
	plot_button2.pack()
	# run the gui
	window3.mainloop()

def nextwindow():
	win = Tk()
	# Set the geometry of tkinter frame
	win.geometry("700x400")
	# Create a text widget and wrap by words
	text = Text(win, wrap=WORD)
	text.insert(INSERT,"SARS-CoV-2-Dashboard \n \n The rapid spread of the coronavirus disease 2019 (COVID19) pandemic, which was caused by the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) coronavirus, has resulted in 95,932,739 confirmed cases. As of January 20, 2021, there had been 2 054 853 cases and 2,054, 853 fatalities. In the twenty-first century, there have been three significant outbreaks of fatal pneumonia this century. SARS-CoV (2002), Middle East, caused by b-coronaviruses MERS-CoV (respiratory syndrome coronavirus) (2012), and SARS-CoV-2 is a virus that causes SARS (2019). Clustering is a Machine Learning Technique that involves the grouping of data points. Given a set of data points, researchers can use a clustering algorithm to classify each data point into a specific group. Creating mutation clusters which depend on certain features of the virus will be easier using clustering algorithms. There is much research conducted regarding mutation clustering (other types of viruses and diseases) following few of them directly regarding SARS CoV-2 mutations. In this research, researchers try to go beyond gene-based clustering of CoV-2 mutations to predict the manner Covid-19 mutates next using analytical techniques.")
	text.pack()
	win.mainloop()

#run

App = mainApp()
App.mainloop()