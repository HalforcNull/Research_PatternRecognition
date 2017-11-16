from sklearn.naive_bayes import GaussianNB
import numpy as np
import itertools
import csv
import pickle
from os import listdir
from os.path import isfile, join



def __loadData(dataFile):
    data = []
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        i = 0
        for row in datas:
            if i > 1000:
                break
            if row is None or len(row) == 0:
                continue
            i += 1
            data.append(row)
    return data

def normalization(sample):
    """one sample pass in"""
    sample = sample + 100
    # 2^20 = 1048576
    return np.log2(sample * 1048576/np.sum(sample))


def loadModels():
    BiClassificationModules = []
    for f in listdir('./normalizedmodel/'):
        fullf = join('./normalizedmodel/',f)
        if isfile(fullf) and f.rsplit('.', 1)[1].lower() == 'pkl':
            newPkl = pickle.load(open(fullf, 'rb'))
            BiClassificationModules.append(newPkl)    
    return BiClassificationModules


def RunForBiPerdiction(models, normalizedData):
    result = []
    for m in models:
        result.append(m.predict([normalizedData])[0])
    return result

def predictWithFeq(datalist):
    mods = loadModels()
    dataPred = normalization(datalist)
    prdrslt = RunForBiPerdiction(mods, dataPred)
    result = {}
    for r in prdrslt:
        if r in result.keys():
            result[r] += 1
        else:
            result[r] = 1
    return result


log = open('log_BioPredictSuccess.txt', 'w')

DataList = __loadData('gtex_data.csv')
log.write('read data: len: ' + str(len(DataList)))
LabelList = __loadData('label.csv')


testData = np.array(DataList).astype(np.float)

success = 0
fail = 0
result = []
for data in testData:
    i = 0
    #result = []
    trueLabel = LabelList[i][0]
    #result.append(trueLabel)
    for key, value in sorted(predictWithFeq(data).iteritems(), key = lambda (k,v): (v,k), reverse = True):
        #print('key: '+key)
        #print('value: ' +str(value))
        if i > 3:
            fail += 1
            result.append(0)
            break;
    #    result.append([key, value])
        if key in trueLabel:
            success += 1
            result.append(value)
            break;
        i += 1
            
with open('bioTestResult.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(result)

log.write('success: ' + str(success))    
log.write('fail: ' + str(fail))



