# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 08:49:12 2017

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

log = open('SkinDataMatchOthers.txt', 'w')
DataList = __loadData('gtex_data.csv')
LabelList = __loadData('label.csv')

log.write('Read Data rows:')
log.write(str(len(DataList)))


log.write('Read Label rows:')
log.write(str(len(LabelList)))

SkinData =[]

TrainingData = []
TrainingLabel = []

for i in range(0, 9662):
    if LabelList[i][0].lower() == 'skin':
        SkinData.append(DataList[i])
    else:
        TrainingData.append(DataList[i])
        TrainingLabel.append(LabelList[i])

testTraining = np.array(TrainingData).astype(np.float)
testlabeling = np.array(TrainingLabel)

model = GaussianNB() 
model.fit(testTraining,testlabeling)

simlarityToAdipose = []
log.write('\n Adipose simlarity: \n')
for data in SkinData:
    score = model.score(np.array([data]).astype(np.float), ['adipose'])
    simlarityToAdipose.append(score)
    log.write(' ' + str(score))
    
simlarityToBreast = []
log.write('\n Breast simlarity: \n')
for data in SkinData:
    score = model.score(np.array([data]).astype(np.float), ['breast'])
    simlarityToBreast.append(score)
    log.write(' ' + str(score))
    
log.write('\n Adipose simlarity mean: ')
log.write(str(np.mean(simlarityToAdipose)))


log.write('\n Breast simlarity mean: ')
log.write(str(np.mean(simlarityToBreast)))


log.write('\n Matching: \n')
log.write(model.predict(np.array(SkinData).astype(np.float)))



