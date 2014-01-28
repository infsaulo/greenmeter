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
    def __init__(self, train_filename, test_filename1, test_filename2, files, minsup, ks, kd, kr, num_test_objects):
        self.train_filename = train_filename

        #Carrega dados de teste
        test1 = open(test_filename1)
        test2 = open(test_filename2)
        self.N = num_test_objects
        (self.test_cats, self.test_part1) = get_terms(test1)
        self.test_part1 = self.test_part1[0:self.N]
        self.test_part2 = get_terms(test2)[1]
        self.test_part2 = self.test_part2[0:self.N]
        assert len(self.test_part1) == len(self.test_part2)
        test1.close()
        test2.close()

        #filenames = os.listdir(indirname)
        self.files = files
        #for filename in filenames:
        #    self.files.append(open(indirname + "/" + filename))
        self.minsup = minsup
        self.ks = ks
        self.kd = kd
        self.kr = kr

        self.candidates = [set() for i in xrange(len(self.test_part1))]

        (self.stats, self.ftc) = self.compute_term_stats()
        self.f_intersection = self.compute_cooccur() #frequencia da co-ocorrencia de dois termos

        self.spread = self.compute_spread()
        self.vote = self.compute_vote()


    #Metodos para calcular metricas

    def stab_promotion(self, k, f):
        return k / (k + math.fabs(math.log(f) - k))

    def compute_vote(self):
        votes = []
        for i in xrange(len(self.test_part1)):
            vote = {} #VOTE, VOTE+, SUM, SUM+
            for u in self.test_part1[i]:
                f_intersec = self.f_intersection[u]
                if u in self.stats:
                    fu = self.stats[u][0]
                else:
                    continue
                stab = self.stab_promotion(self.ks, fu + 1.0)
                position = 0
                for pair in sorted(f_intersec.items(), key=itemgetter(1), reverse=True):
                    c = pair[0]
                    value = float(pair[1])
                    if c not in self.test_part1[i]: #nao recomendar palavras que jah estao lah
                        if c not in vote:
                            vote[c] = [0.0 for x in xrange(4)]
                        confidence = value / fu
                        vote[c][0] += 1.0
                        vote[c][1] += stab * self.rank_promotion(position)
                        vote[c][2] += confidence
                        vote[c][3] += confidence * stab * self.rank_promotion(position)
                        position += 1
            for c in vote:
                self.candidates[i].add(c)
            votes.append(vote)
        return votes


    def compute_freq(self):
        train = open(self.train_filename)
        ft = defaultdict(float)
        train_object = get_next_object(train)
        while train_object != None:
            for term in train_object[1]:
                ft[term] += 1
            train_object = get_next_object(train)
        train.close()
        return ft

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

        return (stats, ftc)

    def compute_cooccur(self):
        train = open(self.train_filename)
        f_intersection = defaultdict(lambda: defaultdict(int)) #frequencia da intersecao de dois termos
        train_object = get_next_object(train)
        while train_object != None:
            for t1 in train_object[1]:
                if self.stats[t1][0] >= self.minsup:
                    for t2 in train_object[1]:
                        if self.stats[t2][0] >= self.minsup and t1 < t2:
                            f_intersection[t1][t2] += 1
                            #f_intersection[t2][t1] += 1
            train_object = get_next_object(train)
        train.close()
        
        #Elimina co-ocorrencias menores que o suporte minimo
        cooccurences = defaultdict(lambda: defaultdict(int))
        for t1 in f_intersection:
            for t2 in f_intersection[t1]:
                if f_intersection[t1][t2] >= self.minsup:
                    cooccurences[t1][t2] = f_intersection[t1][t2]
                    cooccurences[t2][t1] = f_intersection[t1][t2]

        return cooccurences

    # Cada arquivo em files contem o conteudo de um bloco associado ao mesmo objeto
    def compute_instance_spread(self, test_part1):
        spread = defaultdict(float)
        #for t in test_part1:
        #    spread[t] += 1
        for file in self.files:
            block = get_next_object(file)
            for t in block[1]:
                if t not in test_part1:
                    spread[t] += 1
        return spread

    def compute_spread(self):
        spread = defaultdict(lambda: defaultdict(int))
        for i in xrange(len(self.test_part1)):
            spread[i] = self.compute_instance_spread(self.test_part1[i])
            for t in spread[i]:
                if t not in self.test_part1[i]:
                    self.candidates[i].add(t)
        return spread

    def compute_stability(self):
        stab = defaultdict(float)
        for t in self.stats:
            stab[t] = self.ks / (self.ks + math.fabs(self.ks - math.log(self.stats[t][0])))
        return stab

    def compute_descriptiveness(self):
        desc = defaultdict(float)
        for t in self.stats:
            desc[t] = self.kd / (self.kd + math.fabs(self.kd - math.log(self.stats[t][0])))
        return desc

    def rank_promotion(self, position):
        return self.kr / (self.kr + position)


