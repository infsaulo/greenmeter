
import sys
from mapping.term_id_mapping import string2id
from personalized.inout import load_list

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s <tag grouped postings file> <word map file>" % sys.argv[0]
        sys.exit(-1)

    file = open(sys.argv[1])
    map_file = open(sys.argv[2])
    m = string2id(map_file)
    map_file.close()
    
    count = 0
    total = 0

    for line in file:
        line = line.replace("\n", "")
        row = load_list(line)
        words = []
        valid = True
        for tag in row[2:]:
            if tag in m:
                words.append(tag),
            else:
                valid = False
        if valid:
            print row[0], row[1],
            for w in words:
                print m[w],
            print
        else:
            count += 1
        total += 1
    file.close()
    print >> sys.stderr, "Total:%d   With unknown word:%d  With unknown word(percent): %f" % (total, count, float(count)/total)



