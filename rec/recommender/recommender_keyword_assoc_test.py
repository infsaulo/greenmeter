#!/usr/bin/env python

import sys, os
import random
import time
import math
from collections import defaultdict
from operator import itemgetter

from object.textual_features_concat import *


def compute_cooccur_and_entropy(train_filename, freq_term, minsup, minconf, fieldname):
    train = open(train_filename)
    f_intersection = defaultdict(lambda: defaultdict(int)) #frequencia da intersecao de dois termos
    train_object = get_next_concat(train)
    while train_object != None:
        field = train_object[fieldname]
        for t1 in field:
            if freq_term[t1] >= minsup:
                for t2 in field:
                    if freq_term[t2] >= minsup and t1 < t2:
                        f_intersection[t1][t2] += 1
                        #f_intersection[t2][t1] += 1
        train_object = get_next_concat(train)
    train.close()
    
    #Elimina co-ocorrencias menores que o suporte minimo e calcula entropia
    cooccurences = defaultdict(lambda: defaultdict(float))
    entropy = defaultdict(float)
    for t1 in f_intersection:
        ft1 = freq_term[t1]
        entropy[t1] = 0.0
        for t2 in f_intersection[t1]:
            f_t1t2 = float(f_intersection[t1][t2])
            if f_t1t2 >= minsup:
                ft2 = freq_term[t2]
                conft1t2 = f_t1t2 / ft1
                entropy[t1] -= conft1t2 * math.log(conft1t2)

                if conft1t2 >= minconf:
                    cooccurences[t1][t2] = conft1t2

                conft2t1 = f_t1t2 / ft2
                if conft2t1 >= minconf:
                    cooccurences[t2][t1] = conft2t1

    return (cooccurences, entropy)



def compute_DF_and_train_length(train_filename, fieldnames):

    file = open(train_filename)
    df = defaultdict(float)
    n = 1
    train_object = get_next_concat(file)
    while train_object != None:
        n += 1
        bagow = set()
        for field in fieldnames:
            for t in train_object[field]:
                bagow.add(t)
        for term in bagow:
            df[term] += 1.0
        train_object = get_next_concat(file)

    file.close()
    return (df, n)

def compute_TF(obj, fieldnames):

    tf = defaultdict(float)
    for field in fieldnames:
        for t in obj[field]:
            tf[t] += 1.0
    return tf


#Computa metricas e recomenda

def recommend(tf, df, tagf, N, rules, num_rec, alpha):

    assoc = defaultdict(float)
    tfidf = defaultdict(float)
    pk = defaultdict(float)

    for t in tf:
        tfidf[t] = tf[t] * math.log(N / (df[t] + 1.0))

    pos = 1
    for pair in sorted(tfidf.items(), key=itemgetter(1), reverse=True):
        if pos >= 100:
            break
        term = pair[0]
        pk[term] = 100 - pos
        pos += 1

    for t in pk:
        rules_t = rules[t]
        for c in rules_t:
            assoc[c] += rules_t[c] * pk[t]

    if len(assoc) > 0:
        assoc_max = max(assoc.values())

    if len(tfidf) > 0:
        tfidf_max = max(tfidf.values())

    candidates = defaultdict(float)
    for t in assoc:
        candidates[t] = alpha * (assoc[t]/assoc_max)

    for t in tfidf:
        candidates[t] += (1 - alpha) * (tfidf[t]/tfidf_max)

    n = 1
    recommended = []
    for pair in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if n > num_rec:
            break
        n = n + 1
        recommended.append(pair[0])

    return recommended


if __name__ == "__main__":

    if len(sys.argv) < 8:
        print "usage: %s <train file> <test file> <min. support> <min. confidence> <alpha> <num recomendacoes> [<field name>]+" % sys.argv[0]
        sys.exit(-1)

    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    test_file = open(test_filename)
    minsup = int(sys.argv[3])
    minconf = float(sys.argv[4])
    alpha = float(sys.argv[5])
    num_rec = int(sys.argv[6])
    
    fieldnames = []
    for i in range(7, len(sys.argv)):
        fieldnames.append(sys.argv[i])

    (df, n) = compute_DF_and_train_length(train_filename, fieldnames + ["TAG"])
    (tagf, n) = compute_DF_and_train_length(train_filename, ["TAG"])

    rules = compute_cooccur_and_entropy(train_filename, tagf, minsup, minconf, "TAG")[0]

    test_object = get_next_concat(test_file)

    print "df = ", df
    while test_object != None:
        tf = compute_TF(test_object, fieldnames)
        print "tf = ", tf
        rec = recommend(tf, df, tagf, n, rules, num_rec, alpha)
        print "Recs:"
        for tag in rec:
            print tag,
        print
        test_object = get_next_concat(test_file)

    test_file.close()


