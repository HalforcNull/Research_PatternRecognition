# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:14:19 2017

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
    i = 0
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        for row in datas:
            if row is None or len(row) == 0:
                continue
            i = i + 1
            if i <= 5000:
                continue
            data.append(row)
    return data

log = open('TCGA-predict-log.txt', 'w')

TestData = __loadData('tcga_data.csv')

model = pickle.load( open( "gtex_TrainingResult.pkl", "rb" ) )

me = np.array(TestData).astype(np.float)

del(TestData)

log.write(model.predict(me))
log.write('\n')
