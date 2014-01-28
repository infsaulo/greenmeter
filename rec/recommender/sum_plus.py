#!/usr/bin/env python

import sys, os
import random
import time
import math
from collections import defaultdict
from operator import itemgetter

from ..metrics.term_freq import compute_FF_and_train_length, compute_TS, compute_stability, rank_promotion
from ..metrics.cooccur import compute_cooccur_and_entropy_field
from ..personalized.inout import load_list, print_list

from util import get_top_ranked


#Computa metricas e recomenda

def sum_plus_score(intags, confidences, ftag, k_ant, k_cons, k_r, stabilities, is_recommender):
    candidates = defaultdict(float)
    if len(intags) == 0:
        print>>sys.stderr, "Erro. Nenhuma tag de entrada"
        exit(-1)
    for ant in intags:
	if ant not in confidences:
		continue

        fant = ftag[ant]
        if fant not in stabilities:
            stab_ant = compute_stability(fant, k_ant)
            stabilities[fant] = stab_ant
        stab_ant = stabilities[fant]
        #stab_ant = compute_stability(fant, k_ant)
        rules = confidences[ant]
        position = 0.0
        for (cons, conf) in sorted(rules.items(), key=itemgetter(1), reverse=True):
	    if not is_recommender:
            	if cons in intags:
            	    continue
            fcons = ftag[cons]
            if fcons not in stabilities:
                stab_cons = compute_stability(fcons, k_cons)
                stabilities[fcons] = stab_cons
            stab_cons = stabilities[fcons]
            #stab_cons = compute_stability(fcons, k_cons)
            candidates[cons] += conf * rank_promotion(position, k_r) * stab_ant * stab_cons
            position += 1.0

    return candidates


if __name__ == "__main__":

    if len(sys.argv) != 9:
        print "usage: %s <train file (resources)> <input tags filename> <min. support> <min. confidence> <k_ant> <k_cons> <k_r> <num recommendations>" % sys.argv[0]
        sys.exit(-1)

    train_filename = sys.argv[1]
    input_tags = open(sys.argv[2])
    
    minsup = float(sys.argv[3])
    minconf = float(sys.argv[4])
    k_ant = float(sys.argv[5])
    k_cons = float(sys.argv[6])
    k_r = float(sys.argv[7])
    num_rec = int(sys.argv[8])


    (ff, n) = compute_FF_and_train_length(train_filename, ["TAG"])
    confidences = compute_cooccur_and_entropy_field(train_filename, ff["TAG"], minsup, minconf, "TAG")[0]
    stabilities = {}

    for line in input_tags:
        split = load_list(line.strip(), " ")
        intags = [int(x) for x in split[2:]]
        rec = get_top_ranked(sum_plus_score(intags, confidences, ff["TAG"], k_ant, k_cons, k_r, stabilities, 1), num_rec)
        for w in rec:
            print w,
        print

    input_tags.close()


