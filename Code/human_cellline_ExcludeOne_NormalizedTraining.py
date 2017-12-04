from os import listdir
from os.path import isfile, isdir, join
from sklearn.naive_bayes import GaussianNB

import csv
import datetime
import numpy as np
import pickle

dataFolder = '/home/yaor/research/human_matrix_cell_line/'
modelFolder = '/home/yaor/research/models_human_matrix_cell_line/'

def normalization(sample):
    """one sample pass in"""
    sample = sample + 100
    # 2^20 = 1048576
    return np.log2(sample * 1048576/np.sum(sample))



log = open('celllinelog.txt', 'a')


log.write('===============  ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
log.write('===============  New Log Start by ' + 'cell line')


tumorList = listdir(dataFolder)
DataSet = {}
sampleCount = 0
for t in tumorList:
    if not isdir(t): 
        log.write(t + ' is not a folder.')
    subList = listdir(join(dataFolder, t))
    for f in subList:
        fullFile = join(dataFolder, t, f)
        if isfile(fullFile) and f.rsplit('.', 1)[1].lower() == 'csv':            
            lb = t + '.' + f.replace('_expression_matrix.csv', '')
            with open(fullFile, 'rt') as csvfile:
                datas = csv.reader(csvfile, delimiter = '\t')
                numData = []
                for row in datas:
                    if row is None or len(row) == 0:
                        continue
                    r = map(float,row[0].replace('\'', '').split(','))
                    log.write(str(r))
                    numData.append(r)
                    sampleCount = sampleCount + 1 # we don't want count empty lines into samples
                DataSet[lb] = numData
            
            
log.write('Data Load Finished.')
log.write('labels we collected: '+ str(len(DataSet)))
log.write('samples we coolected: ' + str(sampleCount))

labels = DataSet.keys()
for l in labels:
    model = GaussianNB() 
    log.write('building pickle for: ' + l + ' excluded.' )
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

    with open('./normalizedmodel/cell_line/excludeOne/'+l+'.pkl', 'wb') as tr:
        pickle.dump(model, tr, pickle.HIGHEST_PROTOCOL)
