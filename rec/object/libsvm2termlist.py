from libsvm_object import *

def convert(filename):
    file = open(filename)
    object = get_next_object()
    file.close()
    