import numpy as np
import hashlib
import scipy.spatial
import time
import multiprocessing


def generate_units(file_name):
    seqs = []
    queries = []
    with open(file_name) as f:
        seqs = [f.readline().split() for x in range(int(f.readline()))]
        queries = [f.readline().split() for x in range(int(f.readline()))]
    return seqs, queries


def hamming_distances(units, queries, hashes, out_dict, proc_num):
    differences = []
    for i_text, k_bits in queries:
        difference = 0
        i_text = int(i_text)
        k_bits = int(k_bits)
        for i, other_hash in enumerate(hashes):
            if i != i_text:
                #if (hd(hashes[i_text], other_hash)) <= k_bits:
                if hd2(hashes[i_text], other_hash, k_bits):
                    difference += 1
        differences.append(difference)
    out_dict[proc_num] = differences
    #return differences

# hamming distance from scipy
# time for example dataset: ~14s
def hd(hash1, hash2):
    return int(scipy.spatial.distance.hamming(hash1, hash2)*len(hash1))

# compute hamming distance, if more bits are different - break loop
# time for example dataset: ~8s
def hd2(hash1, hash2, max_difference):
    different_bits = 0
    for i,v in enumerate(hash1):
        if v != hash2[i]:
            different_bits += 1
            if different_bits > max_difference:
                return False
    return True


# helper function
def hash_md5(unit):
    return '{0:0128b}'.format(int(hashlib.md5(unit.encode()).hexdigest(), 16))

# simhash
def simhash(units):
    a = np.array([np.array([1 if x == '1' else -1 for x in hash_md5(unit)]) for unit in units])
    return np.array([1 if x >= 0 else 0 for x in np.sum(a, axis=0)])


if __name__ == '__main__':
    units, queries = generate_units('test2/R.in')
    t1 = time.time()
    with open('test2/R.in', 'r') as f:
        hashes = [simhash(f.readline().split()) for _ in range(int(f.readline()))]
    #hashes=np.load('lab1a_hashes.npy')
    t2 = time.time()
    print('simhash time', t2-t1)

    t1 = time.time()
    out_dict=dict()
    hamming_distances(units, queries, hashes, out_dict, 0)
    differences=out_dict[0]
    #differences=np.load('lab1a_differences.npy')
    t2 = time.time()

    print('differences time', t2-t1)

    with open('lab1a_differences.txt', 'w') as f:
        for item in differences:
            f.write('%s\n' % item)


