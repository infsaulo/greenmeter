from numpy import *
import sys, math
from collections import defaultdict


def load_metrics(metrics, file):
    for line in file:
        if '#' not in line:
            tokens = line.split()
            if len(metrics) == 0:
                for i in xrange(len(tokens)):
                    metrics.append([])
            for i in xrange(len(tokens)):
                metrics[i].append(float(tokens[i]))


def load_classif_results(hits, out, labels):
    predicted = []
    correct = []
    for line in out:
        tokens = line.split()
        predicted.append(int(tokens[0]))
    for line in labels:
        tokens = line.split()
        correct.append(int(tokens[0]))
    for i in xrange(len(predicted)):
        if predicted[i] == correct[i]:
            hits.append(1)
        else:
            hits.append(0)


SAMPLE_COUNT = 10
FOLD_COUNT = 10

def load_all(out_dir, labels_dir, metrics_dir, block):
    hits = []
    metrics = []
    for sample_no in xrange(SAMPLE_COUNT):
        for fold_no in xrange(FOLD_COUNT):
            fname = "%s/%d/%s.part%d" % (labels_dir, sample_no, block, fold_no)
            try:
                labels = open(fname)
                fname = "%s/%d/%s.out%d" % (out_dir, sample_no, block, fold_no)
                out = open(fname)
                load_classif_results(hits, out, labels)
                fname = "%s/%d/%s.part%d" % (metrics_dir, sample_no, block, fold_no)
                metrics_file = open(fname)
                load_metrics(metrics, metrics_file)
            except:
                break
    print len(hits)
    print len(metrics)
    print len(metrics[0])
    return (hits, metrics)


def make_hists(hits, metrics, num_bins):
    NAMES = ["#neighbors", "frac. of neighbors in the same category", "#neighbors in the same category", "#neighbors in a different category", "#added terms"];
    v = 0
    for values in metrics:
        print "%s" % NAMES[v]
        #print "#range\taccuracy\tn"
        v += 1
        hist = [0.0 for j in xrange(num_bins + 1)]
        count = [0 for j in xrange(num_bins + 1)]
        M = max(values)
        for i in xrange(len(values)):
            x = values[i]
            if x < 0.0 : x = 0.0
            if M == 0.0: M = 1.0
            position = int(math.floor((x * num_bins) / M))
            hist[position] += hits[i]
            count[position] += 1
        for i in xrange(num_bins):
            x = (M / num_bins) * i
            if count[i] != 0:
                acc = hist[i] / count[i]
            else:
                acc = 0.0
            print "%f\t%f\t%d\t%d\t%f" % (x, acc, count[i], hist[i], float(count[i]) / len(hits))
            #print x, acc, count[i]

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "usage: %s <classification out> <classification labels> <inherit metrics> <block>" % sys.argv[0]
        sys.exit(-1)
    out_dir = sys.argv[1]
    labels_dir = sys.argv[2]
    metrics_dir = sys.argv[3]
    block = sys.argv[4]
    print "loading"; print out_dir; print labels_dir; print metrics_dir; print block
    data = load_all(out_dir, labels_dir, metrics_dir, block)
    make_hists(data[0], data[1], 10)

