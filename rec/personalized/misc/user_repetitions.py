
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
    user_tags = {}

    for line in file:
        total += 1
        line = line.strip()
        row = load_list(line, " ")
        user = row[0]
        tags = set([int(x) for x in row[2:]])
        if user not in user_tags:
            user_tags[user] = defaultdict(int)
        for t in tags:
            user_tags[user][t] += 1 
    file.close()
    
    for (user, tags) in user_tags.items():
        for value in tags.values():
            hist[value] += 1
    for (key, value) in hist.items():
        print key, 100*float(value)/sum(hist.values())





