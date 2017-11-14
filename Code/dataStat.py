from sklearn.naive_bayes import GaussianNB
import numpy as np
import itertools
import csv
import pickle

DataSet = {}

def __loadData(dataFile):
    data = []
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        for row in datas:
            if row is None or len(row) == 0:
                continue
            data.append(row)
    return data

log = open('log-stat.txt', 'w')
DataList = __loadData('gtex_data.csv')
LabelList = __loadData('label.csv')

sumList = np.sum(np.array(DataList).astype(np.float), axis=0)

meanList_0 = np.mean(np.array(DataList).astype(np.float), axis=0)
meanList_1 = np.mean(np.array(DataList).astype(np.float), axis=1)

with open('stat-mean-0.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(meanList_0)
    
with open('stat-mean-1.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(meanList_1)
    
with open('stat-total.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(sumList)
