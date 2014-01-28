
from personalized.inout import print_list_file, load_list
import sys
from random import shuffle, seed


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s <test postings> <outpath>" % sys.argv[0]
        sys.exit(-1)

    test = open(sys.argv[1])
    input_tags = open(sys.argv[2] + ".part1", "w")
    expected_answer = open(sys.argv[2] + ".part2", "w")
    seed(0)

    for line in test:
        split = load_list(line.strip(), " ")
        tags = set(split[2:])
        user = split[0]
        resource = split[1]

        ntags = len(tags)
        half_tags = ntags/2
        taglist = [x for x in tags]
        shuffle(taglist)
        print_list_file(expected_answer, taglist[:half_tags], " ")
        print_list_file(input_tags, [user, resource] + taglist[half_tags:], " ")

    input_tags.close()
    expected_answer.close()

