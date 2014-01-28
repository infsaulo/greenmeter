
from personalized.inout import print_list
import sys

def get_user_set(file):
    users = set()
    for line in file:
        u = line.split(", ")[0]
        users.add(u)
    return users

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "usage: %s <train> <test> <graph>" % sys.argv[0]
        sys.exit(-1)

    train = open(sys.argv[1])
    test = open(sys.argv[2])
    graph = open(sys.argv[3])

    test_users = get_user_set(test)
    train_users = get_user_set(train)
    test.close()
    train.close()

    for line in graph:
        split1 = line.split(", ")
        u1 = split1[0]
        if u1 not in train_users and u1 not in test_users:
            continue
        l = []
        l.append(u1)
        for s1 in split1[1:]:
            split2 = s1.split()
            u2 = split2[0]
            if u2 not in train_users and u2 not in test_users:
                continue
            if u1 in test_users and u2 in test_users:
                continue
            l.append(s1)
        print_list(l)


