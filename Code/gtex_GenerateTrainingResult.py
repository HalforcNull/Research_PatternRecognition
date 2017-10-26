# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 20:37:49 2017

@author: Student
"""

from sklearn.naive_bayes import GaussianNB
import numpy as np
import csv
import pickle

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

testTraining = np.array(DataList).astype(np.float)
testlabeling = np.array(LabelList)

model = GaussianNB() 
model.fit(testTraining,testlabeling)

with open('gtex_TrainingResult.pkl', 'wb') as tr:
    pickle.dump(model, tr, pickle.HIGHEST_PROTOCOL)
