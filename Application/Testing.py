import PySimpleGUI as sg
import json, os, sys, smtplib, ssl, random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
import ctypes
import platform
import seaborn as sns

cov_mut=pd.read_csv('output1.csv',nrows=500)
cov_mut.head()


# ---------------- Front-End-Functions ----------------
# Login Interface
def win_Login():
    try:
        # Interface Layout
        Left_Column = [[sg.Text('Or Are you New User?'), sg.Text(' ' * 10)],
                       [sg.Text('Then'), sg.Button(' Sign Up ')]]

        Right_Column = [[sg.Text(' ' * 13), sg.Button(' Forget Email? ')]]

        layout = [[sg.Text('Email : '), sg.InputText(key='in1', do_not_clear=False)],
                  [sg.Text('Password : '), sg.InputText(key='in2', do_not_clear=False, password_char='*')],
                  [sg.Button(' Log In ')],
                  [sg.Text('_' * 60)],
                  [sg.Column(Left_Column), sg.VSeperator(), sg.Column(Right_Column)]]

        window = sg.Window('Login', layout, margins=(20, 40))
        # Defining Button Connections and Acceptable Data Logic
        event, values = window.Read()
        if (event == ' Log In '):
            email = str(values['in1'])

            Is_space = email.isspace()
            if not email:
                sg.Popup('No Input Data!!')
                window.close()
                win_Login()
            elif Is_space == True:
                sg.popup('Email Cannot contain Spaces!!')
                window.close()
                win_Login()
            elif Is_space == False:
                if email.endswith('@gmail.com') == False:
                    sg.Popup('Invalid Email!!')
                    window.close()
                    win_Login()
                else:
                    with open('datafile.py', 'r') as f:
                        dic = json.load(f)
                    gemail = list(dic.keys())[0]
                    if (email != gemail):
                        sg.Popup('Incorrect Email!!')
                        window.close()
                        win_Login()
                    elif (email == gemail):
                        passwd = str(values['in2'])
                        evalue = dic[email]
                        cr_pass = pass_decoder(evalue)
                        if (passwd.isspace() == True):
                            sg.Popup('Password cannot contain Spaces!!')
                            window.close()
                            win_Login()
                        elif passwd == cr_pass:
                            window.close()
                            win_Plots()
                        elif (passwd != cr_pass):
                            sg.Popup('Incorrect Password!!')
                            window.close()
                            win_Login()
                        else:
                            win_Invalid_Input()
                            window.close()
                            win_Login()
                    else:
                        window.close()
                        win_Login()
            else:
                sg.Popup('Something Went Wrong!!')
                window.close()
                win_Login()
        elif event == sg.WIN_CLOSED:
            window.close()
            i = False
            return i
        elif (event == ' Sign Up '):
            window.close()
            win_Signup()
            win_Login()
        elif (event == ' Forget Email? '):
            window.close()
            sec_ques_check()
        else:
            window.close()
            win_Login()
    except Exception as err:
        sg.Popup(err)
        win_Invalid_Input()
        window.close()
        win_Login()

def win_Plots():
    layout = [[
        sg.Frame(layout=[[sg.Button('HOME',size=(15, 2))],[sg.Button("PREDICTED DATA", size=(15, 2))],
                         [sg.Button("CLUSTERED DATA", size=(15, 2))],[sg.Button("DATA ANALYSIS", size=(15, 2))],
                         [sg.Button("COMMUNITY", size=(15, 2))],[sg.Button("ABOUT", size=(15, 2))]],title="Plots",relief=sg.RELIEF_GROOVE)]]
    window = sg.Window('APP name', layout, margins=(100, 50))
    while True:
        event, values = window.Read()
        if event == "HOME":
            window.close()
            win_Login()
        elif event == "PREDICTED DATA":
            sg.Popup('PREDICTED DATA page')
        elif event == "CLUSTERED DATA":
            window.close()
            # Functions to prevent GUI blurring
            def make_dpi_aware():
                if int(platform.release()) >= 8:
                    ctypes.windll.shcore.SetProcessDpiAwareness(True)

            make_dpi_aware()

            # Function for drawing
            def draw_figure(canvas, figure):
                figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
                figure_canvas_agg.draw()
                figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
                return figure_canvas_agg

            # Layout creation
            layout = [[sg.Text('Kmeans clustering of SARS-CoV-2 mutations')],
                      [sg.Text("Choose a file: "), sg.FileBrowse(key="-IN-", button_text='Import Dataset')],
                      [sg.Canvas(key='-CANVAS-')],
                      [sg.Button("Plot"), sg.Button("Clear")]]

            # Create a window. finalize=Must be True.
            window = sg.Window('Demo Application - Genetrix', layout, finalize=True,
                               element_justification='center', font='Monospace 18')

            # Create a fig for embedding.
            fig = plt.figure(figsize=(6, 5))
            ax = fig.add_subplot(111)
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
            # Event loop
            while True:
                event, values = window.read()
                print(event, values)
                print(values["-IN-"])
                # sg.Print(event, values)

                if event in (None, "Cancel"):
                    break

                elif event == "Plot":
                    df = pd.read_csv(values["-IN-"])
                    print(df.head())
                    le = LabelEncoder()
                    df["Isolate ID"] = le.fit_transform(df["Isolate ID"])
                    # df["DNAENC"] = le.fit_transform(df["DNAENC"])
                    plt.scatter(df['Isolate ID'], df.DNAENC)
                    plt.xlabel('Isolate ID')
                    plt.ylabel('DNAENC')
                    # plt.show()

                    km = KMeans(n_clusters=3)
                    y_predicted = km.fit_predict(df[['Isolate ID', 'DNAENC']])
                    y_predicted
                    df['cluster'] = y_predicted
                    km.cluster_centers_
                    df1 = df[df.cluster == 0]
                    df2 = df[df.cluster == 1]
                    df3 = df[df.cluster == 2]
                    ax.scatter(df1['Isolate ID'], df1['DNAENC'], color='green', label='cluster1')
                    fig_agg.draw()
                    ax.scatter(df2['Isolate ID'], df2['DNAENC'], color='red', label='cluster2')
                    fig_agg.draw()
                    ax.scatter(df3['Isolate ID'], df3['DNAENC'], color='yellow', label='cluster3')
                    fig_agg.draw()
                    ax.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='purple', marker='*',
                               label='centroid')
                    fig_agg.draw()

                elif event == "Clear":
                    ax.cla()
                    fig_agg.draw()

                elif event == sg.FileBrowse():
                    print(values["-IN-"])
            # close the window.
            window.close()
        elif event == "DATA ANALYSIS":
            window.close()
            win_Analysis()
        elif event == "PREDICTED DATA":
            sg.Popup('PREDICTED DATA page')
        elif event == "COMMUNITY":
            sg.Popup('COMMUNITY page')
        elif event == "ABOUT":
            sg.Popup('ABOUT page')
        else:
            break

def win_Analysis():
    layout = [[
        sg.Frame(layout=[[sg.Button('HOME',size=(15, 2))],[sg.Button("BARPLOT", size=(15, 2))],
                         [sg.Button("DISTPLOT", size=(15, 2))],[sg.Button("JOINTPLOT", size=(15, 2))],
                         [sg.Button("STRIPPLOT", size=(15, 2))]],title="Analysis",relief=sg.RELIEF_GROOVE)]]
    window = sg.Window('APP name', layout, margins=(100, 50))
    while True:
        event, values = window.Read()
        if event == "HOME":
            window.close()
            win_Login()
        elif event == "BARPLOT":
            sns.barplot(cov_mut['YYYY-MM-DD'], cov_mut['DNAENC'])
            plt.show()
        elif event == "DISTPLOT":
            sns.distplot(cov_mut['DNAENC'])
            plt.show()
        elif event == "JOINTPLOT":
            sns.jointplot(cov_mut['YYYY-MM-DD'], cov_mut['DNAENC'])
            plt.show()
        elif event == "STRIPPLOT":
            sns.stripplot(cov_mut['Location'], cov_mut['Isolate ID'])
            plt.show()
        else:
            break


# Signup Interface
def win_Signup():
    try:
        # Interface Layout
        layout = [[sg.Text('Enter Email : '), sg.InputText(key='in1', do_not_clear=False)],
                  [sg.Text('Create Password : '), sg.InputText(key='in2', password_char='*', do_not_clear=False)],
                  [sg.Text('ReEnter Password : '), sg.InputText(key='in3', password_char='*', do_not_clear=False)],
                  [sg.Button(' Sign Up ')]]

        window = sg.Window('Sign Up', layout, margins=(30, 50))
        # Backend Logic
        event, values = window.Read()
        if (event == ' Sign Up '):
            global email
            email = str(values['in1'])
            email = email.lower()
            passwd = str(values['in2'])
            rpasswd = str(values['in3'])
            if not passwd or not email:
                sg.Popup('Please Fill up all Entries!!')
                window.close()
                win_Signup()
            elif (email.isspace() == True) or (passwd.isspace() == True):
                sg.Popup('Space is not valid!!')
                window.close()
                win_Signup()
            elif email.endswith('@gmail.com') == False:
                sg.Popup('Invalid Email!!')
                window.close()
                win_Signup()
            elif (len(passwd) < 8):
                sg.Popup('Password Length must be of 8 charcters!!')
                window.close()
                win_Signup()
            elif (passwd == rpasswd):
                global passd
                passd = pass_encoder(passwd)
                window.close()
                last_step(True, email, passd)
            else:
                win_Error()
                window.close()
                win_Signup()
        elif event == sg.WIN_CLOSED:
            window.close()
            i = False
            return i
        else:
            window.close()
            win_Signup()
    except Exception as err:
        window.close()

# Security Setup Interface
def sec_ques_setup():
    # List of Security Questions
    q1 = 'What was the name of your Elementry/Primary School?'
    q2 = 'What is your Favorite place to go?'
    q3 = 'In What City were you born?'
    q4 = 'What is the name of your First Grade Teacher?'
    q5 = 'What is the first name of your Best Friend?'

    List = [q1, q2, q3, q4, q5]

    # Interface Layout
    layout = [[sg.Text('Just One More Step!!\n')],
              [sg.Text('Please choose any Security Question and write it Answer..\n')],
              [sg.Text('First Question : '), sg.OptionMenu(List, key='sq1')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in1')],
              [sg.Text('Second Question : '), sg.OptionMenu(List, key='sq2')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in2')],
              [sg.Text('Third Question : '), sg.OptionMenu(List, key='sq3')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in3')],
              [sg.Button(' Submit ')]]

    window = sg.Window('Security Setup', layout)
    # Backend Logic
    event, values = window.Read()
    if (event == ' Submit '):
        if (values['sq1'] != values['sq2']):  # you don't select same questions
            if (values['sq2'] != values['sq3']):
                if (values['sq1'] != values['sq3']):
                    if (not values['in1']) or (not values['in2']) or (not values['in3']):
                        sg.Popup('Answer Field cannot be Empty!!')
                        window.close()
                        sec_ques_setup()
                    elif ((values['in1'].isspace()) == False):
                        if ((values['in2'].isspace()) == False):
                            if ((values['in3'].isspace()) == False):
                                sq = {values['sq1']: values['in1'], values['sq2']: values['in2'],
                                      values['sq3']: values['in3']}
                                window.close()
                                return sq
                            else:
                                sg.Popup('Answer Field cannot be Empty!!')
                                window.close()
                                sec_ques_setup()
                        else:
                            sg.Popup('Answer Field cannot be Empty!!')
                            window.close()
                            sec_ques_setup()
                    else:
                        sg.Popup('Answer Field cannot be Empty!!')
                        window.close()
                        sec_ques_setup()
                else:
                    sec_Ques_Error()
                    window.close()
                    sec_ques_setup()
            else:
                sec_Ques_Error()
                window.close()
                sec_ques_setup()
        else:
            sec_Ques_Error()
            window.close()
            sec_ques_setup()
    elif (event == sg.WIN_CLOSED):
        sg.Popup("It's Compulsory to Setup Security Question")
        window.close()
        win_setup_Incomplete()
    else:
        sec_ques_setup()

# If you close the program accidentally while setup Process then next time it will start from where you left
def win_setup_Incomplete():
    # Interface Layout
    layout = [[sg.Text("You don't Proceed Next... If you want to setup later..")],
              [sg.Text('Then'), sg.Button(' Close ')],
              [sg.Text('')],
              [sg.Text('If you want to Setup Now..')],
              [sg.Text('Then'), sg.Button(' Continue ')]]

    window = sg.Window('Setup InComplete', layout)
    # Backend Logic
    event, values = window.Read()
    if (event == ' Close ' or event == sg.WIN_CLOSED):
        window.close()
        last_step(False, email, passd)
    elif (event == ' Continue '):
        window.close()
        sq = sec_ques_setup()
        last_step(True, email, passd, sq)
    else:
        window.close()
        win_setup_Incomplete()

# Checking Security Question
def sec_ques_check():
    with open('datafile.py', 'r') as f:
        dic = json.load(f)
    List = list(dic)
    List.pop(0)
    List.pop(-1)
    # Interface Layout
    layout = [[sg.Text('Please choose any Security question and write it Answer..\n')],
              [sg.Text('First Question : '), sg.OptionMenu(List, key='sq1')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in1')],
              [sg.Text('Second Question : '), sg.OptionMenu(List, key='sq2')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in2')],
              [sg.Text('Third Question : '), sg.OptionMenu(List, key='sq3')],
              [sg.Text('Enter Answer : '), sg.InputText(key='in3')],
              [sg.Button(' Submit ')]]

    window = sg.Window('Verifying', layout)
    # Backend Logic
    event, values = window.Read()
    if (event == sg.WIN_CLOSED):
        window.close()
    elif (values['sq1'] != values['sq2']):
        if (values['sq2'] != values['sq3']):
            if (values['sq1'] != values['sq3']):
                if (not str(values['in1'])) or (not str(values['in2'])) or (not str(values['in3'])):
                    window.close()
                    sg.Popup('Please Write the all Answers!!')
                    sec_ques_check()
                elif ((dic[values['sq1']]) == str(values['in1'])):
                    if ((dic[values['sq2']]) == str(values['in2'])):
                        if ((dic[values['sq3']]) == str(values['in3'])):
                            window.close()
                            win_Fuser()
                        else:
                            win_Incorrect_Ans()
                            window.close()
                            win_Login()
                    else:
                        win_Incorrect_Ans()
                        window.close()
                        win_Login()
                else:
                    win_Incorrect_Ans()
                    window.close()
                    win_Login()
            else:
                sec_Ques_Error()
                window.close()
                sec_ques_check()
        else:
            sec_Ques_Error()
            window.close()
            sec_ques_check()
    else:
        sec_Ques_Error()
        window.close()
        sec_ques_check()

# Forget Username Interface
def win_Fuser():
    email = get_email()
    # Interface Layout
    layout = [[sg.Text('Your Email is '), sg.Text(email)],
              [sg.Text('If not, then '), sg.Button(' Log In ')]]

    window = sg.Window('Account Recovery', layout)
    # Backend Logic
    event, values = window.Read()
    if (event == sg.WIN_CLOSED):
        window.close()
    elif (event == ' LogIn '):
        window.close()
        win_Login()
    else:
        window.close()
        win_Login()

# ---------------- Popup Windows --------------------

def win_Error():
    text = 'Password is not Matching.. Please ReEnter it!!'
    sg.Popup(text)


def win_Invalid_Input():
    text = 'Incorrect Password or Email!!'
    sg.Popup(text)


def win_successful_signup():
    text = 'Signed Up Successfully'
    sg.Popup(text)


def sec_Ques_Error():
    text = 'Security Questions Cannot be same!!'
    sg.Popup(text)

def win_confirm():
    text = 'Password Changed!!'
    text1 = 'Click OK to Login'
    sg.Popup(text, text1)

def win_Incorrect_Ans():
    text = 'Incorrect Answer!!'
    sg.Popup(text)

def win_UserAvailable():
    text = "Can't Sign Up Again. User Already Existed"
    sg.Popup(text)

# ----------------- Back-End-Functions -------------------

# Encoding Password
def pass_encoder(pss):
    evalue = []
    for char in pss:
        evalue.append(ord(char))
    return evalue

# Decoding Password
def pass_decoder(evalue):
    pss = ''
    for val in evalue:
        pss = pss + chr(val)
    return str(pss)


# Backup Setup Process
def win_choice():
    try:
        with open('datafile.py', 'a+') as f:
            f.close()
        fsize = os.path.getsize('datafile.py')
        if fsize == 0:
            win_Signup()
        else:
            with open('datafile.py', 'r') as f:
                data = json.load(f)
            if (data['sqs'] == True):
                win_Login()
            else:
                second_last_step()
                last_step(True, email, passd)
    except Exception as err:
        print(err)
        win_choice()

# Saving Security Questions
def last_step(res, *arg):
    l = []
    for a in arg:
        l.append(a)

    email = l[0]
    epass = l[1]

    if (res == True):
        sec_ques = sec_ques_setup()
        dic = {email: epass}
        dic.update(sec_ques)
        dic.update({'sqs': True})
        with open('datafile.py', 'w') as fl:
            json.dump(dic, fl)
        win_successful_signup()
        win_Login()
    elif (res == False):
        dic = {email: epass}
        dic.update({'sqs': False})
        with open('datafile.py', 'w') as f:
            json.dump(dic, f)

def second_last_step():
    with open('datafile.py') as f:
        dic = json.load(f)
    global email, passd
    email = list(dic.keys())[0]
    passd = list(dic.values())[0]

# Check User is available or not
def file_checker():
    try:
        fsize = os.path.getsize('datafile.py')
        if fsize == 0:
            pass
        else:
            win_UserAvailable()
            win_Login()
    except Exception as err:
        sg.Popup(err)

# getting email from file
def get_email():
    with open('datafile.py') as f:
        data = json.load(f)
    email = list(data)[0]
    return email

# -------------------------- Main Program -------------------------

i = True
while i:
    try:
        sg.theme('DarkBlue3')
        i = win_choice()
    except Exception as err:
        print(err)