
from personalized.inout import print_list, load_list
import sys

def get_object_set(rids, file):
    for line in file:
        r = load_list(line.strip(), " ")[1]
        #print >>sys.stderr, "=======", r, "======="
        #sys.exit(-1)
        rids.add(r)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s <train or test> <resources>" % sys.argv[0]
        sys.exit(-1)

    file = open(sys.argv[1])
    resources = open(sys.argv[2])

    rids = set()
    get_object_set(rids, file)

    file.close()

    for line in resources:
        rid = line.split(" |")[0][3:]
        #print >>sys.stderr, "=======", rid, "======="
        #sys.exit(-1)
        if rid in rids:
            print line,

    resources.close()


