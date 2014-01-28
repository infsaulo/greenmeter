
import sys
from collections import defaultdict
from personalized.inout import load_list, print_list

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: %s <tag grouped postings file>" % sys.argv[0]
        sys.exit(-1)

    file = open(sys.argv[1])
    hist = defaultdict(int)
    total = 0

    for line in file:
        total += 1
        line = line.strip()
        row = load_list(line, " ")
        tagn = len(set(row[2:]))
        hist[tagn] += 1
        if tagn > 1:
            print_list(row, " ")
    file.close()

    for (key, value) in hist.items():
        print >>sys.stderr, key, float(value)/total





