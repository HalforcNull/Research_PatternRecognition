from sklearn.naive_bayes import GaussianNB
import numpy as np
import itertools
import csv
import pickle
import logging
import sys
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

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    log = logging.getLogger()
    fh = logging.FileHandler('bi_prediction_success_test.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter = formatter
    log.addHandler(fh)
    #if not log.handlers:
    #    log.addHandler(logging.StreamHandler(sys.stdout))
    
    log.critical('Program Start')
    DataList = __loadData('gtex_data.csv')
    log.info('read data. len: ' + str(len(DataList)))
    LabelList = __loadData('label.csv')
    log.info('read label. len: ' + str(len(LabelList)))

    testData = np.array(DataList).astype(np.float)
    log.info('data in test Data: ' + str(len(testData)))

    success = 0
    fail = 0
    result = []
    for i in range(len(testData)):
        data = testData[i]
        trueLabel = LabelList[i][0]
    #    log.info('cross check data: '+ str(i))
    #    log.info('true label: ' + trueLabel)
        if i%100 == 0:
            log.info('Already test:' + str(i) + ' samples')
        #sortedResult = sorted(predictWithFeq(data).iteritems(), key = lambda (k,v): v, reverse = True)
        for key, value in sorted(predictWithFeq(data).iteritems(), key = lambda (k,v): v, reverse = True):
            j = 0
            if  j > 3:
                fail += 1
                result.append(0)
                break
            if trueLabel in key:
                success += 1
                result.append(value)
                continue
        i += 1

    log.info('start writing result')            
    with open('bioTestResult.csv', 'w') as csvFile:
        wr = csv.writer(csvFile)
        wr.writerow(result)
    log.info('all info write into data. lenth:' + str(len(result)))

    log.info('success: ' + str(success))    
    log.info('fail: ' + str(fail))


if __name__ == '__main__':
    main()
