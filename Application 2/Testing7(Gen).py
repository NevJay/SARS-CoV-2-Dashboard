from tkinter import *
from tkinter.filedialog import askopenfilename
import customtkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import statsmodels.api as sm
import squarify

def Finish():
    win = Tk()

    win.geometry("700x250")
    Label(win, text="Click the button to Open Popup Window", font=('Helvetica 18')).place(relx=.5, rely=.5,anchor=CENTER)
    Button(win, text="Click Me", background="white", foreground="blue", font=('Helvetica 13 bold'),command=win.destroy).pack(pady=50)
    win.mainloop()

def Plotting():

    # Load data
    dat = df_a11
    dat.rename(columns = {'cluster':'Cluster'} , inplace = True)
    print(dat.shape)
    dat.head(5)

    df = dat[['Gene name','Isolate name','YYYY-MM-DD','Isolate ID','Location','DNAENC','Cluster']]

    location = df["Location"]
    location = pd.DataFrame(location)
    location = pd.DataFrame(location.value_counts().sort_index()).reset_index()
    location.columns = ["Location", "Total Cases"]

    cluster = dat["Cluster"]
    cluster = pd.DataFrame(cluster)
    cluster = pd.DataFrame(cluster.value_counts().sort_index()).reset_index()
    cluster.columns = ["cluster", "Count"]
    cluster

    clus = dat[(dat["Cluster"] == 0) |(dat["Cluster"] == 1) |(dat["Cluster"] == 2) |(dat["Cluster"] == 3)]

    x = df.apply(lambda x: x.factorize()[0]).corr()

    x.corr()

    def pairplot():
        plt.title("Overview of the Dataset")
        sns.set(rc = {'figure.figsize':(50,50)})
        sns.pairplot(x)
        plt.savefig(r'C:\Users\Ashen\SARS-CoV-2-Dashboard\Application 2\Plots\pairplot.png')

    # with regression
    def regression():
        plt.title("Overview with Regression applied")
        sns.set(rc = {'figure.figsize':(50,50)})
        sns.pairplot(x, kind="reg")
        plt.savefig(r'C:\Users\Ashen\SARS-CoV-2-Dashboard\Application 2\Plots\regression.png')


    def crosstab():
        sns.heatmap(pd.crosstab(df["Location"], df["Gene name"]),cmap="Greens")
        sns.set(rc = {'figure.figsize':(50,50)})
        plt.tight_layout()
        plt.title("Gene Distribution based on Country",fontsize=10,fontweight="bold")
        plt.savefig(r'C:\Users\Ashen\SARS-CoV-2-Dashboard\Application 2\Plots\crosstab.png')
        #plt.show()

    def mutationsXcountry():
        sns.set_style("whitegrid")
        plt.figure(figsize = (20, 20))

        location.drop(location[location['Total Cases'] < 200].index, inplace = True)
        plt.title("Mutation Distribution based on Country",fontsize=100,fontweight="bold")
        sns.barplot(x = "Location", y = "Total Cases", data = location)
        plt.title("Number of Mutations based on Location", size = 20)
        plt.xlabel("Location", size = 20)
        plt.ylabel("Number of Mutations", size = 20)
        plt.xticks(size = 15, rotation = 60)
        plt.yticks(size = 15)
        #plt.tight_layout()
        plt.savefig(r'C:\Users\Ashen\SARS-CoV-2-Dashboard\Application 2\Plots\mutationsXcountry.png')
        #plt.show()
        plt.xticks(rotation = -45)

    def timeXcases():
        date = df["YYYY-MM-DD"]
        date = pd.DataFrame(date)
        date = pd.DataFrame(date.value_counts().sort_index()).reset_index()
        date.columns = ["Date", "Total Cases"]
        #location["Total Cases"]
        date
        #print(location.value_counts().sum)

        #date.drop(date[date['Total Cases'] < 800].index, inplace = True)

        #plt.title("Total Cases Over Time",fontsize=100,fontweight="bold")
        plt.figure(figsize = (15, 15))
        sns.barplot(x = "Date", y = "Total Cases", data = date)
        plt.title("Total Cases Over Time", size = 20)
        plt.tick_params(left = True, bottom = False, labelleft = True ,
                    labelbottom = False)
        plt.tight_layout()
        plt.savefig(r'C:\Users\Ashen\SARS-CoV-2-Dashboard\Application 2\Plots\timeXcases.png')
        #plt.show()

    def Treemap():
        genename = df["Gene name"]
        genename = pd.DataFrame(genename)
        genename = pd.DataFrame(genename.value_counts().sort_index()).reset_index()
        genename.columns = ["Gene name", "Total Cases"]

        plt.figure(figsize = (100, 100))
        MEDIUM_SIZE = 200

        plt.title("Gene Distribution",fontsize=200,fontweight="bold")
        squarify.plot(sizes=genename['Total Cases'], label=genename['Gene name'], alpha=.8 , text_kwargs={'fontsize': 60}, color=sns.color_palette("flare"))
        plt.axis('off')
        plt.rc('font', size=MEDIUM_SIZE)
        #plt.show()
        plt.savefig(r'C:\Users\Ashen\SARS-CoV-2-Dashboard\Application 2\Plots\treemap.png')

    def clustercat():
        sns.set_style("whitegrid")
        plt.figure(figsize = (18, 7))
        sns.barplot(x = "cluster", y = "Count", data = cluster)
        plt.title("Clusters", size = 20)
        plt.xlabel("Clusters", size = 20)
        plt.ylabel("Count", size = 20)
        plt.xticks(size = 15, rotation = 0)
        plt.yticks(size = 15)
        #plt.xticks(rotation = -45)
        plt.savefig(r"C:\Users\Ashen\SARS-CoV-2-Dashboard\Application 2\Plots\raby.png")
        #plt.show()

    def clusterbyloc():

        location_and_cluster = clus.groupby(["Location", "Cluster"])["Cluster"].agg(["count"]).reset_index()

        location_and_cluster.drop(location_and_cluster[location_and_cluster['count'] < 20].index, inplace = True)

        plt.figure(figsize = (20, 20))
        #plt.legend(fontsize=20)
        sns.barplot(x = "Location", y = "count", hue = "Cluster", data = location_and_cluster)
        plt.title("Mutations and Clusters based on location", size = 20)
        plt.xlabel("Location", size = 20)
        plt.ylabel("Mutations in each Cluster", size = 20)
        plt.xticks(size = 15, rotation = 90)
        plt.yticks(size = 15)
        plt.savefig(r"C:\Users\Ashen\SARS-CoV-2-Dashboard\Application 2\Plots\clusterbyloc.png")

    def mutationsinclusters():
        genename_and_cluster = clus.groupby(["Gene name", "Cluster"])["Cluster"].agg(["count"]).reset_index()
        genename_and_cluster

        plt.figure(figsize = (18, 7))
        #plt.legend(fontsize=20)
        sns.barplot(x = "Gene name", y = "count", hue = "Cluster", data = genename_and_cluster)
        plt.title("Mutation Clusters based on Gene name", size = 20)
        plt.xlabel("Gene name", size = 20)
        plt.ylabel("Mutations in each Cluster", size = 20)
        plt.xticks(size = 15, rotation = 60)
        plt.yticks(size = 15)
        plt.savefig(r"C:\Users\Ashen\SARS-CoV-2-Dashboard\Application 2\Plots\mutationsinclusters.png")

    def other():
        crosstab()
        timeXcases()
        regression()
        pairplot()
        mutationsXcountry()
        Treemap()

    def cluss():
        clusterbyloc()
        mutationsinclusters()
        clustercat()

    other()
    cluss()
    Finish()
def get_data_frame11():
    global df_a11
    global col
    file_name = askopenfilename()
    df_a11 = pd.read_csv(file_name)
    col = list(df_a11)
    print(col)

def Graphs1():
    #root.destroy()
    global root2
    root2 = Tk()
    root2.geometry("480x708")
    root2.resizable(False, False)
    root2["bg"] = "#161C30"
    root2.title("Genetrix")

    Label(root2, text="Welcome To Genetrix Analysis", bg="black", fg="white", font=("monospace", 20, "bold"), width=40, bd=4,relief=RIDGE).pack(side=TOP, fill=X)
    customtkinter.CTkButton(root2, text="BROWSE", bd=0, height=50, width=250, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22),command=get_data_frame11).place(x=110, y=240)
    customtkinter.CTkButton(root2, text="ANALYSE", bd=0, height=50, width=250, text_color="#161C30",fg_color="#ffffff", text_font=('arial', 22),command=Plotting).place(x=110, y=310)
    customtkinter.CTkButton(root2, text="GENERATE", bd=0, height=50, width=250, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22)).place(x=110, y=380)
    customtkinter.CTkButton(root2, text="BACK", bd=0, height=50, width=250, text_color="#161C30", fg_color="#ffffff",text_font=('arial', 22), command="MainBack").place(x=110, y=450)

    root2.mainloop()

Graphs1()
