from collections import defaultdict
from numpy import *

import sys, os, math

# Modulo de I/O para o formato LIBSVM

def get_next_object(libsvm_file):
    line = libsvm_file.readline()
    if line == "":
        return None
    while '#' in line:
        line = libsvm_file.readline()
    raw_data = line.split()
    weights = {}
    cat = int(raw_data[0])

    for term_raw_data in raw_data[1:]:
        try:
            rtid, rtweight = term_raw_data.split(':')
        except:
            print >>sys.stderr, term_raw_data

        tid, tweight = int(rtid), float(rtweight)
        weights[tid] = tweight

    return (cat, weights)


def get_next_term_list(libsvm_file):
    line = libsvm_file.readline()
    if line == "":
        return None
    while '#' in line:
        ID = line[1:len(line)-1]
        ID = ID.replace(" ", "+")
        ID = ID.replace(".xml", "")
        line = libsvm_file.readline()
    raw_data = line.split()
    terms = []
    if raw_data[0] == "null":
        cat = -42
    else:
        cat = int(raw_data[0])

    for term_raw_data in raw_data[1:]:
        try:
            tid = int(term_raw_data.split(':')[0])
        except:
            print >>sys.stderr, term_raw_data

        terms.append(tid)

    return (cat, terms, ID)


#Obtem a concatenacao dos atributos textuais do proximo objeto

#def get_next_concat(files):
#    terms = []
#    for libsvm_file in files:
#        line = libsvm_file.readline()
#        if line == "":
#            return None
#        while '#' in line:
#            line = libsvm_file.readline()
#        raw_data = line.split()
#        cat = int(raw_data[0])
#
#        for term_raw_data in raw_data[1:]:
#            try:
#                tid = int(term_raw_data.split(':')[0])
#            except:
#                print >>sys.stderr, term_raw_data
#
#            terms.append(tid)
#
#    return (cat, terms)


#carrega todos os objetos em memoria

def get_objects(libsvm_file):
    objects = []
    cats = []
    for line in libsvm_file:
        if '#'in line:
            continue
        raw_data = line.split()
        weights = {}
        cats.append(int(raw_data[0]))
        for term_raw_data in raw_data[1:]:
            try:
                rtid, rtweight = term_raw_data.split(':')
            except:
                print >>sys.stderr, term_raw_data

            tid, tweight = int(rtid), float(rtweight)
            weights[tid] = tweight

        objects.append( weights )
    return (cats, objects)


def get_terms(libsvm_file):
    objects = []
    cats = []
    for line in libsvm_file:
        if '#'in line:
            continue
        raw_data = line.split()
        terms = set()
        cats.append(int(raw_data[0]))
        for term_raw_data in raw_data[1:]:
            try:
                tid = int(term_raw_data.split(':')[0])
            except:
                print >>sys.stderr, term_raw_data

            terms.add(tid)
        objects.append(terms)
    return (cats, objects)


def get_term_lists(libsvm_file):
    objects = []
    cats = []
    ids = []
    for line in libsvm_file:
        if '#'in line:
            ID = line[:len(line) - 1]
            ids.append(ID)
            continue
        raw_data = line.split()
        terms = []
        cats.append(int(raw_data[0]))
        for term_raw_data in raw_data[1:]:
            try:
                tid = int(term_raw_data.split(':')[0])
            except:
                print >>sys.stderr, term_raw_data

            terms.append(tid)
        objects.append(terms)
    return (cats, objects, ids)


def sim(o1, o2):
    return dot(o1, o2) #se a norma de ambos forem iguais  a1 !!!

def calcnorm(o):
    sumsq = 0.0
    for t in o:
        sumsq += o[t] * o[t]
    return math.sqrt(sumsq)

def normalize(o):
    n = calcnorm(o)
    for t in o:
        o[t] /= n

def dot(o1, o2):
    sum = 0.0
    for t in o1:
        if t in o2:
            sum += o1[t] * o2[t]

    return sum


