__author__ = 'koala'

import re
Path1 = "/Users/koala/Downloads/sample.txt"
Path2 = "/Users/koala/Downloads/sampleResult.txt"

f1 = open(Path1, "r")
f2 = open(Path2, "w")

pattern = re.compile(r'(.*)\|\|\|(.*)\|\|\|(.*)\|\|\|(.*)')


for line in f1.readlines():
    m = re.match(pattern, line, flags=0)
    if m:
        f2.write(m.group(2)+"|||"+m.group(3)+"|||"+m.group(4)+"\n")
    else:
        print('no match')

f1.close()
f2.close()
