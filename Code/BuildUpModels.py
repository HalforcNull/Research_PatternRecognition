from sklearn.naive_bayes import GaussianNB
import numpy as np
import itertools
import csv
import pickle

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

log = open('log.txt', 'w')
DataList = __loadData('gtex_data.csv')
LabelList = __loadData('label.csv')

for i in range(0, 9662):
    lb = LabelList[i][0]
    if lb in ['small', 'minor', 'whole']:
        # meaning less label are removed from the tests
        continue
    
    if lb in DataSet.keys():
        DataSet[lb].append(DataList[i])
    else:
        DataSet[lb] = [DataList[i]]

log.write('Data Load Finished.')

labels = DataSet.keys()

TwoLabels = itertools.combinations(labels, 2)

for labels in TwoLabels:
    lb1 = labels[0]
    lb2 = labels[1]
    log.write('building pickle for: ' + lb1 + ' ' + lb2)
    Data = DataSet[lb1] + DataSet[lb2]
    Label = [lb1]*len(DataSet[lb1]) + [lb2]*len(DataSet[lb2])
    
    testTraining = np.array(Data).astype(np.float)
    # do normalization here
    testTraining = np.apply_along_axis(normalization, 1, testTraining )
    testlabeling = np.array(Label)
    
    model = GaussianNB() 
    model.fit(testTraining,testlabeling)

    with open('./normalizedmodel/_' + lb1+'_'+lb2+'.pkl', 'wb') as tr:
        pickle.dump(model, tr, pickle.HIGHEST_PROTOCOL)



