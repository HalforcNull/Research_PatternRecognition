# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 08:29:03 2017

@author: Student
"""

import os, time
"""
dirList = os.listdir('c:/Research_PatternRecognition')
for d in dirList:
    if d[0] == '.':
        continue
    
    if os.path.isdir('c:/Research_PatternRecognition/' + d) == True:
        stat = os.stat('c:/Research_PatternRecognition/' + d)
        created = os.stat('c:/Research_PatternRecognition/' + d).st_mtime
        asciiTime = time.asctime( time.gmtime( created ) )
        print(d)
        print('is a dir')#d, "is a dir  (created", asciiTime, ")"
    else:
        stat = os.stat('c:/Research_PatternRecognition/' + d)
        created = os.stat('c:/Research_PatternRecognition/' + d).st_mtime
        asciiTime = time.asctime( time.gmtime( created ) )
        print(d)
        print('is a file')# d, "is a file (created", asciiTime, ")"
        
        
        """
        
print( os.path.isfile('C:/1.csv') )