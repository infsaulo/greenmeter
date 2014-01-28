#!/usr/bin/env python

import sys, os
import random
import time
import math
from collections import defaultdict
from operator import itemgetter

from object.textual_features_concat import get_next_concat_TF_weighted
from metrics.cooccur import compute_intersection_confidence, compute_cooccur_and_entropy_field, compute_cooccur_one_field_to_another
from metrics.term_freq import compute_FF_and_train_length

from util import get_top_ranked, merge_scores, rescore
from lipczac_only_one_field import recommend_content_only


def recommend_assoc_only(antecedent_score, rules):
    score = defaultdict(float)
    for w in antecedent_score:
        as_w = antecedent_score[w]
        rules_w = rules[w]
        for c in rules_w:
            if c not in score:
                score[c] = 1.0
            score[c] *= (1.0 - rules_w[c]*as_w)

    for w in score:
        score[w] = 1.0 - score[w]

    return score


def recommend_assoc_combined(obj, title_intersec, desc_intersec, tag_tag, title_tag, title_scale, desc_scale):

    title_score = recommend_content_only(obj, title_intersec, "TITLE")
    desc_score = recommend_content_only(obj, desc_intersec, "DESCRIPTION")

    title_tag_score = recommend_assoc_only(title_score, title_tag)

    rescore(title_score, title_scale)
    rescore(desc_score, desc_scale)

    content_score = merge_scores((title_score, desc_score))
    tag_tag_score = recommend_assoc_only(content_score, tag_tag)

    return merge_scores((title_tag_score, tag_tag_score)) 


if __name__ == "__main__":

    if len(sys.argv) != 8:
        print "usage: %s <train file> <test file> <min. supp.> <min. conf.> <title scale> <desc. scale> <num recomendacoes>" % sys.argv[0]
        sys.exit(-1)

    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    test_file = open(test_filename)
    minsup = float(sys.argv[3])
    minconf = float(sys.argv[4])
    title_scale = float(sys.argv[5])
    desc_scale = float(sys.argv[6])
    num_rec = int(sys.argv[7])

    (ff, n) = compute_FF_and_train_length(train_filename, ["TITLE", "DESCRIPTION", "TAG"])

    title_intersec = compute_intersection_confidence(train_filename, "TITLE", "TAG")
    desc_intersec = compute_intersection_confidence(train_filename, "DESCRIPTION", "TAG")

    tag_tag = compute_cooccur_and_entropy_field(train_filename, ff["TAG"], minsup, minconf, "TAG")[0]
    title_tag = compute_cooccur_one_field_to_another(train_filename, ff, minsup, minconf, "TITLE", "TAG")

    test_object = get_next_concat_TF_weighted(test_file)
    while test_object != None:
        candidates = recommend_assoc_combined(test_object, title_intersec, desc_intersec, tag_tag, title_tag, title_scale, desc_scale)
        for w in get_top_ranked(candidates, num_rec):
            print w,
        print
        test_object = get_next_concat_TF_weighted(test_file)

    test_file.close()

