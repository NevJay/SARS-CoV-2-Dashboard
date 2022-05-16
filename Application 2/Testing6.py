from tkinter import *
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
        X= []
        y = []
        for i in range(len(encoded_text[iter]) - 3):
            # X.append([encoded_text[i].tolist(), encoded_text[i+1].tolist(), encoded_text[i+2].tolist()])
            # y.append(encoded_text[i+3].tolist())
            seq_x, seq_y = encoded_text[iter][i:i+3], encoded_text[iter][i+3]
            temp_x = list(seq_x)
            temp_y = list(seq_y)

            temp_x = [float(x) for x in temp_x]
            temp_y = [float(y) for y in temp_y]

            X.append(temp_x)
            y.append(temp_y)

        return X,y

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

        #print('X Shape: ', X.shape)
        #X = X.reshape((X.shape[0], X.shape[1], 1))

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
            X,y = xy_split(vertical, m)

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

            self.buttonFrame = ttk.LabelFrame(self, text="")
            self.buttonFrame.place(x=150,y=80)
            self.progressBar()
            self.run_progressbar()

        def progressBar(self):
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

def SelectGene():
    global lbl
    root.destroy()
    frame = tk.Tk()
    frame.title("TextBox Input")
    frame.geometry('400x200')

    def printInput():
        inp = inputtxt.get(1.0, "end-1c")
        lbl.config(text="Sequence: " + inp)
        print(inp)

    inputtxt = tk.Text(frame, height=1, width=20)

    inputtxt.pack()

    printButton = tk.Button(frame, text="Input", command=printInput)
    printButton.pack()
    ModelButton = tk.Button(frame, text="Predict", command=Model)
    ModelButton.pack()

    lbl = tk.Label(frame, text="")
    lbl.pack()
    frame.mainloop()

def DataSet():
    global df
    global root
    root=Tk()
    root.geometry("200x350")
    style = ttk.Style()
    style.theme_use('clam')
    my_frame = Frame(root)          #create frame
    my_frame.pack(pady=20)
    my_tree = ttk.Treeview(my_frame)            #create treeview

    df = pd.read_csv(askopenfilename())     #path

    customtkinter.CTkButton(root, text="Select Gene", bd=0, height=50, width=285, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22,),command=SelectGene).pack()
    customtkinter.CTkButton(root, text="Back", bd=0, height=50, width=285, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22,), command=root.destroy).pack()
    my_tree["column"] = list(df.columns)            #setup new treeview
    my_tree["show"] = "headings"

    for column in my_tree["column"]:  # Loop thru column list
        my_tree.heading(column, text=column, anchor=CENTER)

          #put data in treeview
    df1=df['Gene name'].drop_duplicates()
    for rows in df1:
        my_tree.insert("","end",value=rows)

    my_tree.pack()                  #pack the treeview finally
    root.mainloop()

DataSet()