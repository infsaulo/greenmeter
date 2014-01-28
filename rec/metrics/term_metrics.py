#!/usr/bin/env python
from collections import defaultdict
from object.libsvm_object import *

import sys, os, math

def compute_freq(train_filename):
    train = open(train_filename)
    ft = defaultdict(float)
    train_object = get_next_object(train)
    while train_object != None:
        for term in train_object[1]:
            ft[term] += 1
        train_object = get_next_object(train)
    train.close()
    return ft



def compute_all_stats(train_filename):
    train = open(train_filename)
    infogain = defaultdict(float)
    entropia = defaultdict(float)
    entropia_ = defaultdict(float)
    ft = defaultdict(float)
    ftc = defaultdict(lambda: defaultdict(float))
    fc = defaultdict(float)

    num_objects = 0
    train_object = get_next_object(train)
    while train_object != None:
        num_objects += 1
        category = train_object[0]
        fc[category] += 1
        for term in train_object[1]:
            infogain[term] = 0
            ft[term] += 1
            ftc[term][category] += 1
        train_object = get_next_object(train)
    train.close()

    num_cats = len(fc)
    Hc = 0.0
    for c in fc.keys():
        pc = fc[c] / num_objects
        Hc += pc * math.log(pc)

    for t in infogain:
        pt = ft[t] / num_objects
        ptn = 1.0 - pt
        Ht = 0.0
        Htn = 0.0
        for c in fc.keys():
            pc_t = ftc[t][c] / ft[t]
            pc_tn = (fc[c] - ftc[t][c]) / (num_objects - ft[t])
            if pc_t != 0.0:
                Ht += pc_t * math.log(pc_t)
            if pc_tn != 0.0:
                Htn += pc_tn * math.log(pc_tn)
        entropia[t] = -Ht
        entropia_[t] = -Htn
        Ht *= pt
        Htn *= ptn
        infogain[t] = -Hc + Ht + Htn

    return (ft, infogain, entropia, entropia_, ftc, num_objects, fc)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: %s <libsvm file>" % sys.argv[0]
        sys.exit(-1)

    stats = compute_all_stats(sys.argv[1])
    print "#ID FT IG H HN"
    for t in stats[0]:
        print t, stats[0][t], stats[1][t], stats[2][t], stats[3][t]
