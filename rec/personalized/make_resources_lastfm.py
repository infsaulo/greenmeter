import sys, csv
from processing.text_filtering import *
from inout import load_list, load_postings_resource_tags

#LastFM:  ID,INT_ID,TITLE,TAG,DESC,CATEG,WIKICHANGED,LISTENERS,PLAYCOUNT,MBID,STREAM,URL
#YouTube: ID,INT_ID,TITLE,TAG,DESC,CATEG,AUTHOR,DURATION,LAT,LONG,AVGRAT,MINRAT,MAXRAT,RATCOUNT,VIEWCOUNT,FAVCOUNT


def print_resources(row, stopw, word_map, wid, resource_tags):
    oid = row[0].replace(" ", "+")
    spl = oid.split("/")
    oid = spl[len(spl) - 1]
    tags = row[3][1:len(row[3]) - 1]
    title = row[2]
    desc = row[4]
    cat = row[5].replace(" ", "+")

    tags_split = split_words(tags)

    if oid in resource_tags:
        for t in resource_tags[oid]:
            tags_split += split_words(t)

    desc_split = split_words(desc)
    title_split = split_words(title)

    obj_words = tags_split + desc_split + title_split

    nstopw = 0
    for w in obj_words:
        if w in stopw:
            nstopw += 1

    if nstopw < 3:
        return

    textual_features = {}

    textual_features["TAG"] = process(tags_split, stopw)
    textual_features["TITLE"] = process(title_split, stopw)
    textual_features["DESCRIPTION"] = process(desc_split, stopw)
    textual_features["CAT"] = []
    textual_features["CAT"].append(cat)

    print "ID %s" % oid,

    for (name, words) in textual_features.items():
        print "| %s" % name,
        for w in words:
            if w not in word_map:
                word_map[w] = wid[0]
                wid[0] += 1
            print word_map[w],
    print


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print >>sys.stderr, "usage: %s <csv file> <grouped postings> <stopwords file> <word map (output)>" % sys.argv[0]
        sys.exit(-1)

    stopw_file = open(sys.argv[3])
    reader = csv.reader(open(sys.argv[1]))
    postings_filename = sys.argv[2]
    out = open(sys.argv[4], "w")
    resource_tags = load_postings_resource_tags(postings_filename)
    csv.field_size_limit(999999999)
    
    stopw = set()
    for line in stopw_file:
        stopw.add(line.strip())
    stopw_file.close()

    n = 1
    wid = [1]
    word_map = {}
    for row in reader:
        if n != 1:
            print_resources(row, stopw, word_map, wid, resource_tags)
        n = n + 1

    for (w, i) in word_map.items():
        print >>out, w, i

