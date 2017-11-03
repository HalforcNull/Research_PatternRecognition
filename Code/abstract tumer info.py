# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 17:02:15 2017

abstract tumer info from file

@author: Student
"""

import re
import csv

with open('bigwig_file.txt') as f:
    content = f.readlines()

regexPattern = '[A-Z0-9]*_[A-Z0-9]*_[A-Z0-9]*_(?P<Gender>[fe]*male)_(?P<Tissue>[\w]*)(.)?(?P<SubTissue>[\w.]*).bw'
prog = re.compile(regexPattern)

NotMatchedLines = []
MatchedList = []
MatchedTissueList = []
MatchedSummaryOnlyTissue = {}
MatchedSummaryNoGenderInfo = {}
MatchedSummary = {}
Male = 0
Female = 0

OutputGenderTissue = []
OutputNoGenderTissueIncludeSub = []
OutputAll = []

for line in content:
    if line is None or line == '' or line == '\n':
        continue
    
    matchResult = prog.match(line)
    if matchResult is None:
        NotMatchedLines.append(line)
        continue
    
    MatchedList.append(line)
    gender = matchResult.group('Gender')
    if gender.lower() == 'male':
        Male += 1
    else:
        Female += 1
            
    tissue = matchResult.group('Tissue')
    subTissue = matchResult.group('SubTissue')
    
    MatchedTissueList.append(tissue)
    OutputGenderTissue.append(gender + '_' + tissue)
    if subTissue == '':
        OutputNoGenderTissueIncludeSub.append(tissue)
    else:
        OutputNoGenderTissueIncludeSub.append(tissue+'.'+subTissue)
        
    if subTissue == '':
        OutputAll.append(gender + '_' + tissue)
    else:
        OutputAll.append(gender + '_' + tissue+'.'+subTissue)
    
    if tissue in MatchedSummaryOnlyTissue.keys():
        MatchedSummaryOnlyTissue[tissue] += 1
    else:
        MatchedSummaryOnlyTissue[tissue] = 0
    
    wholeTissue = tissue + '.' + subTissue
    
    if tissue in MatchedSummaryNoGenderInfo.keys():
        MatchedSummaryNoGenderInfo[wholeTissue] += 1
    else:
        MatchedSummaryNoGenderInfo[wholeTissue] = 0
    
    gtKey = gender+'.'+wholeTissue
    
    if gtKey in MatchedSummary.keys():
        MatchedSummary[gtKey] += 1
    else:
        MatchedSummary[gtKey] = 0
        
GenderResult = 'Male: '+str(Male)+ ' Female: ' + str(Female)
print(GenderResult)         
"""       
with open('OnlyTissueLabelList.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(MatchedTissueList)"""
with open('OutputGenderTissue.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(OutputGenderTissue)
    
with open('OutputNoGenderTissueIncludeSub.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(OutputNoGenderTissueIncludeSub)
    
with open('OutputAll.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(OutputAll)



