import numpy as np
import itertools
import csv
import datetime
from os import listdir
from os.path import isfile, isdir, join

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
        DS = np.array(DataSet)     #np array
        return outputDataS("np array" + name, DS, logSys)
    else:
        DS = np.array(DataSet)
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

log.write('===============  ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
log.write('===============  New Log Start by ' + 'cell line')

dataFolder = '/home/yaor/research/human_matrix_cell_line/'
tumorList = listdir(dataFolder)
DataSet = []
LabelCount = {}
sampleCount = 0
for t in tumorList:
    if not isdir(t): 
        log.write(t + ' is not a folder.')
    subList = listdir(join(dataFolder, t))
    for f in subList:
        LabelCount[t+'.'+f] = 0
        fullFile = join(dataFolder, t, f)
        if isfile(fullFile) and f.rsplit('.', 1)[1].lower() == 'csv':            
            lb = t + '.' + f.replace('_expression_matrix.csv', '')
            with open(fullFile, 'rt') as csvfile:
                datas = csv.reader(csvfile, delimiter = '\t')
                sampleCount = 0
                for row in datas:
                    if row is None or len(row) == 0:
                        continue
                    if sampleCount >= 70:
                        break
                    r = map(float,row[0].replace('\'', '').split(','))
                    log.write(str(r))
                    DataSet.append(r)
                    sampleCount = sampleCount + 1 # we don't want count empty lines into samples
                LabelCount[t+'.'+f] = sampleCount
            