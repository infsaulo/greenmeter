from object.libsvm_object import *

def read_map_int_float(file):
    map = defaultdict(float)
    for line in file:
        split = line.split()
        key = int(split[0])
        value = float(split[1])
        map[key] = value
    return map

def compute_all(libsvm_file, libsvm_file2, infogain1, infogain2):

    o1 = get_next_object(libsvm_file)
    o2 = get_next_object(libsvm_file2)

    while o1 != -1:
        sum_before = 0.0
        sum_after = 0.0
        for t in o1[1].keys():
            sum_before += infogain1[t]
        for t in o2[1].keys():
            sum_after += infogain2[t]
        sum_before /= len(o1[1])
        sum_after /= len(o2[1])
        print (sum_after - sum_before)/sum_before

        o1 = get_next_object(libsvm_file)
        o2 = get_next_object(libsvm_file2)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "usage: %s <libsvm file> <libsvm file with inheritance> <infogain before> <infogain after>" % sys.argv[0]
        sys.exit(-1)

    libsvm_file = open(sys.argv[1])
    libsvm_file2 = open(sys.argv[2])
    infogain1_file = open(sys.argv[3])
    infogain2_file = open(sys.argv[4])
    
    infogain1 = read_map_int_float(infogain1_file)
    infogain2 = read_map_int_float(infogain2_file)

    compute_all(libsvm_file, libsvm_file2, infogain1, infogain2)
