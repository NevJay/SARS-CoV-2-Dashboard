import PySimpleGUI as sg
from sqlite3 import connect
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

# ---- APPLICATION GUI LAYOUT ---------------------------------------------- #
main_layout = [
    [sg.Text('What do you want to do?')],
    [sg.Button('login', size=(8,1)), sg.Button('sign-up', size=(8,1))]]

login_layout = [
    [sg.Text('username'), sg.Input(key='username')],
    [sg.Text('password'), sg.Input(password_char='*', key='password')],
    [sg.Button('login', bind_return_key=True)]]

signup_layout = [
    [sg.Text('username'), sg.Input(key='username')],
    [sg.Text('email'), sg.Input(key='email')],
    [sg.Text('password'), sg.Input(password_char='*', key='password')],
    [sg.Button('sign-up', bind_return_key=True)]]

main_window = sg.Window('Main Menu', main_layout, element_justification='center')
login_window = sg.Window('Login', login_layout, element_justification='right')
signup_window = sg.Window('Create Account', signup_layout, element_justification='right')

# ---- APPLICATION FUNCTIONS ------------------------------------------------#
def create_db():
    ''' create database if one does not already exist '''
    with connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)")


def login(values):
    ''' obtain user credentials and validate against database '''
    with connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test WHERE username = ? AND password = ?", (values['username'], values['password']))
        check = len(cursor.fetchall())
        # login if credentials are found, otherwise alert user
    if check == 1:
        login_window.close()
        win_Plots()
    else:
        sg.popup_error('Invalid username or password')


def signup(values):
    ''' create user accounts based on supplied parameters, if account does not already exist '''
    with connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test WHERE username = ?", (values['username'],))
        check = len(cursor.fetchall())
        # add to database if not existing, otherwise alert user
        print(check)
        if check == 0:
            cursor.execute("INSERT INTO test VALUES(NULL, ?, ?, ?)", (values['username'], values['email'], values['password']))
            sg.popup('Username {} has been created'.format(values['username']))
        else:
            sg.popup_error('Username {} already exists'.format(values['username']))




def win_Plots():
    layout = [[
        sg.Frame(layout=[[sg.Button('EXIT',size=(15, 2))],[sg.Button("PREDICTED DATA", size=(15, 2))],
                         [sg.Button("CLUSTERED DATA", size=(15, 2))],[sg.Button("DATA ANALYSIS", size=(15, 2))],
                         [sg.Button("COMMUNITY", size=(15, 2))],[sg.Button("ABOUT", size=(15, 2))]],title="Plots",relief=sg.RELIEF_GROOVE)]]
    window = sg.Window('APP name', layout, margins=(100, 50))
    while True:
        event, values = window.Read()
        if event == "EXIT":
            window.close()
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
        sg.Frame(layout=[[sg.Button('EXIT',size=(15, 2))],[sg.Button("BARPLOT", size=(15, 2))],
                         [sg.Button("DISTPLOT", size=(15, 2))],[sg.Button("JOINTPLOT", size=(15, 2))],
                         [sg.Button("STRIPPLOT", size=(15, 2))]],title="Analysis",relief=sg.RELIEF_GROOVE)]]
    window = sg.Window('APP name', layout, margins=(100, 50))
    while True:
        event, values = window.Read()
        if event == "EXIT":
            window.close()
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



# ---- MAIN EVENT LOOP ----------------------------------------------------- #
create_db()

while True:
    event, values = main_window.read()
    if event in (None, 'Cancel'):
        break
    if event == 'login':
        main_window.close()
        log_event, log_values = login_window.read()
        if log_event == 'login':
            login(log_values)
            break
    if event == 'sign-up':
        main_window.close()
        sign_event, sign_values = signup_window.read()
        if sign_event == 'sign-up':
            signup(sign_values)
            break



