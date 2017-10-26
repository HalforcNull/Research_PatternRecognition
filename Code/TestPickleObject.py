# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 13:51:54 2017

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
#LabelList = __loadData('label.csv')

#testTraining = np.array(DataList).astype(np.float)

model = pickle.load( open( "gtex_TrainingResult.pkl", "rb" ) )
me = np.array(DataList).astype(np.float)

del(DataList)

log.write(model.predict(me))
log.write('\n')



