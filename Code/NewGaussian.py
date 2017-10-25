# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 19:47:22 2017

@author: Student
"""

from sklearn.naive_bayes import GaussianNB
import numpy as np
import csv
import pickle

TrainingData = []
TrainingResult = []

TestSampleData = []
TestActualResult = []

def __loadData(dataFile):
    data = []
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        for row in datas:
            
            if row is None or len(row) == 0:
                continue
            
            data.append(row)
    return data

log = open('log.txt', 'w')
DataList = __loadData('data.csv')
LabelList = __loadData('label.csv')

log.write('Read Data rows:')
log.write(str(len(DataList)))


log.write('Read Label rows:')
log.write(str(len(LabelList)))

TestData = DataList[:100]
TestLabel = LabelList[:100] 
"""
log.write('TestDataPrinted')
print('TestDataPrinted')
print(TestData)
log.write('\r\n')
log.write('TestLabelPrinted')
print('TestLabelPrinted')
print(TestLabel)
log.write('\r\n')
"""
TrainingData = DataList[100:]
TrainingLabel = LabelList[100:]
"""
print(len(TrainingData))
print(len(TrainingData[0]))
print(len(TrainingLabel))
"""
testTraining = np.array(TrainingData).astype(np.float)
testlabeling = np.array(TrainingLabel)

model = GaussianNB() 
model.fit(testTraining,testlabeling)

log.write(model.predict(np.array(TestData).astype(np.float)))
log.write('\n')
for label in TestLabel:
    log.write(' ' + label[0])

with open('TrainingResult.pkl', 'wb') as tr:
    pickle.dump(model, tr, pickle.HIGHEST_PROTOCOL)

