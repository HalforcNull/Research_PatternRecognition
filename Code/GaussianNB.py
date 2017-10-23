# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:09:29 2017

@author: Student
"""
from sklearn.naive_bayes import GaussianNB
import numpy as np
import csv

TestSample = []
TestActualResult = []
TrainingData = []
TrainingResult = []

def readTrainingData(dataFileName, dataLabel):
    with open(dataFileName, 'rt') as csvfile:
        mr = csv.reader(csvfile, delimiter = ',')
        a = zip(*mr)
        TestSample.append(next(a))
        TestActualResult.append(dataLabel)
        TestSample.append(next(a))
        TestActualResult.append(dataLabel)
        while True:
            try:
                ele = next(a)
                TrainingData.append(list(ele))
                TrainingResult.append(dataLabel)
              #  print(type(TrainingData))
              #  print(type(TrainingResult))
            except StopIteration:
                break



readTrainingData( 'C:/Research_PatternRecognition/Data/AllC16Data.csv', '16 Cell')
readTrainingData( 'C:/Research_PatternRecognition/Data/AllC8Data.csv', '8 Cell')
readTrainingData( 'C:/Research_PatternRecognition/Data/AllC4Data.csv', '4 Cell')
model = GaussianNB() 

model.fit(np.array(TrainingData).astype(np.float),np.array(TrainingResult))

print(model.predict(np.array(TestSample).astype(np.float)))
print(TestActualResult)
    