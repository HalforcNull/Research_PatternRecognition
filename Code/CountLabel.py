# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 13:11:11 2018

@author: runan.yao

This program simply count the label, so we know how many samples/training data
are provided by each label
"""

import csv
import json


def __loadData(dataFile):
    data = {}
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        for row in datas:
            if row is None or len(row) == 0:
                continue
            l = row[0]
            data[l] = data.get(l, 0) + 1
    return data


myd = __loadData('gtex_label.csv')
with open('gtexLabelInfo.csv', 'w') as csvFile:
    json.dump(myd, csvFile)

tcgad = __loadData('tcga_label.csv')
with open('tcgaLabelInfo.csv', 'w') as csvFile2:
    json.dump(tcgad, csvFile2)
