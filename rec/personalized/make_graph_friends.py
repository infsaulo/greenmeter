import sys, csv

def print_adj_list(row):
    print "%s," % row[0],
    adj = row[3][1:len(row[3]) - 1].split(", ")
    if len(adj) > 1:
        for user in adj[0:len(adj) - 1]:
            print "%s 1," % user.replace(" ", "+"),
    if len(adj) > 0:
        user = adj[len(adj) - 1]
        print "%s 1" % user.replace(" ", "+")


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
            print_adj_list(row)
        n = n + 1

