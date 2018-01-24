# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:38:41 2018

@author: runan.yao
"""

import numpy as np
import itertools
import csv
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

log = open('splitData.txt', 'a')


log.write('===============  ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
log.write('===============  New Log Start by ' + 'Except One')

DataList = __loadData('gtex_data.csv', isNumericData = True)
LabelList = __loadData('label.csv')

LabelCount = {}
DataS = []
LabelS = []

for i in range(0, 9662):
    lb = LabelList[i][0]
    if lb in LabelCount.keys():
        if LabelCount[lb] < 100:
            DataS.append(DataList[i])
            LabelS.append(lb)
            LabelCount[lb] = LabelCount[lb] + 1
    else:
        LabelCount[lb] = 0

log.write('Data Load Finished.')
log.write(str(LabelCount))

with open('CuttedData.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(DataS)
    
with open('CuttedLabel.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(LabelS)    

log.write('Data is wrote')
