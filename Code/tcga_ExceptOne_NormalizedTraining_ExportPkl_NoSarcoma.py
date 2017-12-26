# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 15:14:29 2017

@author: runan.yao
"""

from sklearn.naive_bayes import GaussianNB
import numpy as np
import itertools
import csv
import pickle
import datetime

DataSet = {}

def __loadData(dataFile, isNumericData = False):
    data = []
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        for row in datas:
            if row is None or len(row) == 0:
                continue
            if isNumericData:
                data.append(map(float,row))
            else:
                data.append(row)        
    return data

def normalization(sample):
    """one sample pass in"""
    sample = sample + 100
    # 2^20 = 1048576
    return np.log2(sample * 1048576/np.sum(sample))

log = open('excludeOneTCGAlog.txt', 'a')


log.write('===============  ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
log.write('===============  New Log Start by ' + 'Except One')

DataList = __loadData('tcga_data.csv', isNumericData = True)
LabelList = __loadData('tcga_label.csv')

for i in range(0, 9662):
    lb = LabelList[i][0]
    if lb == 'Sarcoma':
        continue
    if lb in DataSet.keys():
        DataSet[lb].append(DataList[i])
    else:
        DataSet[lb] = [DataList[i]]

log.write('Data Load Finished.')

labels = DataSet.keys()

#for i in range( 0, 10 ):
#    l = labels[i]
for l in labels:
    model = GaussianNB() 
    log.write('building pickle for: ' + l + ' excluded.' )
    Data = []
    Label = []
    for j in labels:
        if l != j:
            Data = Data + DataSet[j]
            Label = Label + [j] * len(DataSet[j])
            
    testTraining = np.array(Data).astype(np.float)
    # do normalization here
    testTraining = np.apply_along_axis(normalization, 1, testTraining )
    testlabeling = np.array(Label)
    model.fit(testTraining,testlabeling)

    with open('./normalizedmodel/tcga/excludeOne/NoSarcoma/'+l+'.pkl', 'wb') as tr:
        pickle.dump(model, tr, pickle.HIGHEST_PROTOCOL)

