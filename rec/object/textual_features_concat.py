from collections import defaultdict
from numpy import *

import sys, os, math
from ..object.libsvm_object import get_next_term_list

#I/O para formato "Object Textual Features"


def get_next_concat(file):
    obj = {}
    line = file.readline()
    if line == "":
        return None
    split1 = line.split("|")
    for s1 in split1:
        split2 = s1.split()
        name = split2[0]
        if name == "ID":
            obj[name] = split2[1]
        else:
            obj[name] = []
            o = obj[name]
            for t in split2[1:]:
                o.append(int(t))
    return obj

def get_next_concat_TF_weighted(file):
    obj = {}
    line = file.readline()
    if line == "":
        return None
    split1 = line.split("|")
    for s1 in split1:
        split2 = s1.split()
        name = split2[0]
        if name == "ID":
            obj[name] = split2[1]
        else:
            obj[name] = defaultdict(float)
            o = obj[name]
            for t in split2[1:]:
                tid = int(t)
                o[tid] += 1.0
    return obj


def get_all_concats(file):
    objs = {}
    for line in file:
        obj = {}
        if line == "":
            return None
        split1 = line.split("|")
        for s1 in split1:
            split2 = s1.split()
            name = split2[0]
            if name == "ID":
                obj[name] = split2[1]
            else:
                obj[name] = []
                o = obj[name]
                for t in split2[1:]:
                    o.append(int(t))
        objs[obj["ID"]] = obj
    return objs

def get_all_concats_TF_weighted(file):
    objs = {}
    for line in file:
        obj = {}
        if line == "":
            return None
        split1 = line.split("|")
        for s1 in split1:
            split2 = s1.split()
            name = split2[0]
            if name == "ID":
                obj[name] = split2[1]
            else:
                obj[name] = defaultdict(float)
                o = obj[name]
                for t in split2[1:]:
                    o[int(t)] += 1.0
        objs[obj["ID"]] = obj
    return objs


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) % 2 == 0:
        print "usage: %s <file 1> <field name 1> <file 2> <field name 2> ..." % sys.argv[0]
        sys.exit(-1)


    files = {}
    i = 1
    while i < len(sys.argv):
        filename = sys.argv[i]
        i += 1
        name = sys.argv[i]
        i += 1
        files[name] = open(filename)

    obj = {}
    for name in files:
        obj[name] = get_next_term_list(files[name])

    while obj[name] != None:
        print "ID", obj[name][2],
        print "| CAT", obj[name][0],
        for name in obj:
            print "|",
            print name, 
            for t in obj[name][1]:
                print t,
        print

        for name in files:
            obj[name] = get_next_term_list(files[name])




