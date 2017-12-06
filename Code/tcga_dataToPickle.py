# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 15:35:30 2017

@author: runan.yao
"""


import csv
import pickle

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


def fileLoad():
    DataSet = {}
    DataList = __loadData('tcga_data.csv', isNumericData = 'True')
    LabelList = __loadData('tcga_label.csv')
    #LabelList = __loadData('label.csv')
    
    for i in range(0, 9662):
        lb = LabelList[i][0]
        #if lb in ['small', 'minor', 'whole']:
            # meaning less label are removed from the tests
        #    continue
    
        if lb in DataSet.keys():
            DataSet[lb].append(DataList[i])
        else:
            DataSet[lb] = [DataList[i]]
    return DataSet

DataSet = fileLoad()
for label in DataSet.keys():
    with open('./data/tcga/pickledData/'+label+'.pkl', 'wb') as tr:
        pickle.dump(DataSet[label], tr, pickle.HIGHEST_PROTOCOL)

