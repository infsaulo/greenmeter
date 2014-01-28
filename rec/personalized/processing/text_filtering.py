import re
from stemmer import *

def split_words(string):
    words = []
    s = string.lower().split()
    validc = "\w|\-"
    for tok in s:
        w = ""
        for i in xrange(len(tok)):
            c = tok[i]
            if re.match(validc, c) != None:
                w += c

        if len(w) > 0:
            words.append(w)
    return words

def remove_stopwords(words, stopw):
    res = []
    for w in words:
        if w not in stopw:
            res.append(w)
    return res


def process(wordlist, stopw):
    p = PorterStemmer()
    res = []
    words = remove_stopwords(wordlist, stopw)
    for w in words:
        res.append(p.stem(w, 0, len(w) - 1))
    return res


