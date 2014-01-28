from collections import defaultdict
from ..object.libsvm_object import *
from ..object.textual_features_concat import get_next_concat_TF_weighted
from term_freq import compute_stability, rank_promotion
from operator import itemgetter

import sys, os, math


def compute_cooccur_and_entropy_field_trainset(resources, freq_term, minsup, minconf, fieldname, oids):

    f_intersection = defaultdict(lambda: defaultdict(int)) #frequencia da intersecao de dois termos
    for oid in oids:
        train_object = resources[oid]
        field = train_object[fieldname]
        for t1 in field:
            if freq_term[t1] >= minsup:
                for t2 in field:
                    if freq_term[t2] >= minsup and t1 < t2:
                        f_intersection[t1][t2] += 1
                        f_intersection[t2][t1] += 1

    #Elimina co-ocorrencias menores que o suporte minimo e calcula entropia
    cooccurences = defaultdict(lambda: defaultdict(float))
    entropy = defaultdict(float)
    for t1 in f_intersection:
        ft1 = freq_term[t1]
        entropy[t1] = 0.0
        for t2 in f_intersection[t1]:
            f_t1t2 = float(f_intersection[t1][t2])
            if f_t1t2 >= minsup:
                #ft2 = freq_term[t2]
                conft1t2 = f_t1t2 / ft1

                if conft1t2 >= minconf:
                    entropy[t1] -= conft1t2 * math.log(conft1t2)
                    cooccurences[t1][t2] = conft1t2

                #conft2t1 = f_t1t2 / ft2
                #if conft2t1 >= minconf:
                #    cooccurences[t2][t1] = conft2t1

    return (cooccurences, entropy)



def compute_cooccur_and_entropy(train_filename, freq_term, minsup, minconf):
    train = open(train_filename)
    f_intersection = defaultdict(lambda: defaultdict(int)) #frequencia da intersecao de dois termos
    train_object = get_next_object(train)
    while train_object != None:
        for t1 in train_object[1]:
            if freq_term[t1] >= minsup:
                for t2 in train_object[1]:
                    if freq_term[t2] >= minsup and t1 < t2:
                        f_intersection[t1][t2] += 1
                        f_intersection[t2][t1] += 1
        train_object = get_next_object(train)
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
                #ft2 = freq_term[t2]
                conft1t2 = f_t1t2 / ft1

                if conft1t2 >= minconf:
                    cooccurences[t1][t2] = conft1t2
                    entropy[t1] -= conft1t2 * math.log(conft1t2)

                #conft2t1 = f_t1t2 / ft2
                #if conft2t1 >= minconf:
                #    cooccurences[t2][t1] = conft2t1

    return (cooccurences, entropy)


def compute_cooccur_and_entropy_field(train_filename, freq_term, minsup, minconf, fieldname):
    train = open(train_filename)
    f_intersection = defaultdict(lambda: defaultdict(int)) #frequencia da intersecao de dois termos
    train_object = get_next_concat_TF_weighted(train)
    while train_object != None:
        field = train_object[fieldname]
        for t1 in field:
            if freq_term[t1] >= minsup:
                for t2 in field:
                    if freq_term[t2] >= minsup and t1 < t2:
                        f_intersection[t1][t2] += 1
                        f_intersection[t2][t1] += 1
        train_object = get_next_concat_TF_weighted(train)
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
                #ft2 = freq_term[t2]
                conft1t2 = f_t1t2 / ft1

                if conft1t2 >= minconf:
                    cooccurences[t1][t2] = conft1t2
                    entropy[t1] -= conft1t2 * math.log(conft1t2)

                #conft2t1 = f_t1t2 / ft2
                #if conft2t1 >= minconf:
                #    cooccurences[t2][t1] = conft2t1

    return (cooccurences, entropy)



def compute_cooccur_one_field_to_another(train_filename, ff, minsup, minconf, fieldname1, fieldname2):
    train = open(train_filename)
    f_intersection = defaultdict(lambda: defaultdict(int)) #frequencia da intersecao de dois termos
    train_object = get_next_concat_TF_weighted(train)
    while train_object != None:
        field1 = train_object[fieldname1]
        field2 = train_object[fieldname2]
        
        for t1 in field1:
            if ff[fieldname1][t1] >= minsup:
                for t2 in field2:
                    if ff[fieldname2][t2] >= minsup and t1 != t2:
                        f_intersection[t1][t2] += 1
                        #f_intersection[t2][t1] += 1
        train_object = get_next_concat_TF_weighted(train)
    train.close()

    #Elimina co-ocorrencias menores que o suporte minimo

    cooccurences = defaultdict(lambda: defaultdict(float))

    for t1 in f_intersection:
        ft1 = ff[fieldname1][t1]

        for t2 in f_intersection[t1]:
            f_t1t2 = float(f_intersection[t1][t2])
            if f_t1t2 >= minsup:
                conft1t2 = f_t1t2 / ft1
                if conft1t2 >= minconf:
                    cooccurences[t1][t2] = conft1t2

    return cooccurences


def compute_intersection_confidence(train_filename, fieldname1, fieldname2):
    train = open(train_filename)
    intersec = defaultdict(float)
    ft1 = defaultdict(float)
    train_object = get_next_concat_TF_weighted(train)
    while train_object != None:
        field1 = train_object[fieldname1]
        field2 = train_object[fieldname2]

        for t in field1:
            ft1[t] += 1.0
            if t in field2:
                intersec[t] += 1.0
        train_object = get_next_concat_TF_weighted(train)

    for t in intersec:
        intersec[t] /= ft1[t]
    train.close()
    return intersec


def compute_vote(input_tags, confidences, tag_f, ks, kr):
    vote = {} #VOTE, VOTE+, SUM, SUM+
    for u in input_tags:
        conf_u = confidences[u]
        if u in tag_f:
            fu = tag_f[u]
        else:
            continue
        stab = compute_stability(fu, ks)
        position = 0
        for (cand, conf) in sorted(conf_u.items(), key=itemgetter(1), reverse=True):
            if cand not in input_tags: #nao recomendar palavras que jah estao lah
                if cand not in vote:
                    vote[cand] = [0.0 for x in xrange(4)]
                vote[cand][0] += 1.0
                vote[cand][1] += stab * rank_promotion(position, kr)
                vote[cand][2] += conf
                vote[cand][3] += conf * stab * rank_promotion(position, kr)
                position += 1
    return vote




