# -*- coding: utf-8 -*-
"""
Data picklization
Created on Tue Dec 05 13:43:42 2017
@author: runan.yao
"""

import csv
import pickle
import numpy as np

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
    DataList = __loadData('gtex_data.csv', isNumericData = True)
    LabelList = __loadData('gtex_label.csv')
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

def normalization(sample):
    """one sample pass in"""
    sample = sample + 100
    # 2^20 = 1048576
    return np.log2(sample * 1048576/np.sum(sample))

DataSet = fileLoad()
for label in DataSet.keys():
    with open('./data/gtex/pickledNormalizedData/'+label+'.pkl', 'wb') as tr:
        t = np.array(DataSet[label]).astype(np.float)
        pickle.dump(normalization(t), tr, pickle.HIGHEST_PROTOCOL)

