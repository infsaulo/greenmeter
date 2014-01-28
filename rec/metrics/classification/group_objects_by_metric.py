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
    #print len(hits)
    #print len(metrics)
    #print len(metrics[0])
    return (hits, metrics)


def group(hits, values, ranges):
    print "#interval\tcount\thits\taccuracy\tcount(%)"
    num_bins = len(ranges)
    nhits = [0 for j in xrange(num_bins + 1)]
    count = [0 for j in xrange(num_bins + 1)]
    for i in xrange(len(hits)):
        for j in xrange(num_bins - 1):
            if (values[i] >= ranges[j] and values[i] < ranges[j + 1]) or (values[i] < ranges[0]):
                break
        nhits[j] += hits[i]
        count[j] += 1
    for i in xrange(num_bins - 1):
        if count[i] == 0:
            frac = 0
        else:
            frac = float(nhits[i]) / count[i]
        print "%f\t%d\t%d\t%f\t%f" % (ranges[i], count[i], nhits[i], frac, float(count[i]) / len(hits))

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
        print "usage: %s <classification out> <classification labels> <metrics> <block>" % sys.argv[0]
        sys.exit(-1)
    out_dir = sys.argv[1]
    labels_dir = sys.argv[2]
    metrics_dir = sys.argv[3]
    block = sys.argv[4]
    #print "loading"; print out_dir; print labels_dir; print metrics_dir; print block
    data = load_all(out_dir, labels_dir, metrics_dir, block)
    RANGES = [0.0, 0.1, 0.2, 0.6, 0.7, 1.0]
    METRIC_INDEX = 1

    group(data[0], data[1][METRIC_INDEX], RANGES)

