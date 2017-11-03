# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:30:32 2017

@author: Student
"""

from sklearn.naive_bayes import GaussianNB
from scipy import stats
import numpy as np
import csv

def __loadData(dataFile):
    data = []
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        for row in datas:
            if row is None or len(row) == 0:
                continue

            data.append(row)
    return data

log = open('log_GETX_Training_Self_test_normalized.txt', 'w')

DataList = __loadData('gtex_data.csv')
LabelList = __loadData('label.csv')


#log.write(DataList)
#DataList = stats.threshold(DataList, threshmin=100, threshmax=None, newval=1.5)
#log.write(DataList)

#for data in DataList:
#     log.write(str(data))

testTraining = np.array(DataList).astype(np.float)
testTraining = stats.threshold(testTraining, threshmin=100, threshmax=None, newval=1)
testTraining = np.log(testTraining)

testlabeling = np.array(LabelList)

model = GaussianNB() 
model.fit(testTraining,testlabeling)

#log.write(model.predict(testTraining))
results = model.predict(testTraining)

i = 0
reports = []
for result in results:
    expectedLabel = LabelList[i][0]
    if result == expectedLabel:
        i = i+1
        continue
    report = [i, expectedLabel, result, model.score([testTraining[i]], [expectedLabel])]
    reports.append(report)
    i = i + 1
    
with open('reportAll.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(reports)

log.write('\n')
