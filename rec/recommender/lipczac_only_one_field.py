#!/usr/bin/env python

import sys, os
import random
import time
import math
from collections import defaultdict

from object.textual_features_concat import get_next_concat_TF_weighted
from metrics.cooccur import compute_intersection_confidence
from util import get_top_ranked


def recommend_content_only(obj, intersec, fieldname):
    score = defaultdict(float)
    for w in obj[fieldname]:
        intersec_w = intersec[w]
        if intersec_w > 0.0:
            score[w] = intersec_w

    return score


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print "usage: %s <train file> <test file> <num recomendacoes> <field name>" % sys.argv[0]
        sys.exit(-1)

    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    test_file = open(test_filename)
    num_rec = int(sys.argv[3])
    fieldname = sys.argv[4]

    intersec = compute_intersection_confidence(train_filename, fieldname, "TAG")

    test_object = get_next_concat_TF_weighted(test_file)
    while test_object != None:
        candidates = recommend_content_only(test_object, intersec, fieldname)
        for w in get_top_ranked(candidates, num_rec):
            print w,
        print
        test_object = get_next_concat_TF_weighted(test_file)

    test_file.close()

