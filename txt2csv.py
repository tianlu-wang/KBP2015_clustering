__author__ = 'koala'
# turn the EM pair confidence into matrix to be evaluated by matlab
# path1 is the input file
# path2 is the output matrix file
# path3 is the output pdost file related to the cophenet value

import re
Path1 = "/Users/koala/Downloads/sampleResult.txt"
Path2 = "/Users/koala/Downloads/txt2matrix"
Path3 = "/Users/koala/Downloads/txt2pdist"

f1 = open(Path1, "r")
f2 = open(Path2, "w")
f3 = open(Path3, "w")

pattern = re.compile(r'(.*)\|\|\|(.*)\|\|\|(.*)')
listOfEM = [] # store all event mentions
for line in f1.readlines():
    m = re.match(pattern, line, flags=0)
    if m:
        if m.group(1) in listOfEM:
            if m.group(2) not in listOfEM:
                listOfEM.append(m.group(2))
        else:
            listOfEM.append(m.group(1))
            if m.group(2) not in listOfEM:
                listOfEM.append(m.group(2))
    else:
        print('no match')
numEM = len(listOfEM)
print numEM
print listOfEM
f1.close()

f1 = open(Path1, "r") # be careful with the readline function

multilist = [['inf' for col in range(numEM)] for row in range(numEM)] # two dimension matrix

maxCon = 0

for line in f1.readlines():
    m = re.match(pattern,line,flags=0)
    if m:
        confidence = 1-float(m.group(3))  # to fit into the minimum cut equation
        if maxCon < confidence:
            maxCon = confidence
        multilist[listOfEM.index(m.group(2))][listOfEM.index(m.group(1))] = confidence
        multilist[listOfEM.index(m.group(1))][listOfEM.index(m.group(2))] = confidence

for k in range(numEM):
    multilist[k][k] = 0 # also to fit into the minimum cut equation

for i in range(numEM):
    for j in range(numEM):
        if multilist[i][j] == 'inf':
            multilist[i][j] = 10*maxCon  # TODO: be modified according to the data
        f2.write(str(multilist[i][j]))
        f2.write(" ")
    f2.write("\n")
    n = i+1
    while n < numEM:
        f3.write(str(multilist[i][n]))
        f3.write(' ')
        n += 1  # augmented assignment

f1.close()
f2.close()
f3.close()