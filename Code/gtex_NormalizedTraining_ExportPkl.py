# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 09:53:15 2017

@author: runan.yao
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

def normalization(sample):
    """one sample pass in"""
    sample = sample + 100
    # 2^20 = 1048576
    return np.log2(sample * 1048576/np.sum(sample))

log = open('log.txt', 'w')

DataList = __loadData('gtex_data.csv')
LabelList = __loadData('label.csv')

testTraining = np.array(DataList).astype(np.float)
testTraining = np.apply_along_axis(normalization, 1, testTraining )

testlabeling = np.array(LabelList)

model = GaussianNB() 
model.fit(testTraining,testlabeling)

with open('gtex_TrainingNormalizedResult.pkl', 'wb') as tr:
    pickle.dump(model, tr, pickle.HIGHEST_PROTOCOL)
