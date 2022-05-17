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

gene_names=''
def Model():

    data = df
    data = data.drop('Isolate name', 1)
    data = data.drop('Isolate ID', 1)
    data = data.drop('Location', 1)

    data['YYYY-MM-DD'] = pd.to_datetime(data['YYYY-MM-DD'], errors='ignore')

    data = data.sort_values(by='YYYY-MM-DD')
    global gene_names
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
        print(i + 1, " ", gene_names[i])
    gene_index = inp-1

    print('gene: ', gene_names[gene_index])
    encode_seq(gene_names[gene_index])

    vertical = generate_postional(gene_names[gene_index])

    seq = []
    for m in range(len(vertical)):
        print(" Iteration: ", m, " of ", len(vertical), '\n')
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
    lbl.config(text="Sequence: " + final_seq +"\n")
    print('final seq: ', final_seq)

def ProgressBar():
    class Root(Tk):
        def __init__(self):
            super(Root, self).__init__()
            self.title("Progress Bar")
            self.minsize(400, 100)
            self.resizable(False, False)
            self["bg"] = "#161C30"
            self.buttonFrame = ttk.LabelFrame(self, text="")
            self.buttonFrame.place(x=150,y=80)
            self.progressBar()
            self.run_progressbar()

        def progressBar(self):
            self.progress_bar = ttk.Progressbar(self, orient = 'horizontal', length = 286, mode = 'determinate')
            self.progress_bar.place(x=60,y=50)

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

def ProgressBar1():

    root7 = Tk()
    root7.geometry("400x100")
    root7.resizable(False, False)
    root7["bg"] = "#161C30"
    root7.title("Genetrix")

    Label(root7, text="Please Enter a Integer of the Gene Name", bg="#161C30", fg="white", font=("monospace", 15, "bold"), width=40,bd=4).pack()
    customtkinter.CTkButton(root7, text="Cancel", bd=0, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22),command=root7.destroy).place(x=140,y=50)

    root7.mainloop()


def DataSet():
    global df
    global root6
    root6=Tk()
    root6.geometry("403x750")
    root6["bg"] = "#161C30"
    root6.resizable(False, False)
    style = ttk.Style()
    style.theme_use('clam')
    my_frame = Frame(root6)          #create frame
    my_frame.pack(pady=20)
    my_tree = ttk.Treeview(my_frame)            #create treeview

    df = pd.read_csv(askopenfilename())     #path

    customtkinter.CTkButton(root6, text="Back", bd=0,text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22,), command=root6.destroy).place(x=140,y=700)

    def printInput():
        global inp
        inp = int(inputtxt.get(1.0, "end-1c"))
        lbl.config(text="Sequence: " + str(inp))
        print(inp)

    Button(root6, text="Enter", bd=0,command=ProgressBar1).place(x=70,y=270)
    #tk.Label(root6, text="Enter Int:", height=1, width=10).place(x=40,y=270)
    customtkinter.CTkButton(root6, text="Input",bd=0,fg_color="#ffffff",text_color="#161C30",text_font=('arial', 22,), command=printInput).place(x=140,y=600)
    customtkinter.CTkButton(root6, text="Predict",bd=0,fg_color="#ffffff",text_color="#161C30",text_font=('arial', 22,), command=ProgressBar).place(x=140,y=650)
    inputtxt = tk.Text(root6, height=1, width=20)
    inputtxt.pack()
    global lbl
    lbl = tk.Label(root6, text="",height=20,width=55,wraplength=375)
    lbl.pack()

    my_tree["column"] = list(df.columns)            #setup new treeview
    my_tree["show"] = "headings"

          #put data in treeview
    df['YYYY-MM-DD'] = pd.to_datetime(df['YYYY-MM-DD'], errors='ignore')
    df = df.sort_values(by='YYYY-MM-DD')
    df1=df['Gene name'].unique()
    i=1
    for rows in df1:
        my_tree.insert("","end",value=str(i)+' '+rows)
        i=i+1

    my_tree.pack()                  #pack the treeview finally
    root6.mainloop()

DataSet()
