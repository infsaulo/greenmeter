import sys

def load_graph(filename):
    graph = {}
    file = open(filename)
    for line in file:
        s = line.split(", ")
        u = s[0]
        graph[u] = []
        if len(s) > 1:
            for tok in s[1:]:
                s2 = tok.split()
                if len(s2) == 2:
                    adj = s2[0]
                    w = float(s2[1])
                    graph[u].append((adj, w))
                else:
                    print >>sys.stderr, "Delimiter string at user name:%s" % tok
    file.close()
    return graph

def load_postings_user_tags(filename):
    postings = {}
    file = open(filename)
    for line in file:
        s = line.strip().split(", ")
        u = s[0]
        if u not in postings:
            postings[u] = []
        for t in s[2:]:
            postings[u].append(t.strip())
    file.close()
    return postings


def load_postings_user_int_tags(filename):
    postings = {}
    file = open(filename)
    for line in file:
        row = load_list(line.strip(), " ")
        u = row[0]
        if u not in postings:
            postings[u] = []
        for t in row[2:]:
            postings[u].append(int(t))
    file.close()
    return postings


def load_postings_resource_tags(filename):
    postings = {}
    file = open(filename)
    for line in file:
        s = line.strip().split(", ")
        r = s[1]
        if r not in postings:
            postings[r] = []
        for t in s[2:]:
            postings[r].append(t.strip())
    file.close()
    return postings

def load_postings_user_resource_tags(filename):
    postings = {}
    file = open(filename)
    for line in file:
        s = line.split(", ")
        u = s[0]
        r = s[1]
        t = s[2].strip()
        if (u, r) not in postings:
            postings[(u, r)] = []
        postings[(u, r)].append(t)
    file.close()
    return postings


def load_postings_user_resource_int_tags(filename):
    postings = {}
    file = open(filename)
    for line in file:
        s = line.split()
        u = s[0]
        r = s[1]
        t = s[2].strip()
        if (u, r) not in postings:
            postings[(u, r)] = []
        postings[(u, r)].append(int(t))
    file.close()
    return postings


def print_list(lis, delim=", "):
    print delim.join(lis)

def load_list(string, delim=", "):
    res = []
    if len(string) == 0:
        return res
    for s in string.split(delim):
        res.append(s)
    return res

def print_list_file(file, lis, delim=", "):
    print >>file, delim.join(lis)


def read_set_file(filename):
    file = open(filename)
    res = set()
    for line in file:
        res.add(line.strip())
    file.close()
    return res

