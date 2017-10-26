# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:49:08 2017

@author: Student
"""

DataFolder = 'C:\\Research_PatternRecognition\\Data\\'

def __loadData(dataFile):
    data = []
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        for row in datas:
            if row is None or len(row) == 0:
                continue
            data.append(row)
    return data

label = __loadData(DataFolder+'label.csv')
result = __loadData(DataFolder+'log_GETX_Training_Self_test.txt')

if len(label) != len(result):
    print('length not match')
    
same = 0
size = len(label)
for i in range(0, size):
    if label[i][0] == result[i][0]:
        same = same + 1
        
print(same)
print(size)


#print(str( same/(float)size) )        


