import sys, csv
from processing.text_filtering  import *
from inout import read_set_file

def print_postings(row, stopw):
    user = row[0].replace(" ", "+")
    postings = row[4][1:len(row[4]) - 1].split(", ")
    for p in postings:
        pair = p.split(":")
        if len(pair) == 2:
            tag = pair[0]
            tags = process(split_words(tag), stopw)
            s = pair[1].split("/")
            ar = s[len(s) - 1]
            if "Ar" in s[0]:
                for t in tags:
                    print "%s, %s, %s" % (user, ar, t)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >>sys.stderr, "usage: %s <csv file> <stopwords>" % sys.argv[0]
        sys.exit(-1)

    filename = sys.argv[1]
    stopw = read_set_file(sys.argv[2])

    reader = csv.reader(open(filename))
    csv.field_size_limit(999999999)
    n = 1
    for row in reader:
        if n != 1:
            print_postings(row, stopw)
        n = n + 1

