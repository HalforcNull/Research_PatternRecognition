# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 10:08:50 2017

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

AdiposeData =[]

TrainingData = []
TrainingLabel = []

for i in range(0, 9662):
    if LabelList[i][0].lower() == 'adipose':
        AdiposeData.append(DataList[i])
    else:
        TrainingData.append(DataList[i])
        TrainingLabel.append(LabelList[i])

testTraining = np.array(TrainingData).astype(np.float)
testlabeling = np.array(TrainingLabel)

model = GaussianNB() 
model.fit(testTraining,testlabeling)

simlarityToSkin = []
log.write('\n Skin simlarity: \n')
for data in AdiposeData:
    score = model.score(np.array([data]).astype(np.float), ['skin'])
    simlarityToSkin.append(score)
    log.write(' ' + str(score))
    
simlarityToBreast = []
log.write('\n Breast simlarity: \n')
for data in AdiposeData:
    score = model.score(np.array([data]).astype(np.float), ['breast'])
    simlarityToBreast.append(score)
    log.write(' ' + str(score))
    
log.write('\n Skin simlarity mean: ')
log.write(str(np.mean(simlarityToSkin)))


log.write('\n Breast simlarity mean: ')
log.write(str(np.mean(simlarityToBreast)))



