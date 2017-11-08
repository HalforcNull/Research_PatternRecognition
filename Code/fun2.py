def isOneStep(sr, de):
    # check if the position really able to jump by one step
    if sr < 0 or sr > 63 or de < 0 or de > 63:
        print('error')
    xsr = sr%8
    ysr = sr/8
    xde = de%8
    yde = de/8
    if (( xsr - xde == 2 and ysr - yde == 1 ) or 
        ( xsr - xde == 2 and yde - ysr == 1 ) or 
        ( xsr - xde == 1 and ysr - yde == 2 ) or 
        ( xsr - xde == 1 and yde - ysr == 2 ) or 
        ( xde - xsr == 2 and ysr - yde == 1 ) or 
        ( xde - xsr == 2 and yde - ysr == 1 ) or 
        ( xde - xsr == 1 and ysr - yde == 2 ) or 
        ( xde - xsr == 1 and yde - ysr == 2 )):
        return True
    else:
        return False
       
def getAllPos(c):
    # get all possible jump position
    allP = []
    allP.append(c+6)
    allP.append(c+10)
    allP.append(c+15)
    allP.append(c+17)
    allP.append(c-6)
    allP.append(c-10)
    allP.append(c-15)
    allP.append(c-17)
    return [t for t in allP if t >= 0 and t<=63]

def answer(src, dest):
    # your code here
    if src == dest:
        return 0
    if src < 0 or dest < 0 or src > 63 or dest > 63:
        return -1
    checked = []
    current = [src]
    nextList = []
    step = 1
    while True:
        for c in current:
            jumps = getAllPos(c)
            for t in jumps:
                if t == dest:
                    print(c)
                    return step
                if t in checked or t in nextList:
                    continue
                if isOneStep(c, t):
                    nextList.append(t)
        checked = list(set(current + checked))
        current = nextList
        print(nextList)
        nextList = []
        step += 1
    return None