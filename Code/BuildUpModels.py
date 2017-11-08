# -*- coding: utf-8 -*-
"""
Created on Tue Nov 07 09:39:17 2017

@author: Student
"""

from sklearn.naive_bayes import GaussianNB
import numpy as np
import csv

DataSet = {}

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

for i in range(0, 9662):
    lb = LabelList[i][0]
    if lb in DataSet.keys():
        DataSet[lb].Append(DataList[i])
    else:
        DataSet[lb] = [DataList[i]]

labels = DataSet.keys()



