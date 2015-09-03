__author__ = 'koala'

# input: event mention pair coreference confidence
# output: the clustering result
# alert: cannot set the number of clusters K manually

import re  # for regular expression
import operator  # for sort

inputPath = "/Users/koala/PycharmProjects/KBP2015_clustering/nugget_detection_results/sample3.txt"
outputPath = "/Users/koala/PycharmProjects/KBP2015_clustering/nugget_detection_results/sample3_c.txt"

inputFile = open(inputPath, 'r')
outputFile = open(outputPath, 'w')

pattern = re.compile(r'(.*)\|\|\|(.*)\|\|\|(.*)\|\|\|(.*)')

dictOfEM = {}  # {'name':'frequency'}
for line in inputFile.readlines():
    m = re.match(pattern, line, flags=0)
    if m:
        em1 = m.group(2)
        em2 = m.group(3)
        if em1 in dictOfEM:  # dictOfEM runs faster than dictOfEM.keys() here
            dictOfEM[em1] = dictOfEM.get(em1) + 1
            if em2 not in dictOfEM:
                dictOfEM[em2] = 1
            else:
                dictOfEM[em2] = dictOfEM.get(em2) + 1
        else:
            dictOfEM[em1] = 1
            if em2 not in dictOfEM:
                dictOfEM[em2] = 1
            else:
                dictOfEM[em2] = dictOfEM.get(em2) + 1
    else:
        print('no match')
listOfEM = dictOfEM.keys()
numEM = len(listOfEM)
#  below is the debug code
#  ---------------------
print numEM
print listOfEM
print dictOfEM
#  ----------------

sortedEM = sorted(dictOfEM.items(), key=operator.itemgetter(1), reverse=True)
inputFile.close()
inputFile = open(inputPath, 'r')   # actually I want to read the file once but don't how to do it

multiList = [[0 for col in range(numEM)] for row in range(numEM)]

for line in inputFile.readlines():
    m = re.match(pattern, line, flags=0)
    if m:
        em1 = m.group(2)
        em2 = m.group(3)
        score = m.group(4)
        multiList[listOfEM.index(em1)][listOfEM.index(em2)] = score
        multiList[listOfEM.index(em2)][listOfEM.index(em1)] = score
    else:
        print 'not match'

inputFile.close()
# --------for debug------------
print sortedEM
print multiList
# ----------------------------------


def avg(l, num):
    total = 0
    for iAvg in l:
        print('iAvg : %d' % iAvg)
        total += float(multiList[iAvg][num])
    return total/len(l)


def cluster(dic, num):
    flag = False
    for e in dic:
        l = dic.get(e)
        if avg(l, num) >= threshold:
            l.append(num)
            dic[e] = l
            flag = True
        if flag:
            break
    if not flag:
        dic[len(dic)+1] = [num]
    print('dic in cluster:')
    print dic
    return dic

# ----------------------------------
# listOfEM sortedEM multiList

dictResult = {}
threshold = 0.5389676  # important!
for k in range(numEM):
    if k == 0:
        print dictResult
    elif k == 1:
        i = listOfEM.index(sortedEM[k][0])
        j = listOfEM.index(sortedEM[k - 1][0])
        if multiList[i][j] > threshold:
            dictResult[1] = [0, 1]
        else:
            dictResult[1] = [0]
            dictResult[2] = [1]
        print(dictResult)
    else:
        i = listOfEM.index(sortedEM[k][0])
        cluster(dictResult, i)
        print dictResult
print("the answer: \n")
print(dictResult)
for element in dictResult:
    outputFile.write(str(element))
    outputFile.write(':')
    for e in dictResult.get(element):
        outputFile.write(listOfEM[e] + "  ")
    outputFile.write('\n')
outputFile.close()












