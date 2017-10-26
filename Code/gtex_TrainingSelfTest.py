# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:30:32 2017

@author: Student
"""

from sklearn.naive_bayes import GaussianNB
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

log = open('log_GETX_Training_Self_test.txt', 'w')

DataList = __loadData('gtex_data.csv')
LabelList = __loadData('label.csv')

testTraining = np.array(DataList).astype(np.float)
testlabeling = np.array(LabelList)

model = GaussianNB() 
model.fit(testTraining,testlabeling)

log.write(model.predict(testTraining))
log.write('\n')
