#!/usr/bin/env python

import sys, os
import random
import time
import math
from collections import defaultdict
from operator import itemgetter

from object.textual_features_concat import get_all_concats_TF_weighted
from metrics.term_freq import compute_FF_and_train_length, compute_FS, compute_internal_frequency_metrics
from metrics.cooccur import compute_cooccur_and_entropy_field
from personalized.inout import load_list, print_list, load_graph

from recommender.sum_plus import sum_plus_score
from util import *


#Computa metricas e recomenda
#Entrada: test_object: atributos textuais do objeto
#              intags: lista de tags de entrada
#                  fs: Feature Spread dos atributos textuais considerados
#         confidences: Confiancas das regras de associacao
#                ftag: frequencia em que uma palavra aparece como tag
#                  k*, alpha, beta: parametros de ajuste


def sum_plus_descriptive_power_user_score(test_object, intags, fs, confidences, ftag, k_ant, k_cons, k_r, stabilities, alpha, beta, metric_number, graph, user, tag_freq_user, postings, hops):
    gama = 1.0 - alpha - beta
    candidates = sum_plus_descriptive_power_score(test_object, intags, fs, confidences, ftag, k_ant, k_cons, k_r, stabilities, alpha, metric_number)

    #if len(candidates) > 0:
    #    maxv = max(candidates.values())
    #    for c in candidates:
    #        candidates[c] /= maxv

    urank = defaultdict(float)
    user_tag_freq_rank(urank, user, tag_freq_user, 0, 1.0, graph, postings, hops)

    new_candidates = {}
    for t in urank:
        if t not in intags:
            new_candidates[t] = urank[t]
    if len(new_candidates) > 0:
        maxv = max(new_candidates.values())
    else:
        maxv = 1.0
    for t in new_candidates:
        candidates[t] += gama * new_candidates[t] / maxv

    return candidates


if __name__ == "__main__":

    if len(sys.argv) != 16:
        print >>sys.stderr, "usage: %s <train (resources)> <test (resources)> <train (postings)> <input tags filename> <user graph> <max hops> <min. support> <min. confidence> <k_ant> <k_cons> <k_r> <alpha> <beta> <num recomendacoes> <descriptive power metric#>\nmetric#:\n\t0 = TS\n\t1 = TF\n\t2 = TFxFS\n\t3 = Sum of FS" % sys.argv[0]
        sys.exit(-1)

    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    test_file = open(test_filename)
    postings_filename = sys.argv[3]
    input_tags = open(sys.argv[4])
    user_graph_filename = sys.argv[5]
    maxhops = int(sys.argv[6])
    minsup = float(sys.argv[7])
    minconf = float(sys.argv[8])
    k_ant = float(sys.argv[9])
    k_cons = float(sys.argv[10])
    k_r = float(sys.argv[11])
    alpha = float(sys.argv[12])
    beta = float(sys.argv[13])
    num_rec = int(sys.argv[14])
    metric_number = int(sys.argv[15])
    
    if metric_number < 0 or metric_number > 3:
        print >>sys.stderr, "Metric number must be between 0 and 3"
        sys.exit(-1)
    
    test_objects = get_all_concats_TF_weighted(test_file)

    (ff, n) = compute_FF_and_train_length(train_filename, ["TAG"])
    confidences = compute_cooccur_and_entropy_field(train_filename, ff["TAG"], minsup, minconf, "TAG")[0]
    fs = compute_FS(train_filename, ["TITLE", "DESCRIPTION"])
    stabilities = {}
    print >> sys.stderr, "FS =", fs
    graph = load_graph(user_graph_filename)
    tag_freq_user = {}
    postings = load_postings_user_int_tags(postings_filename)

    for line in input_tags:
        split = load_list(line.strip(), " ")
        intags = [int(x) for x in split[2:]]
        user = split[0]
        rid = split[1]

        test_object = test_objects[rid]
        cand = sum_plus_descriptive_power_user_score(test_object, intags, fs, confidences, ff["TAG"], k_ant, k_cons, k_r, stabilities, alpha, beta, metric_number, graph, user, tag_freq_user, postings, maxhops)
        rec = get_top_ranked(cand, num_rec)
        for w in rec:
            print w,
        print

    test_file.close()

