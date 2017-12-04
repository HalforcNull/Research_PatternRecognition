# -*- coding: utf-8 -*-
"""
Created on Fri Dec 01 12:43:05 2017

@author: runan.yao
"""

from os import listdir
from os.path import isfile, isdir, join

import csv
import datetime
#from itertools import zip

dataFolder = '/home/yaor/research/human_matrix_cell_line/'
modelFolder = '/home/yaor/research/models_human_matrix_cell_line/'


log = open('celllinelog.txt', 'a')


log.write('===============  ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
log.write('===============  New Log Start by ' + 'data trasport')


tumorList = listdir(dataFolder)
DataSet = {}
sampleCount = 0
for t in tumorList:
    if not isdir(t): 
        log.write(t + ' is not a folder.')
    subList = listdir(join(dataFolder, t))
    for f in subList:
        fullFile = join(dataFolder, t, f)
        lb = t + '.' + f.replace('_expression_matrix.tsv', '')
        if isfile(fullFile) and f.rsplit('.', 1)[1].lower() == 'tsv':
            log.write('start convert : '+ str(t) + '.' + str(f))
            with open(fullFile, 'rt') as csvfile:
                rawdatas = csv.reader(csvfile, delimiter = '\t')
                data = []
                for row in rawdatas:
                    if row is None or len(row) == 0:
                        continue
                    data.append(row)
                data.pop(0) #pop sample id
                data = zip(*data)
                data.pop(0) #pop gene
                csv.writer(open(fullFile.replace('.tsv', '.csv'), 'wt')).writerows(data)
            log.write('finish convert : '+ str(t) + '.' + str(f))
