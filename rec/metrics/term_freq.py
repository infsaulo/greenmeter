#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from ..object.libsvm_object import *
from ..object.textual_features_concat import get_next_concat_TF_weighted

import sys, os, math

def compute_freq(train_filename):
    train = open(train_filename)
    ft = defaultdict(int)
    train_object = get_next_object(train)
    while train_object != None:
        for term in train_object[1]:
            ft[term] += 1
        train_object = get_next_object(train)
    train.close()
    return ft

def compute_freq_and_train_length(train_filename):
    train = open(train_filename)
    ft = defaultdict(int)
    n = 1
    train_object = get_next_object(train)
    while train_object != None:
        n += 1
        for term in train_object[1]:
            ft[term] += 1
        train_object = get_next_object(train)
    train.close()
    return (ft, n)

def compute_DF_and_train_length(train_filename, fieldnames):

    file = open(train_filename)
    df = defaultdict(float)
    n = 1
    train_object = get_next_concat_TF_weighted(file)
    while train_object != None:
        n += 1
        bagow = set()
        for field in fieldnames:
            for t in train_object[field]:
                bagow.add(t)
        for term in bagow:
            df[term] += 1.0
        train_object = get_next_concat_TF_weighted(file)

    file.close()
    return (df, n)

#Computa Feature Frequency considerando apenas objetos de um conjunto passado como parametro (oids)

def compute_FF_trainset(resources, fieldnames, oids):
    ff = {}
    for name in fieldnames:
        ff[name] = defaultdict(float)

    for oid in oids:
        train_object = resources[oid]
        for fieldname in fieldnames:
            field = train_object[fieldname]
            for t in field:
                ff[fieldname][t] += 1.0
    return ff


def compute_FF_and_train_length(train_filename, fieldnames):

    ff = {}
    for name in fieldnames:
        ff[name] = defaultdict(float)

    file = open(train_filename)
    n = 1
    train_object = get_next_concat_TF_weighted(file)
    while train_object != None:
        n += 1
        for fieldname in fieldnames:
            field = train_object[fieldname]
            for t in field:
                ff[fieldname][t] += 1.0

        train_object = get_next_concat_TF_weighted(file)

    file.close()
    return (ff, n)



#obj = term list

def compute_TF(obj, fieldnames):

    tf = defaultdict(float)
    for field in fieldnames:
        for t in obj[field]:
            tf[t] += 1.0
    return tf


#obj = term set (or dictionary)

def compute_TS(obj, fieldnames):

    ts = defaultdict(float)
    for field in fieldnames:
        for t in obj[field]:
            ts[t] += 1.0
    return ts


def compute_TF_from_term_map(obj, fieldnames):

    tf = defaultdict(float)
    for field in fieldnames:
        o = obj[field]
        for t in o:
            tf[t] += o[t]
    return tf

def compute_TFxFS(obj, fs):

    tf = defaultdict(float)
    for field in fs:
        o = obj[field]
        for t in o:
            tf[t] += o[t] * fs[field]
    return tf

def compute_FSsum(obj, fs):

    tf = defaultdict(float)
    for field in fs:
        o = obj[field]
        for t in o:
            tf[t] += fs[field]
    return tf

def compute_internal_frequency_metrics_normalized(obj, fs):
	metrics = {} #TS, TF, TFxFS, FSsum
	sum_fs = sum(fs.values())
	inv_number_fields = 1.0/len(fs)
	inv_number_terms = 1.0 / sum([len(obj[field]) for field in fs])
	for (field, fs_value) in fs.items():
		o = obj[field]
		inv_number_terms_field = 1.0/(len(o)+1)
		for (t, tf) in o.items():
			if t not in metrics:
				metrics[t] = [0.0 for x in xrange(4)]
			m = metrics[t]
			m[0] += inv_number_fields
			m[1] += tf * inv_number_terms
			m[2] += tf * inv_number_terms_field * fs_value/sum_fs
			m[3] += fs_value/sum_fs

	return metrics

def compute_internal_frequency_metrics(obj, fs):
    metrics = {} #TS, TF, TFxFS, FSsum
    for (field, fs_value) in fs.items():
        o = obj[field]
        for (t, tf) in o.items():
            if t not in metrics:
                metrics[t] = [0.0 for x in xrange(4)]
            m = metrics[t]
            m[0] += 1.0
            m[1] += tf
            m[2] += tf * fs_value
            m[3] += fs_value
    return metrics


def compute_FIS(obj, fieldnames):
    fis = {}
    ts = compute_TS(obj, fieldnames)
    for field in fieldnames:
        avgTS = 0.0
        o = obj[field]
        for t in o:
            avgTS += ts[t]
        if len(o) > 0:
            avgTS /= len(o)
        fis[field] = avgTS
    return fis

def compute_FS(train_filename, fieldnames):
    fs = {}
    file = open(train_filename)
    train_object = get_next_concat_TF_weighted(file)
    for fieldname in fieldnames:
        fs[fieldname] = 0.0
    n = 1.0

    while train_object != None:
        fis = compute_FIS(train_object, fieldnames)
        for fieldname in fis:
            fs[fieldname] += fis[fieldname]
        train_object = get_next_concat_TF_weighted(file)
        n += 1.0

    for fieldname in fieldnames:
        fs[fieldname] /= n

    file.close()
    return fs

def compute_IDF(freq, N):
    return math.log((N + 1.0) / (freq + 1.0))

def compute_stability(freq, ks):
    return ks / (ks + math.fabs(ks - math.log(freq + 1.0)))

def rank_promotion(position, kr):
    return kr / (kr + position)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: %s <libsvm file>" % sys.argv[0]
        sys.exit(-1)

    ft = compute_freq(sys.argv[1])
    for t in ft:
        print t, ft[t]
