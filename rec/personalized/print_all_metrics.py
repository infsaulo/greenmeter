
import sys, math
from collections import defaultdict
from personalized.inout import load_graph, load_postings_user_int_tags, print_list, load_list
from recommender.util import get_top_ranked, get_top_ranked_map
from metrics.term_freq import compute_FF_and_train_length, compute_internal_frequency_metrics, compute_IDF, compute_stability
from metrics.cooccur import compute_vote, compute_cooccur_and_entropy_field
from object.textual_features_concat import get_next_concat_TF_weighted


if __name__ == "__main__":
    if len(sys.argv) != 12:
        print >>sys.stderr, "usage: %s <train postings> <input tags> <train resources> <test resources> <graph> <ks> <kd> <kr> <minsup> <minconf> <#hops>" % sys.argv[0]
        sys.exit(-1)

    train = load_postings_user_tags(sys.argv[1])
    input_tags = open(sys.argv[2])
    train_resources_filename = sys.argv[3]
    test_resources_filename = sys.argv[4]
    test_resources = open(test_resources_filename)

    graph = load_graph(sys.argv[5])
    ks = float(sys.argv[6])
    kd = float(sys.argv[7])
    kr = float(sys.argv[8])
    minsup = float(sys.argv[9])
    minconf = float(sys.argv[10])
    hops = int(sys.argv[11]) 

    MAX_CAND = 100
    tag_freq_user = {}

    (f_tag, train_length) = compute_FF_and_train_length(train_resources_filename, ["TAG"])["TAG"]
    fs = compute_FS(train_resources_filename, ["TITLE", "DESCRIPTION"])

    (confidences, entropy) = compute_cooccur_and_entropy_field(train_resources_filename, f_tag, minsup, minconf, "TAG")

    iff = {}
    stab = {}
    test_objects = get_all_concats_TF_weighted(test_resources)

    for line in input_tags:
        row = load_list(line.strip(), " ")
        user = row[0]
        oid = row[1]
        intags = set([int(x) for x in row[2:]])
        concat = test_objects[oid]

        urank = defaultdict(float)
        user_tag_freq_rank(urank, user, tag_freq_user, 0, 1.0, graph, train, hops)

        social_candidates = get_top_ranked_map(urank, MAX_CAND)
        urank = None #free memory

        vote = compute_vote(intags, confidences, f_tag, ks, kr)
        descriptive_power_metrics = compute_internal_frequency_metrics(concat, fs)
        candidates = set(social_candidates.keys() + vote.keys() + descriptive_power_metrics.keys()) - intags


        #valores default para as metricas

        vot = 0.0
        vot_stab = 0.0
        sum = 0.0
        sum_stab = 0.0
        fc = 0.0
        ur = 0.0
        
        ts = 0.0
        tf = 0.0
        tfxfs = 0.0
        fs_sum = 0.0
        
        h = 100.0

        for c in candidates:
            if c in vote:
                elem = vote[c]
                vot = elem[0]
                vot_stab = elem[1]
                sum = elem[2]
                sum_stab = elem[3]

            if c in f_tag:
                fc = f_tag[c]

            if fc not in iff:
                iff[fc] = compute_IDF(fc, train_length)
                stab[fc] = compute_stability(fc, kd)

            if c in social_candidates:
                ur = social_candidates[c]

            if c in descriptive_power_metrics:
                elem = descriptive_power_metrics[c]
                ts = elem[0]
                tf = elem[1]
                tfxfs = elem[2]
                fs_sum = elem[3]

            if c in entropy:
                h = entropy[c]

            print c, vot, vot_stab, sum, sum_stab, ts, tf, tfxfs, fs_sum, iff[fc], stab[fc], h, ur,
            print ",",
        print


    input_tags.close()
    test_resources.close()

