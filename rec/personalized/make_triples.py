import sys, csv

def print_postings(row):
    user = row[6].replace(" ", "+")
    video = row[0]
    tags = row[3][1:len(row[3]) - 1].split(", ")
    for tag in tags:
        print "%s, %s, %s" % (user, video, tag.lower())


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

