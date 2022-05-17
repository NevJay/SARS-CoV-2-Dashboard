import os.path
import csv

data_set_path = r'allnuc1115.fasta'
file_path = r'allnuc.csv'

def fasta_to_csv():
    if os.path.exists(file_path):
        with open(file_path, 'a') as file:
            with open(data_set_path, 'r') as data_set:

                for i in range(1):
                    print(i)
                    det = data_set.readline()
                    #print(det)
                    det = det[1:-1]
                    seq = data_set.readline()
                    #print(seq)
                    seq = seq[:-2]
                    temp_record =  det + '|' + seq
                    sliced_record = str(temp_record).split('|')
                    print(sliced_record)
                    print(len(sliced_record))
                    writer.writerow(sliced_record)
                    #print('Target: ', 1000000,'      Count: ', i)

    else:
        with open(file_path, 'w') as file:
            writer = csv.writer(file)
            #writer.writerow('\n')
            writer.writerow(['Gene name','Isolate name','YYYY-MM-DD','Isolate ID','Passage details/history','Type^^location/state','Host','Originating lab','Submitting lab','Submitter','Location','Sequence'])
            #writer.writerow('\n')
            print("File Created")
            fasta_to_csv()

def fasta_to_csv1():
    with open(file_path, 'a') as file:
        with open(data_set_path, 'r') as data_set:
            writer = csv.writer(file)
            writer.writerow(['Gene name', 'Isolate name', 'YYYY-MM-DD', 'Isolate ID', 'Passage details/history',
                             'Type^^location/state', 'Host', 'Originating lab', 'Submitting lab', 'Submitter',
                             'Location', 'Sequence'])

            for i in range(5000000):
                det = data_set.readline()
                #print(det)
                det = det[1:-1]
                seq = data_set.readline()
                #print(seq)
                seq = seq[:-2]
                temp_record =  det + '|' + seq
                sliced_record = str(temp_record).split('|')
                #print(sliced_record)
                #print(len(sliced_record))
                writer.writerow(sliced_record)
                print('Target: ', 5000000,'      Count: ', i)

fasta_to_csv1()