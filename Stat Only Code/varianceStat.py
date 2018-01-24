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

def normalization(sample):
    """one sample pass in"""
    sample = sample + 100
    # 2^20 = 1048576
    return np.log2(sample * 1048576/np.sum(sample))


def outputDataS(name, DataS, logSys):
    myvar = np.var(DataS, axis = 0)
    myav = np.mean(DataS, axis = 0)
    myavsq = np.multiply(myav, myav)
    myr = np.divide(myvar, myavsq)                      # variance / average^2

    # with open(opDataF, 'w') as csvFile:
    #     wr = csv.writer(csvFile)
    #     wr.writerow(myr)

    s = np.argsort(myr)                                 # sort and get the index
    s = s[::-1]

    #myr[s[120]]                                         # gtex, 120 gene is enough to 
    logSys.write( 'top 120 of ' + name + ' is: ' + str(s[1:120]))
    logSys.write( 'the last one is: ' + str(myr[s[120]])) 
    return s[1:120]


def topGeneCalc( name ,dataF, labelF, opDataF, procType, logSys):
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

    if procType == 1:
        return outputDataS("orginal " + name, DataS, logSys)       # original
    elif procType == 2:                 
        DS = np.array(DataSet).astype(np.float)      #np array
        return outputDataS("np array" + name, DS, logSys)
    else:
        DS = np.array(DataSet).astype(np.float)
        return outputDataS("normalized" + name, DS, normalization(DS))
    


log = open('consoleTest.txt', 'a')
gtex1 = topGeneCalc('gtex', 'gtex_data.csv', 'gtex_label.csv', 'gtex.detailed.result.csv', 1, log)
tcga1 = topGeneCalc('tcga', 'tcga_data.csv', 'tcga_label.csv', 'tcga.detailed.result.csv', 1, log)

gtex2 = topGeneCalc('gtex', 'gtex_data.csv', 'gtex_label.csv', 'gtex.detailed.result.csv', 2, log)
tcga2 = topGeneCalc('tcga', 'tcga_data.csv', 'tcga_label.csv', 'tcga.detailed.result.csv', 2, log)

gtex3 = topGeneCalc('gtex', 'gtex_data.csv', 'gtex_label.csv', 'gtex.detailed.result.csv', 3, log)
tcga3 = topGeneCalc('tcga', 'tcga_data.csv', 'tcga_label.csv', 'tcga.detailed.result.csv', 3, log)

BothGtex = set(gtex1) & set(gtex2) & set(gtex3)
BothTcga = set(tcga1) & set(tcga2) & set(tcga3)

log.write( '\r\n' )
log.write( str(len(BothGtex)) + ' genes in all gtex, they are: ' + str(BothGtex))
log.write( '\r\n' )
log.write( str(len(BothTcga)) + ' genes in all tcga, they are: ' + str(BothTcga))



# BothGtexTcga1 = set(gtex1) & set(tcga1)
# EitherGtexTcga1 = set(gtex1) | set(tcga1)
# log.write( '\r\n' )
# log.write( str(len(BothGtexTcga)) + ' genes in both, they are: ' + str(BothGtexTcga))
# log.write( '\r\n' )
# log.write( str(len(EitherGtexTcga)) + ' genes in either, they are: ' + str(EitherGtexTcga))
