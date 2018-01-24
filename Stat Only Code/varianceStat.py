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


def topGeneCalc( name ,dataF, labelF, opDataF, logSys):
    DataList = __loadData(dataF, isNumericData = True)
    LabelList = __loadData(labelF)

    LabelCount = {}
    DataS = []
    LabelS = []

    for i in range(0, 9662):
        lb = LabelList[i][0]
        if lb in LabelCount.keys():
            if LabelCount[lb] < 70:
                DataS.append(DataList[i])
                LabelS.append(lb)
                LabelCount[lb] = LabelCount[lb] + 1
        else:
            LabelCount[lb] = 0

    logSys.write('Data Load Finished.')
    myvar = np.var(DataS, axis = 0)
    myav = np.mean(DataS, axis = 0)
    myavsq = np.multiply(myav, myav)
    myr = np.divide(myvar, myavsq)                      # variance / average^2

    with open(opDataF, 'w') as csvFile:
        wr = csv.writer(csvFile)
        wr.writerow(myr)

    s = np.argsort(myr)                                 # sort and get the index
    s = s[::-1]

    myr[s[120]]                                         # gtex, 120 gene is enough to 
    logSys.write( 'top 120 of ' + name + ' is: ' + str(s[120]))


log = open('consoleTest.txt', 'a')
topGeneCalc('gtex', 'gtex_data.csv', 'gtex_label.csv', 'gtex.detailed.result.csv', log)
topGeneCalc('tcga', 'tcga_data.csv', 'tcga_label.csv', 'tcga.detailed.result.csv', log)

