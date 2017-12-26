import pickle
import json

part_1 = pickle.load(open('./data/testR_GTEXDataVSTCGAModel_1.pkl', 'rb'))
part_2 = pickle.load(open('./data/testR_GTEXDataVSTCGAModel_2.pkl', 'rb'))


for gtexKeyIn1 in part_1.keys():
    if gtexKeyIn1 not in part_2.keys():
        part_2[gtexKeyIn1] = {}
    for tcgaResultIn1 in part_1[gtexKeyIn1].keys():
        if tcgaResultIn1 not in part_2[gtexKeyIn1].keys():
            part_2[gtexKeyIn1][tcgaResultIn1] = 0
        part_2[gtexKeyIn1][tcgaResultIn1] += part_1[gtexKeyIn1][tcgaResultIn1]

with open('bioTestResult_GETXdata_TCGAmodel_Overall.csv', 'w') as outputFile:
        json.dump(part_2, outputFile)


