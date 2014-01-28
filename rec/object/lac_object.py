from collections import defaultdict
from numpy import *

import sys, os, math

# Modulo de I/O para o formato LAC


#carrega todos os objetos em memoria

def get_objects(lac_file):
    classes = {}
    words = {}
    for line in lac_file:
        c = set()
        w = set()
        raw_data = line.split()
        ID = int(raw_data[0])
        for term_raw_data in raw_data[1:]:
            try:
                tipo, term = term_raw_data.split('=')
            except:
                print >>sys.stderr, term_raw_data

            if tipo == "CLASS":
                c.add(int(term))
            else:
                w.add(int(term))

        classes[ID] = c
        words[ID] = w

    return (classes, words)





