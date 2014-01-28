
#from personalized.inout import load_postings_user_resource_tags
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: %s <postings file>" % sys.argv[0]
        sys.exit(-1)

    filename = sys.argv[1]
    file = open(filename)
    current_ur = None
    tags = []
    for line in file:
        line = line.replace("\n", "")
        s = line.split(", ")
        u = s[0]
        r = s[1]
        t = s[2]
        if (u, r) == current_ur or current_ur == None:
            tags.append(t)
        else:
            print "%s, %s," % current_ur,
            print ", ".join(tags)

            tags = [] #empty buffer
            tags.append(t)
        current_ur = (u, r)


