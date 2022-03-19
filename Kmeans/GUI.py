import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import KMeans
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Functions to prevent GUI blurring
def make_dpi_aware():
    import ctypes
    import platform
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
          [sg.Button("Process"), sg.Button("Plot"), sg.Button("Clear")]]

# Create a window. finalize=Must be True.
window = sg.Window('Demo Application - Genetrix', layout, size=(1000, 650), finalize=True,
                   element_justification='center', font='Monospace 18')

# Create a fig for embedding.
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111)
fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
# Event loop

def kMeans(df):
    print(df.head())
    le = LabelEncoder()
    df["Gene name"] = le.fit_transform(df["Gene name"])
    # df["DNAENC"] = le.fit_transform(df["DNAENC"])
    plt.scatter(df['Gene name'], df.DNAENC)
    plt.xlabel('Gene name')
    plt.ylabel('DNAENC')
    # plt.show()

    km = KMeans(n_clusters=4)
    y_predicted = km.fit_predict(df[['Gene name', 'DNAENC']])
    y_predicted
    df['cluster'] = y_predicted
    km.cluster_centers_
    df1 = df[df.cluster == 0]
    df2 = df[df.cluster == 1]
    df3 = df[df.cluster == 2]
    ax.scatter(df1['Gene name'], df1['DNAENC'], color='green', label='cluster1')
    fig_agg.draw()
    ax.scatter(df2['Gene name'], df2['DNAENC'], color='red', label='cluster2')
    fig_agg.draw()
    ax.scatter(df3['Gene name'], df3['DNAENC'], color='yellow', label='cluster3')
    fig_agg.draw()
    ax.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='purple', marker='*', label='centroid')
    fig_agg.draw()

def process(path):
    df = pd.read_csv(path)
    #df.drop(['Passage details/history', 'Type^^location/state','Host','Originating lab','Submitting lab','Submitter'], axis=1, inplace=True)
    df = df.filter(['Gene name', 'Isolate name','YYYY-MM-DD','Isolate ID','Location','Sequence'])
    pd.set_option('display.max_columns', None)
    print(df.head())
    list = df['Sequence'].tolist()
    sequence = df.iloc[:, 5:6].values
    list2 = []
    number = 0
    for j in range(len(list)):
        for i in range(len(list[j])):
            if list[j][i] == 'A':
                number += 1 * i
            if list[j][i] == 'T':
                number += 2 * i
            if list[j][i] == 'C':
                number += 3 * i
            if list[j][i] == 'G':
                number += 4 * i
        # number = str(number)
        list2.append(number / 1000)
        number = 0
    df['DNAENC'] = list2
    print(df.head())
    return df
while True:
    event, values = window.read()
    print(event, values)
    print(values["-IN-"])
    # sg.Print(event, values)

    if event in (None, "Cancel"):
        break
    elif event == "Process":
        try:
            df = process(values["-IN-"])
        except FileNotFoundError:
            print("First, import the dataset")

    elif event == "Plot":
        try:
            kMeans(df)
        except NameError:
            print("First, import the dataset, pre-process and then plot")

    elif event == "Clear":
        ax.cla()
        fig_agg.draw()

    elif event == sg.FileBrowse():
        print(values["-IN-"])
# close the window.
window.close()