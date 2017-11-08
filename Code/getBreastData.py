import csv


def __loadData(dataFile):
    data = []
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        for row in datas:
            if row is None or len(row) == 0:
                continue
            data.append(row)
    return data


log = open('log.txt', 'w')

DataList = __loadData('gtex_data.csv')
LabelList = __loadData('label.csv')

DataCollectedBreast = []

for i in range(0, 9662):
    if LabelList[i][0].lower() == 'breast':
        b = []
        b.append(i)
        b.append('breast')
        b.append(DataList[i])
        DataCollectedBreast.append(b)

with open('OutputBreast.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(DataCollectedBreast)
    
        


class DataRecord():
    rid = -1
    data = None
    rlabel = None
    def __init__(self, id, label, data):
        self.rid = id
        self.rlabel = label,
        self.data = data

