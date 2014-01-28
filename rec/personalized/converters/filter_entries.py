
import sys
from mapping.term_id_mapping import string2id
from personalized.inout import load_list, read_set_file, print_list

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s <tag grouped postings file> <resource ids>" % sys.argv[0]
        sys.exit(-1)

    file = open(sys.argv[1])
    ids = read_set_file(sys.argv[2])
    count = 0
    total = 0
    for line in file:
        line = line.replace("\n", "")
        row = load_list(line)
        if row[1] in ids:
            count += 1
            print_list(row)
        total += 1
    file.close()
    print >>sys.stderr, "Total:%d   Without resource:%d   Without resource(percent): %f" % (total, total - count, 1.0 - float(count)/total)



