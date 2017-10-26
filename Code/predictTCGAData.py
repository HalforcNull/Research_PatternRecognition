# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:14:19 2017

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
DataList = __loadData('gtex_data.csv')
LabelList = __loadData('label.csv')
TestData = __loadData('tcga_data.csv')

testTraining = np.array(DataList).astype(np.float)
testlabeling = np.array(LabelList)

model = GaussianNB() 
model.fit(testTraining,testlabeling)

log.write(model.predict(np.array(TestData).astype(np.float)))
log.write('\n')
