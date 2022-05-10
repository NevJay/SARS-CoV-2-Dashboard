import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer as TFIDF
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score, confusion_matrix

from sklearn.model_selection import train_test_split, validation_curve, learning_curve
from sklearn.naive_bayes import MultinomialNB

def printMetrics(Y_test, Y_predicted):
    accuracy = accuracy_score(Y_test, Y_predicted)
    precision = precision_score(Y_test, Y_predicted, average='weighted')
    recall = recall_score(Y_test, Y_predicted, average='weighted')
    f1 = f1_score(Y_test, Y_predicted, average='weighted')
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", f1)

    return accuracy

#splitting sequence into KMers
def getKmers(sequence, size = 6):
    return [sequence[x:x+size].lower() for x in range(len(sequence) - size + 1)]

def train_model(data_set_size):
    data = pd.read_csv('output2.csv', nrows=data_set_size)

    print(data.head())



    #appending a kmer column to the dataframe

    data['kmer'] = data.apply(lambda x: getKmers(x['Sequence']), axis=1)
    print(data.head())

    #data = data.drop('Sequence', axis=1)

    #convert kmers to words

    textword = list(data["kmer"])

    for i in range(len(textword)):
        textword[i] = " ".join(textword[i])

    target = data.iloc[:, 0]

    #print(textword)

    cv = CountVectorizer()

    X_cv = cv.fit_transform(textword)

    kmers = cv.get_feature_names_out()

    print(pd.DataFrame(X_cv.toarray(), columns=kmers).head())

    vec = TFIDF()

    tfidf = vec.fit(textword)

    theX1 = tfidf.transform(textword)

    print(pd.DataFrame(theX1.toarray(), columns=kmers).head())

    transformer = TfidfTransformer()

    training_tfidf = transformer.fit_transform(X_cv)

    print(pd.DataFrame(training_tfidf.toarray(), columns=kmers).head())


    X_train, X_test, Y_train, Y_test = train_test_split(X_cv, target, test_size=0.2, random_state=420)
    # print("----------------------------X Test------------------------------")
    # print(X_test)




    classifier = MultinomialNB(alpha=0.1)
    classifier.fit(X_train, Y_train)

    y_pred = classifier.predict(X_test)
    print(y_pred)

    print(Y_test)
    print("Prediction Analysis")
    accuracy = printMetrics(Y_test, y_pred)

    return accuracy


def learning_curve():
    data_size = np.arange(10,10011, 1000)
    accuracy_array = []
    for i in range(len(data_size)):
        temp_acc = train_model(data_set_size= data_size[i])
        accuracy_array.append(temp_acc)
        print(len(data_size))
        print(len(accuracy_array))

    plt.plot(data_size, accuracy_array)
    plt.xlabel('No of DataPoints')
    plt.ylabel('Training Accuracy')
    plt.plot()
    plt.show()


learning_curve()