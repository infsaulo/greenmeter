#!/usr/bin/env python

from __future__ import with_statement
from collections import defaultdict
from numpy import *
from operator import itemgetter
import sys, os, math

from metrics.infogain import compute_stats
from object.libsvm_object import *
from graph.graph_loader import getsims

def merge(objects, cats, sims, k, same_class, g, infogain, ft, fc, ftc, num_objects, num_cats, sup):

    catset = set(cats)
    num_herancas = 0
    for i in xrange(0, len(objects)):
        inherit = defaultdict(int)
        new_weights = objects[i].copy()
        friends = len(sims[i])
        term_freq_neighbors = defaultdict(float)
        candidate_terms = defaultdict(float)
        candidate_terms_ig = defaultdict(float)

        for j in sims[i]:
            if (same_class and cats[i] == cats[j]) or (not same_class):
                for t in objects[j].keys():
                    term_freq_neighbors[t] += 1.0
                    candidate_terms[t] += objects[j][t]
                    candidate_terms_ig[t] = infogain[t]
            #print term_freq_neighbors

        n = 0.0
        #print sorted(candidate_terms_ig.items(), key=itemgetter(1), reverse=True)
        #sys.exit(0)
        #obtem termos em ordem decrescente de infogain
        diff_cat = 0.0
        concentration = 0.0

        #print "my class:", cats[i]
        for pair in sorted(candidate_terms_ig.items(), key=itemgetter(1), reverse=True):
            t = pair[0]
            if n >= g:
                break
            if (t not in objects[i]) and (term_freq_neighbors[t] >= k) and (ft[t] > sup): #inherit
                n += 1.0
                #cmax = 0
                #pmax = 0.0
                #concentration += ftc[t][cats[i]] / ft[t]
                print (ftc[t][cats[i]] / ft[t]), ft[t]
                #for c in catset:
                #    pc_t = ftc[t][c] / ft[t]
                #    if pc_t > pmax:
                #        pmax = pc_t
                #        cmax = c
                #print "cmax:", cmax
                #if cats[i] != cmax:
                #    diff_cat += 1.0
                #num_herancas += 1
        #if n > 0:
        #    print (concentration / n), n, 


if __name__ == "__main__":
    if len(sys.argv) != 7 and len(sys.argv) != 8:
        print "usage: %s <libsvm file> <graph file> <limiar de sim.> <limiar de consenso> <mesma classe> <freq. min.> [g]" % sys.argv[0]
        sys.exit(-1)

    libsvm_file = open(sys.argv[1])
    graph_file = open(sys.argv[2])
    t = float(sys.argv[3])
    k = int(sys.argv[4])
    same_class = bool(int(sys.argv[5]))
    #print "Same class?", same_class
    #print "Limiar de sim.:", t
    #print "Limiar de consenso:", k
    sup = int(sys.argv[6])

    if len(sys.argv) == 8:
        g = int(sys.argv[7])

    else:
        g = sys.maxint

        
    #print "Herdar top", g, "termos"
    objects_and_cats = get_objects(libsvm_file)

    s = getsims(graph_file, t)

    libsvm_file.close()
    graph_file.close()
    libsvm_file = open(sys.argv[1])
    stats = compute_stats(libsvm_file, 1)
    merge(objects_and_cats[0], objects_and_cats[1], s, k, same_class, g, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], sup)
    libsvm_file.close()


