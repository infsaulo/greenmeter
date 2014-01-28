#!/usr/bin/env python

import sys, os
import random
import time
import math
from collections import defaultdict
from operator import itemgetter

from object.textual_features_concat import get_next_concat_TF_weighted
from metrics.cooccur import compute_intersection_confidence
from util import get_top_ranked, merge_scores, rescore
from lipczac_only_one_field import recommend_content_only


def recommend_content(obj, title_intersec, desc_intersec, title_scale, desc_scale):
    title_score = recommend_content_only(obj, title_intersec, "TITLE")
    desc_score = recommend_content_only(obj, desc_intersec, "DESCRIPTION")
    
    rescore(title_score, title_scale)
    rescore(desc_score, desc_scale)

    return merge_scores((title_score, desc_score))


if __name__ == "__main__":

    if len(sys.argv) != 6:
        print "usage: %s <train file> <test file> <title scale> <desc. scale> <num recomendacoes>" % sys.argv[0]
        sys.exit(-1)

    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    test_file = open(test_filename)
    title_scale = float(sys.argv[3])
    desc_scale = float(sys.argv[4])
    num_rec = int(sys.argv[5])

    title_intersec = compute_intersection_confidence(train_filename, "TITLE", "TAG")
    desc_intersec = compute_intersection_confidence(train_filename, "DESCRIPTION", "TAG")

    test_object = get_next_concat_TF_weighted(test_file)

    while test_object != None:
        candidates = recommend_content(test_object, title_intersec, desc_intersec, title_scale, desc_scale)
        for w in get_top_ranked(candidates, num_rec):
            print w,
        print
        test_object = get_next_concat_TF_weighted(test_file)

    test_file.close()

