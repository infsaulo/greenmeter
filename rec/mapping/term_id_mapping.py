import sys

def hashcode2string(file):
    dict = {}
    for line in file:
        spl = line.split()
        hashcode = int(spl[len(spl) - 1])
        string = spl[0]
        dict[hashcode] = string
    return dict
    

def id2hashcode(file):
    dict = {}
    for line in file:
        spl = line.split()
        hashcode = int(spl[0])
        id = int(spl[1])
        dict[id] = hashcode
    return dict
    
def id2string(file):
    dict = {}
    for line in file:
        spl = line.split()
        string = spl[0]
        id = int(spl[1])
        dict[id] = string
    return dict

def string2id(file):
    dict = {}
    for line in file:
        spl = line.split()
        string = spl[0]
        id = int(spl[1])
        dict[string] = id
    return dict

#Programa principal

if __name__ == "__main__":
    
    if len(sys.argv) != 3 :
        print "Usage: python %s <hashcode2id> <string2hashcode>" % sys.argv[0]
        sys.exit()
    
    file1 = open(sys.argv[1])
    file2 = open(sys.argv[2])
    
    m1 = id2hashcode(file1)
    m2 = hashcode2string(file2)
    
    for key in m1:
        print m2[m1[key]], key
    
