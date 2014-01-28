#!/usr/bin/env python

from GP14 import *

import sys, os
import random
import time
from expressions.eval_prefix_exp import *
from metrics.term_freq import compute_freq_and_train_length
from metrics.spread import compute_instance_spread
from metrics.cooccur import compute_cooccur_and_entropy
from object.libsvm_object import *


#Computa metricas e recomenda

def recommend(obj, rules, entropy, spread, freq, train_length, k, relevance_func, num_rec):

    vote = defaultdict(float)
    vote_plus = defaultdict(float)
    sum = defaultdict(float)
    sum_plus = defaultdict(float)

    for t in obj:
        stab_t = stab_promotion(freq[t] + 1.0, k[0])
        position = 0
        for pair in sorted(rules[t].items(), key=itemgetter(1), reverse=True):
            c = pair[0]
            if c not in obj:
                rank = rank_promotion(position, k[2])
                vote[c] += 1.0
                plus = stab_t * rank
                vote_plus[c] += plus
                sum[c] += rules[t][c]
                sum_plus[c] += sum[c] * plus
                position += 1
    candidates = {}
    for t in vote:
        candidates[t] = 0
    for t in spread:
        if t not in obj:
            candidates[t] = 0

    for c in candidates:
        variables = {}
        variables["VOTE"] = vote[c]
        variables["VOTE_PLUS"] = vote_plus[c]
        variables["SUM"] = sum[c]
        variables["SUM_PLUS"] = sum_plus[c]
        variables["SP"] = spread[c]
        variables["FT"] = freq[c]
        variables["H"] = entropy[c]
        variables["DESC"] = stab_promotion(freq[c] + 1.0, k[1])
        variables["IFF"] = log((train_length + 1.0) / (freq[c] + 1.0))
        
        candidates[c] = eval_prefix_expression(relevance_func, variables)
    
    n = 1
    recommended = []
    for pair in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if n > num_rec:
            break
        n = n + 1
        recommended.append(pair[0])
    
    return recommended


def rank_promotion(position, kr):
    return kr / (kr + position)

def stab_promotion(f, k):
    return k / (k + math.fabs(math.log(f) - k))

if __name__ == "__main__":

    if len(sys.argv) < 10:
        print "usage: %s <train file> <test file> <min. support> <min. confidence> <num recomendacoes> <ks> <kd> <kr> <recommender function> [files]" % sys.argv[0]
        sys.exit(-1)

    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    test_file = open(test_filename)
    minsup = int(sys.argv[3])
    minconf = float(sys.argv[4])
    num_rec = int(sys.argv[5])

    k = []
    k.append(float(sys.argv[6]))
    k.append(float(sys.argv[7]))
    k.append(float(sys.argv[8]))
    func_file = open(sys.argv[9])
    for line in func_file:
        func = line.split()
    func_file.close()
    files = []
    for i in range(10, len(sys.argv)):
        files.append(open(sys.argv[i]))
    #print "blah", ks, kd, kr, minsup, num_rec

    (ft, n) = compute_freq_and_train_length(train_filename)
    (rules, entropy) = compute_cooccur_and_entropy(train_filename, ft, minsup, minconf)
    
    test = get_terms(test_file)[1]
    test_file.close()
    
    spreads = []
    
    
    for obj in test:
        spreads.append(compute_instance_spread(files))
    for f in files:
        f.close()

    for i in xrange(len(test)):
        rec = recommend(test[i], rules, entropy, spreads[i], ft, n, k, func, num_rec)

        for tag in rec:
            print tag,
        print



