from collections import defaultdict
from operator import itemgetter


def get_top_ranked(candidates, num_rec):
    result = []
    n = 1
    for pair in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if n > num_rec:
            break
        n = n + 1
        result.append(pair[0])
    return result

def get_top_ranked_map(candidates, num_rec):
    result = {}
    n = 1
    for (key, value) in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if n > num_rec:
            break
        n = n + 1
        result[key] = value
    return result

def rescore(scores, factor):
    if len(scores) > 0:
        m = max(scores.values())
        if m == 0:
            return
        for s in scores:
            scores[s] = (scores[s] * factor)/m

def merge_scores(scores_array):
    final_score = defaultdict(float)
    all_candidates = set()
    for score in scores_array:
        for t in score:
            all_candidates.add(t)
    for w in all_candidates:
        prod = 1.0
        for score in scores_array:
            prod *= (1.0 - score[w])
        final_score[w] = 1.0 - prod
    return final_score



def index_max(dict):
    if len(dict) == 0:
        print >>sys.stderr, "Erro: extracao de valor maximo de lista vazia"
        sys.exit(-1)
    maxval = -999999999
    for i in dict:
        if dict[i] > maxval:
            imax = i
            maxval = dict[i]
    return imax



