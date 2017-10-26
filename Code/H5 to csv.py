# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 20:08:19 2017

@author: Student
"""
import h5py
import csv

is_label = False
h5FileName = 'tcga_matrix.h5'
infile = h5py.File(h5FileName)
myData = infile["data"]["expression"][0:]

print('lenth of data:')
print( len(myData) )

print('\n lenth of data element:')
print( len(myData[0]) )
print('\n')

with open("tcga_data.csv", "wb") as f:
    writer = csv.writer(f)
    if is_label:
        writer.writerow(myData)
    else:
        writer.writerows(myData)

