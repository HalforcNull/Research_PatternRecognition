# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 20:08:19 2017

@author: Student
"""

>>> infile = h5py.File('C:/Downloads/gtex_matrix.h5')
>>> myData = infile["data"]["expression"][0:]
>>> myData[0]
array([  64625,   91931,    4352, ..., 5141780, 1071715,  285020])
>>> length(myData[0])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'length' is not defined
>>> count(myData[0])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'count' is not defined
>>> len(myData[0])
25150
>>> import csv
>>> with open("TheOutputCSV.csv", "wb") as f:
...     writer = csv.writer(f)
...     writer.writerows(myData)
...