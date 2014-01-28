import sys, csv

def print_postings(row):
    user = row[0].replace(" ", "+")
    taggings = row[4][1:len(row[4]) - 1].split(", ")
    for t in taggings:
        pair = t.split(":")
        tag = pair[0]
        if len(pair) == 2:
            s = pair[1].replace(" ", "+")
            if "Ar" in s:
                print "%s, %s, %s" % (user, s, tag.lower())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: %s <csv file>" % sys.argv[0]
        sys.exit(-1)

    filename = sys.argv[1]
    reader = csv.reader(open(filename))
    csv.field_size_limit(999999999)
    n = 1
    for row in reader:
        if n != 1:
            print_postings(row)
        n = n + 1

