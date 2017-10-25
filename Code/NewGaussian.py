# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 19:47:22 2017

@author: Student
"""

from sklearn.naive_bayes import GaussianNB
import numpy as np
import csv

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

TestData = DataList[:20]
TestLabel = LabelList[:20] 

TrainingData = DataList[20:]
TrainingLabel = DataList[20:]

model = GaussianNB() 
model.fit(np.array(TrainingData).astype(np.float),np.array(TrainingLabel))

log.write(model.predict(np.array(TestData).astype(np.float)))
log.write(TestLabel)
