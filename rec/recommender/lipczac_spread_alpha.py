#!/usr/bin/env python

import sys, os
import random
import time
import math
from collections import defaultdict
from operator import itemgetter

from object.textual_features_concat import get_next_concat_TF_weighted
from metrics.term_freq import compute_FF_and_train_length, compute_TS
from metrics.cooccur import compute_cooccur_and_entropy_field, compute_cooccur_one_field_to_another, compute_intersection_confidence
from lipczac_all_fields import recommend_content
from lipczac_only_assoc import recommend_assoc_combined
from util import *


#Computa metricas e recomenda

def recommend(obj, title_intersec, desc_intersec, tag_tag, title_tag, num_rec, title_scale, desc_scale, content_scale, alpha):

    content_score = recommend_content(obj, title_intersec, desc_intersec, title_scale, desc_scale)
    assoc_score = recommend_assoc_combined(obj, title_intersec, desc_intersec, tag_tag, title_tag, title_scale, desc_scale)
    rescore(content_score, content_scale)
    rescore(assoc_score, alpha)
    
    spread_score = compute_TS(obj, ["TITLE", "DESCRIPTION"])
    rescore(spread_score, 1.0 - alpha)

    return merge_scores((content_score, assoc_score, spread_score))


if __name__ == "__main__":

    if len(sys.argv) != 10:
        print "usage: %s <train file> <test file> <min. support> <min. confidence> <num recomendacoes> <title scale> <desc. scale> <content scale> <alpha>" % sys.argv[0]
        sys.exit(-1)

    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    test_file = open(test_filename)
    minsup = float(sys.argv[3])
    minconf = float(sys.argv[4])
    num_rec = int(sys.argv[5])
    title_scale = float(sys.argv[6])
    desc_scale = float(sys.argv[7])
    content_scale = float(sys.argv[8])
    alpha = float(sys.argv[9])

    (ff, n) = compute_FF_and_train_length(train_filename, ["TAG", "DESCRIPTION", "TITLE"])

    tag_tag = compute_cooccur_and_entropy_field(train_filename, ff["TAG"], minsup, minconf, "TAG")[0]
    title_tag = compute_cooccur_one_field_to_another(train_filename, ff, minsup, minconf, "TITLE", "TAG")
    title_intersec = compute_intersection_confidence(train_filename, "TITLE", "TAG")
    desc_intersec = compute_intersection_confidence(train_filename, "DESCRIPTION", "TAG")

    test_object = get_next_concat_TF_weighted(test_file)

    while test_object != None:
        rec = recommend(test_object, title_intersec, desc_intersec, tag_tag, title_tag, num_rec, title_scale, desc_scale, content_scale, alpha)
        for w in get_top_ranked(rec, num_rec):
            print w,
        print
        test_object = get_next_concat_TF_weighted(test_file)

    test_file.close()


