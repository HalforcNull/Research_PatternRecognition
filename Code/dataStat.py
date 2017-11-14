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

sumList = np.sum(np.array(DataList).astype(np.float), axis=1)

meanList = np.mean(np.array(DataList).astype(np.float))

with open('stat-mean.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(meanList)
    
with open('stat-total.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(sumList)
