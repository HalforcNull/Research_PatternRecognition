from sklearn.naive_bayes import GaussianNB
import numpy as np
import itertools
import csv
import pickle
import psutil

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

def normalization(sample):
    """one sample pass in"""
    sample = sample + 100
    # 2^20 = 1048576
    return np.log2(sample * 1048576/np.sum(sample))

def getMemoUsage():
    return str(psutil.virtual_memory().percent)

log = open('excludeOnelog.txt', 'w')
log.write('Program Start \n')
log.write('Memo usage: '+ getMemoUsage() +'\n')

DataList = __loadData('gtex_data.csv')
LabelList = __loadData('gtex_label.csv')

log.write('File load Finished. \n')
log.write('Memo usage: '+ getMemoUsage() +'\n')


for i in range(0, 9662):
    lb = LabelList[i][0]
    if lb in DataSet.keys():
        DataSet[lb].append(DataList[i])
    else:
        DataSet[lb] = [DataList[i]]

del DataList
del LabelList

log.write('Data Load Finished.\n')
log.write('Memo usage: '+ getMemoUsage() +'\n')

labels = DataSet.keys()

for i in range( 0, 10 ):
    l = labels[i]
    model = GaussianNB() 
    log.write('Building pickle for: ' + l + ' excluded.' )
    Data = []
    Label = []
    for j in labels:
        if l != j:
            Data = Data + DataSet[j]
            Label = Label + [j] * len(DataSet[j])
            
    testTraining = np.array(Data).astype(np.float)
    # do normalization here
    testTraining = np.apply_along_axis(normalization, 1, testTraining )
    testlabeling = np.array(Label)
    model.fit(testTraining,testlabeling)
    
    log.write('Model: ' + l + ' training finished.\n')
    log.write('Memo usage: '+ getMemoUsage() +'\n')
    
    with open('./normalizedmodel/gtex/excludeOne/'+l+'.pkl', 'wb') as tr:
        pickle.dump(model, tr, pickle.HIGHEST_PROTOCOL)
    
    log.write('pickel: ' + l + ' write done.\n')
    log.write('Memo usage: '+ getMemoUsage() +'\n')
