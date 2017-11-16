import csv

DataSet = {}

def __loadData(dataFile):
    data = []
    with open(dataFile, 'rt') as csvfile:
        datas = csv.reader(csvfile, delimiter = ',')
        i = 0
        for row in datas:
            if row is None or len(row) == 0:
                continue
            i+=1
            if i > 100 and i < 200:
                data.append(row)
    return data

log = open('log-stat.txt', 'w')
DataList = __loadData('gtex_data.csv')
LabelList = __loadData('label.csv')

with open('get100Data.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(DataList)
    
with open('get100Label.csv', 'w') as csvFile:
    wr = csv.writer(csvFile)
    wr.writerow(LabelList)
    