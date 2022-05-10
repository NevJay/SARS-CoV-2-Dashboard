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
from pathlib import Path
import warnings
from fontTools.otlLib.optimize.gpos import Cluster
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def make_window(theme):
    sg.theme(theme)
    layout = [[sg.Text('Please Select A Theme')],[sg.Combo(sg.theme_list(), default_value=theme, enable_events=True, key='-THEMES-')],[sg.Button('ok')]]

    return sg.Window('Main', layout, finalize=True,size=(200,100))

def theme():
    window = make_window('Python')
    while True:             # Event Loop
        event, values = window.read()
        if values['-THEMES-']:
            window.close()
            window = make_window(values['-THEMES-'])
        if event=='ok':
            window.close()
            # ---- APPLICATION GUI LAYOUT ---------------------------------------------- #
            # sg.theme('Dark2')
            main_layout = [[sg.Text('What do you want to do?')],
                           [sg.Button('sign-up', size=(8, 1)), sg.Button('login', size=(8, 1))]]

            login_layout = [
                [sg.Text('username'), sg.Input(key='username')],
                [sg.Text('password'), sg.Input(password_char='*', key='password')],
                [sg.Button('sign-up'), sg.Button('login', bind_return_key=True)]]

            signup_layout = [
                [sg.Text('username'), sg.Input(key='username')],
                [sg.Text('email'), sg.Input(key='email')],
                [sg.Text('password'), sg.Input(password_char='*', key='password')],
                [sg.Button('Login'), sg.Button('sign-up', bind_return_key=True)]]

            main_window = sg.Window('Main Menu', main_layout, element_justification='center', size=(250, 80))
            login_window = sg.Window('Login', login_layout, element_justification='right')
            signup_window = sg.Window('Create Account', signup_layout, element_justification='right')

            # ---- APPLICATION FUNCTIONS ------------------------------------------------#
            def create_db():
                ''' create database if one does not already exist '''
                with connect('users.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)")

            def login(values):
                ''' obtain user credentials and validate against database '''
                with connect('users.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM test WHERE username = ? AND password = ?",
                                   (values['username'], values['password']))
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
                        cursor.execute("INSERT INTO test VALUES(NULL, ?, ?, ?)",
                                       (values['username'], values['email'], values['password']))
                        sg.popup('Username {} has been created'.format(values['username']))
                    else:
                        sg.popup_error('Username {} already exists'.format(values['username']))

            def win_Plots():
                layout = [[
                    sg.Frame(layout=[[sg.Button("PREDICTED DATA", size=(15, 2))],
                                     [sg.Button("CLUSTERED DATA", size=(15, 2))],
                                     [sg.Button("DATA ANALYSIS", size=(15, 2))],
                                     [sg.Button("ABOUT", size=(15, 2))], [sg.Button('EXIT', size=(15, 2))]],
                             title="Please Select One", relief=sg.RELIEF_GROOVE)]]
                window = sg.Window('Genetrix', layout, margins=(100, 50))
                while True:
                    event, values = window.Read()
                    if event == "EXIT":
                        window.close()
                    elif event == "PREDICTED DATA":
                        window.close()
                        # set the theme for the screen/window
                        sg.theme("LightBlue")
                        # define layout
                        layout = [[sg.ProgressBar(50, orientation='h', size=(20, 20), border_width=4, key='progbar',
                                                  bar_color=['Red', 'Green'])]]
                        # Define Window
                        window = sg.Window("Progress Bar", layout)
                        # Read  values entered by user
                        i = 0
                        k = 15
                        val = 0
                        for i in range(k):
                            event, values = window.read(timeout=100)
                            # update prograss bar value
                            val = val + 100 / (k - i)
                            window['progbar'].update_bar(val)
                        window.close()
                        sg.Popup("Predicted Data")
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
                                  [sg.Button("Plot"), sg.Button("Clear"), sg.Button("Back")]]

                        # Create a window. finalize=Must be True.
                        window = sg.Window('Demo Application - Genetrix', layout, finalize=True,
                                           element_justification='center', font='Monospace 18')

                        # Create a fig for embedding.
                        fig = plt.figure(figsize=(10, 5))
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
                                plt.scatter(df['Isolate ID'], df.DNAENC)
                                plt.xlabel('Isolate ID')
                                plt.ylabel('DNAENC')

                                km = KMeans(n_clusters=3)
                                y_predicted = km.fit_predict(df[['Isolate ID', 'DNAENC']])
                                df['cluster'] = y_predicted
                                df1 = df[df.cluster == 0]
                                df2 = df[df.cluster == 1]
                                df3 = df[df.cluster == 2]
                                ax.scatter(df1['Isolate ID'], df1['DNAENC'], color='green', label='cluster1')
                                fig_agg.draw()
                                ax.scatter(df2['Isolate ID'], df2['DNAENC'], color='red', label='cluster2')
                                fig_agg.draw()
                                ax.scatter(df3['Isolate ID'], df3['DNAENC'], color='yellow', label='cluster3')
                                fig_agg.draw()
                                ax.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='purple',
                                           marker='*',
                                           label='centroid')
                                fig_agg.draw()

                            elif event == "Back":
                                window.close()
                                win_Analysis()

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
                    elif event == "ABOUT":
                        filename = 'hello.txt'
                        if Path(filename).is_file():
                            try:
                                with open(filename, "rt", encoding='utf-8') as f:
                                    text = f.read()
                                popup_text(filename, text)
                            except Exception as e:
                                print("Error: ", e)

                    else:
                        break

            def win_Analysis():
                layout = [[
                    sg.Frame(layout=[[sg.Button("BARPLOT", size=(15, 2))],
                                     [sg.Button("CLUSTERPLOT", size=(15, 2))],
                                     [sg.Button("CLUSTERS BASED ON LOCATIONS", size=(15, 2))],
                                     [sg.Button("CLUSTERS BASED ON GENE NAME", size=(15, 2))],
                                     [sg.Button('BACK', size=(15, 2))]], title="Analysis", relief=sg.RELIEF_GROOVE)]]
                window = sg.Window('Genetrix', layout, margins=(100, 50))
                while True:
                    event, values = window.Read()
                    if event == "BACK":
                        window.close()
                        win_Plots()
                    elif event == "BARPLOT":
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
                        layout = [[sg.Text('BarPlot of SARS-CoV-2 mutations')],
                                  [sg.Text("Choose a file: "),
                                   sg.FileBrowse(key="-IN-", button_text='Import Dataset 1')],
                                  [sg.Text("Choose a file: "),
                                   sg.FileBrowse(key="-IN2-", button_text='Import Dataset 2')],
                                  [sg.Canvas(key='-CANVAS-')],
                                  [sg.Button("Plot"), sg.Button("Clear"), sg.Button("Back")]]

                        # Create a window. finalize=Must be True.
                        window = sg.Window('Demo Application - Genetrix', layout, finalize=True,
                                           element_justification='center', font='Monospace 18')

                        # Create a fig for embedding.
                        fig = plt.figure(figsize=(17, 8))
                        ax = fig.add_subplot(111)
                        fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
                        # Event loop
                        while True:
                            event, values = window.read()
                            print(event, values)
                            print(values["-IN-"])
                            print(values["-IN2-"])
                            # sg.Print(event, values)

                            if event in (None, "Cancel"):
                                break

                            elif event == "Plot":
                                df_a = pd.read_csv(values["-IN-"])
                                df_a.head(2)
                                df_v = pd.read_csv(values["-IN2-"])
                                df_v.head(2)
                                df = pd.merge(df_a, df_v, left_index=True, right_index=True)
                                df.head(2)

                                location = df["Location"]
                                location = pd.DataFrame(location)
                                location = pd.DataFrame(location.value_counts().sort_index()).reset_index()
                                location.columns = ["Location", "Total Cases"]
                                len(df_v.index)

                                sns.set_style("whitegrid")
                                sns.barplot(x="Location", y="Total Cases", data=location)
                                plt.title("Number of Mutations based on Location", size=20)
                                plt.xlabel("Location", size=20)
                                plt.ylabel("Number of Mutations", size=20)
                                plt.xticks(size=10, rotation=45)
                                plt.yticks(size=15)
                                plt.savefig("raby.png")
                                fig_agg.draw()

                            elif event == "Clear":
                                ax.cla()
                                fig_agg.draw()

                            elif event == "Back":
                                window.close()
                                win_Analysis()

                            elif event == sg.FileBrowse():
                                print(values["-IN-"])
                        # close the window.
                        window.close()
                    elif event == "CLUSTERPLOT":
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
                        layout = [[sg.Text('CLUSTERPLOT of SARS-CoV-2 mutations')],
                                  [sg.Text("Choose a file: "),
                                   sg.FileBrowse(key="-IN-", button_text='Import Dataset 1')],
                                  [sg.Text("Choose a file: "),
                                   sg.FileBrowse(key="-IN2-", button_text='Import Dataset 2')],
                                  [sg.Canvas(key='-CANVAS-')],
                                  [sg.Button("Plot"), sg.Button("Clear"), sg.Button("Back")]]

                        # Create a window. finalize=Must be True.
                        window = sg.Window('Demo Application - Genetrix', layout, finalize=True,
                                           element_justification='center', font='Monospace 18')

                        # Create a fig for embedding.
                        fig = plt.figure(figsize=(17, 8))
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
                                df_a = pd.read_csv(values["-IN-"])
                                df_a.head(2)
                                df_v = pd.read_csv("output2.csv")
                                df_v.head(2)
                                df = pd.merge(df_a, df_v, left_index=True, right_index=True)
                                df.head(2)
                                location = df["Location"]
                                location = pd.DataFrame(location)
                                location = pd.DataFrame(location.value_counts().sort_index()).reset_index()
                                location.columns = ["Location", "Total Cases"]

                                len(df_v.index)
                                cluster = df["Cluster"]
                                cluster = pd.DataFrame(cluster)
                                cluster = pd.DataFrame(cluster.value_counts().sort_index()).reset_index()
                                cluster.columns = ["Cluster", "Count"]

                                sns.set_style("whitegrid")
                                sns.barplot(x="Cluster", y="Count", data=cluster)
                                plt.title("Clusters", size=20)
                                plt.xlabel("Clusters", size=20)
                                plt.ylabel("Count", size=20)
                                plt.xticks(size=15, rotation=0)
                                plt.yticks(size=15)
                                plt.savefig("raby.png")
                                fig_agg.draw()



                            elif event == "Clear":
                                ax.cla()
                                fig_agg.draw()

                            elif event == "Back":
                                window.close()
                                win_Analysis()

                            elif event == sg.FileBrowse():
                                print(values["-IN-"])
                        # close the window.
                        window.close()
                    elif event == "CLUSTERS BASED ON LOCATIONS":
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
                        layout = [[sg.Text('CLUSTERS BASED ON LOCATIONS of SARS-CoV-2 mutations')],
                                  [sg.Text("Choose a file: "),
                                   sg.FileBrowse(key="-IN-", button_text='Import Dataset 1')],
                                  [sg.Text("Choose a file: "),
                                   sg.FileBrowse(key="-IN2-", button_text='Import Dataset 2')],
                                  [sg.Canvas(key='-CANVAS-')],
                                  [sg.Button("Plot"), sg.Button("Clear"), sg.Button("Back")]]

                        # Create a window. finalize=Must be True.
                        window = sg.Window('Demo Application - Genetrix', layout, finalize=True,
                                           element_justification='center', font='Monospace 18')

                        # Create a fig for embedding.
                        fig = plt.figure(figsize=(17, 8))
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
                                df_a = pd.read_csv(values["-IN-"])
                                df_a.head(2)
                                df_v = pd.read_csv("output2.csv")
                                df_v.head(2)
                                df = pd.merge(df_a, df_v, left_index=True, right_index=True)
                                df.head(2)
                                location = df["Location"]
                                location = pd.DataFrame(location)
                                location = pd.DataFrame(location.value_counts().sort_index()).reset_index()
                                location.columns = ["Location", "Total Cases"]

                                len(df_v.index)
                                cluster = df["Cluster"]
                                cluster = pd.DataFrame(cluster)
                                cluster = pd.DataFrame(cluster.value_counts().sort_index()).reset_index()
                                cluster.columns = ["Cluster", "Count"]

                                clus = df[(df["Cluster"] == 0) |
                                          (df["Cluster"] == 1) |
                                          (df["Cluster"] == 2) |
                                          (df["Cluster"] == 3)]
                                clus.head(2)
                                location_and_cluster = clus.groupby(["Location", "Cluster"])["Cluster"].agg(
                                    ["count"]).reset_index()
                                sns.barplot(x="Location", y="count", hue="Cluster", data=location_and_cluster)
                                plt.title("Mutations and Clusters based on location", size=20)
                                plt.xlabel("Location", size=20)
                                plt.ylabel("Mutations in each Cluster", size=20)
                                plt.xticks(size=9, rotation=45)
                                plt.yticks(size=15)
                                plt.savefig("mah.png")
                                fig_agg.draw()

                            elif event == "Clear":
                                ax.cla()
                                fig_agg.draw()

                            elif event == "Back":
                                window.close()
                                win_Analysis()

                            elif event == sg.FileBrowse():
                                print(values["-IN-"])
                        # close the window.
                        window.close()
                    elif event == "CLUSTERS BASED ON GENE NAME":
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
                        layout = [[sg.Text('CLUSTERS BASED ON GENE NAME of SARS-CoV-2 mutations')],
                                  [sg.Text("Choose a file: "),
                                   sg.FileBrowse(key="-IN-", button_text='Import Dataset 1')],
                                  [sg.Text("Choose a file: "),
                                   sg.FileBrowse(key="-IN2-", button_text='Import Dataset 2')],
                                  [sg.Canvas(key='-CANVAS-')],
                                  [sg.Button("Plot"), sg.Button("Clear"), sg.Button("Back")]]

                        # Create a window. finalize=Must be True.
                        window = sg.Window('Demo Application - Genetrix', layout, finalize=True,
                                           element_justification='center', font='Monospace 18')

                        # Create a fig for embedding.
                        fig = plt.figure(figsize=(17, 8))
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
                                df_a = pd.read_csv(values["-IN-"])
                                df_a.head(2)
                                df_v = pd.read_csv("output2.csv")
                                df_v.head(2)
                                df = pd.merge(df_a, df_v, left_index=True, right_index=True)
                                df.head(2)
                                location = df["Location"]
                                location = pd.DataFrame(location)
                                location = pd.DataFrame(location.value_counts().sort_index()).reset_index()
                                location.columns = ["Location", "Total Cases"]

                                len(df_v.index)
                                cluster = df["Cluster"]
                                cluster = pd.DataFrame(cluster)
                                cluster = pd.DataFrame(cluster.value_counts().sort_index()).reset_index()
                                cluster.columns = ["Cluster", "Count"]

                                clus = df[(df["Cluster"] == 0) |
                                          (df["Cluster"] == 1) |
                                          (df["Cluster"] == 2) |
                                          (df["Cluster"] == 3)]
                                clus.head(2)
                                genename_and_cluster = clus.groupby(["Gene name", "Cluster"])["Cluster"].agg(
                                    ["count"]).reset_index()
                                sns.barplot(x="Gene name", y="count", hue="Cluster", data=genename_and_cluster)
                                plt.title("Mutation Clusters based on Gene name", size=20)
                                plt.xlabel("Gene name", size=20)
                                plt.ylabel("Mutations in each Cluster", size=20)
                                plt.xticks(size=15, rotation=60)
                                plt.yticks(size=15)
                                plt.savefig("mah.png")
                                fig_agg.draw()

                            elif event == "Back":
                                window.close()
                                win_Analysis()

                            elif event == "Clear":
                                ax.cla()
                                fig_agg.draw()

                            elif event == sg.FileBrowse():
                                print(values["-IN-"])
                        # close the window.
                        window.close()
                    else:
                        break

            def popup_text(filename, text):

                layout = [
                    [sg.Multiline(text, size=(80, 25)), ],
                ]
                win = sg.Window(filename, layout, modal=True, finalize=True)

                while True:
                    event, values = win.read()
                    if event == sg.WINDOW_CLOSED:
                        break
                win.close()

            # ---- MAIN EVENT LOOP ----------------------------------------------------- #
            create_db()

            def main():
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
                        elif log_event == 'sign-up':
                            login_window.close()
                            sign_event, sign_values = signup_window.read()
                    if event == 'sign-up':
                        main_window.close()
                        sign_event, sign_values = signup_window.read()
                        if sign_event == 'sign-up':
                            signup(sign_values)
                            break
                        elif sign_event == 'Login':
                            signup_window.close()
                            log_event, log_values = login_window.read()
            main()
theme()