from object.libsvm_object import *

def compute_all(libsvm_file, libsvm_file2):
    o1 = get_next_object(libsvm_file)
    o2 = get_next_object(libsvm_file2)
    while o1 != -1:
        print (len(o2[1]) - len(o1[1]))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s <libsvm file> <libsvm file with inheritance>" % sys.argv[0]
        sys.exit(-1)

    libsvm_file = open(sys.argv[1])
    libsvm_file2 = open(sys.argv[2])

    compute_all(libsvm_file, libsvm_file2)
