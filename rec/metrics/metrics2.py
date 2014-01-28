#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from collections import defaultdict
from object.libsvm_object import *
from operator import itemgetter
import sys, os, math

# Encapsula todas as metricas que serao usadas como variaveis no GP
# Como essas metricas nao mudam, elas sao pre-computadas e armazenadas em tabelas

class Metrics:
    def __init__(self, train_filename, files, k, fmin, fmax):
        self.train_filename = train_filename
        self.files = files
        self.k = k
        self.fmin = fmin
        self.fmax = fmax
        (self.stats, self.ftc, self.num_objects) = self.compute_term_stats()
        self.compute_instance_stats()

    #Metodos para calcular metricas

    #stats = [FT, IG, H, H_]
    def compute_term_stats(self):
        train = open(self.train_filename)
        stats = {}
        ftc = defaultdict(lambda: defaultdict(float))
        fc = defaultdict(float)

        num_objects = 0
        train_object = get_next_object(train)
        while train_object != None:
            num_objects += 1
            category = train_object[0]
            fc[category] += 1
            for term in train_object[1]:
                if term not in stats:
                    stats[term] = [0 for i in xrange(4)]
                stats[term][0] += 1
                ftc[term][category] += 1
            train_object = get_next_object(train)
        train.close()
        self.n_train = num_objects
        Hc = 0.0
        for c in fc:
            pc = fc[c] / num_objects
            Hc += pc * math.log(pc)

        for t in stats:
            pt = stats[t][0] / num_objects
            ptn = 1.0 - pt
            Ht = 0.0
            Htn = 0.0
            for c in fc:
                pc_t = ftc[t][c] / stats[t][0]
                pc_tn = (fc[c] - ftc[t][c]) / (num_objects - stats[t][0])
                if pc_t != 0.0:
                    Ht += pc_t * math.log(pc_t)
                if pc_tn != 0.0:
                    Htn += pc_tn * math.log(pc_tn)
            stats[t][2] = -Ht
            stats[t][3] = -Htn
            Ht *= pt
            Htn *= ptn
            stats[t][1] = -Hc + Ht + Htn

        return (stats, ftc, num_objects)


    # Cada arquivo em files contem o conteudo de um bloco associado ao mesmo objeto
    def compute_instance_spread(self, instance):
        spread = defaultdict(float)
        for file in self.files:
            block = get_next_object(file)
            for t in block[1]:
                    spread[t] += 1
        return spread

    def compute_instance_stats(self):
        fi_file = open(self.train_filename)
        instance = get_next_object(fi_file)
        while instance != None:
            conc_list = []
            conc_spread_list = []
            spread_list = []
            iff_list = []
            iff_spread_list = []
            iff_conc_list = []
            conc_sp_iff_list = []
            spread = self.compute_instance_spread(instance[1])
            cat = instance[0]
            for t in instance[1]:
                freq = self.stats[t][0]
                if  freq < self.fmin or freq > self.fmax:
                    continue
                sp = spread[t]
                iff = math.log(self.num_objects / freq)
                iff_list.append(iff)
                conc = self.ftc[t][cat] / freq
                spread_list.append(sp)
                conc_list.append(conc)
                conc_spread_list.append(conc * sp)
                iff_conc_list.append(conc * iff)
                iff_spread_list.append(sp * iff)
                conc_sp_iff_list.append(sp * conc * iff)
            if len(conc_list) != 0:
                print self.media_top(spread_list), self.media_top(conc_list), self.media_top(conc_spread_list), self.media_top(iff_spread_list), self.media_top(iff_conc_list), self.media_top(conc_sp_iff_list), self.media_top(iff_list), len(conc_list)

            instance = get_next_object(fi_file)

    def media_top(self, values):
        n = 0
        m = 0
        for v in sorted(values):
            n += 1
            if n > self.k:
                break
            m += v
        return m / n

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "usage: %s <input file> <k (top terms)> <fmin> <fmax> <feature filenames list>" % sys.argv[0]
        sys.exit(-1)
    k = int(sys.argv[2])
    fmin = int(sys.argv[3])
    fmax = int(sys.argv[4])
    filename = sys.argv[1]
    files = []
    for i in range(5, len(sys.argv)):
        files.append(open(sys.argv[i]))

    metrics = Metrics(filename, files, k, fmin, fmax)


