
import sys, math
from collections import defaultdict
from personalized.inout import load_graph, load_postings_user_tags, print_list
from recommender.util import get_top_ranked


def compute_tag_freq(user_postings):
    freq = defaultdict(float)
    for tag in user_postings:
        freq[tag] += 1.0
    return freq


#Calcula um score de tags baseando-se na frequecia de uso das tags por um usuario e seus vizinhos na rede

def user_tag_freq_rank(rank, user, tag_freq, hop, w, graph, postings, maxhop):
    #calcula, sob demanda, frequencia de uso de tags para um usuario
    if user not in tag_freq:
        if user in postings:
            tag_freq[user] = compute_tag_freq(postings[user])
        else:
            tag_freq[user] = {}

    for (t, tf) in tag_freq[user].items():
        rank[t] += tf * math.exp(-hop) * w
    if hop == maxhop:
        return
    if user in graph:
        for (v, sim) in graph[user]:
            user_tag_freq_rank(rank, v, tag_freq, hop + 1, sim, graph, postings, maxhop)



if __name__ == "__main__":
    if len(sys.argv) != 5:
        print >>sys.stderr, "usage: %s <graph> <train> <test> <#hops>" % sys.argv[0]
        sys.exit(-1)

    graph = load_graph(sys.argv[1])
    train = load_postings_user_tags(sys.argv[2])
    test = open(sys.argv[3])
    h = int(sys.argv[4])
    tag_freq = {}
    
    for line in test:
        s = line.split(", ")
        user = s[0]
        rank = defaultdict(float)
        user_tag_freq_rank(rank, user, tag_freq, 0, 1.0, graph, train, h)
        print_list(get_top_ranked(rank, 999999999))
    test.close()






