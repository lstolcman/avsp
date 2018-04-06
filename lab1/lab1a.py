import numpy as np
import hashlib
import scipy.spatial
import time


def generate_units(file_name):
    seqs = []
    queries = []
    with open(file_name) as f:
        num_of_seqs = int(f.readline())
        for seq in range(num_of_seqs):
            seqs.append(f.readline().rstrip('\n').rstrip(' ').split(' '))
        num_of_queries = int(f.readline())
        for query in range(num_of_queries):
            queries.append(f.readline().rstrip('\n').rstrip(' ').split(' '))
    return seqs, queries


def simhash(units):
    hashes = []
    for unit in units:
        unit_elemets = np.empty((0, 128))
        for element in unit:
            element_md5_hex = hashlib.md5(element.encode()).hexdigest()
            # make binary version, preserve 128bit lengts (leading zeros)
            element_md5_bin = format(int(element_md5_hex, 16), '0128b')
            # 0 -> -1  
            element_md5_bin2 = np.array([(1 if int(v) > 0 else -1) for v in element_md5_bin])
            # create matrix
            unit_elemets = np.append(unit_elemets, [element_md5_bin2], axis=0)
        # sum columns
        unit_sum = np.sum(unit_elemets, axis=0)
        # replace -1s to 0s
        unit_hash_tab = np.array([(1 if int(v) >= 0 else 0) for v in unit_sum])
        #unit_hash_bin = ''.join(map(str, unit_hash_tab))
        #unit_hash_hex = hex(int(unit_hash_bin, 2))[2:]
        hashes.append(unit_hash_tab)
    return hashes

def hamming_distances(units, queries):
    differences = []
    for i_text, k_bits in queries:
        i_text = int(i_text)
        k_bits = int(k_bits)
        difference = 0
        for other_hash in hashes[:i_text]:
            if (hd(hashes[i_text], other_hash)) <= k_bits:
                difference += 1
        for other_hash in hashes[i_text+1:]:
            if (hd(hashes[i_text], other_hash)) <= k_bits:
                difference += 1
        differences.append(difference)
    return differences

def hd(hash1, hash2):
    return int(scipy.spatial.distance.hamming(hash1, hash2)*len(hash1))


if __name__ == '__main__':
    units, queries = generate_units('test2/R.in')

    #hashes = simhash(units)
    #np.save('simhash.npy', hashes)
    hashes=np.load('simhash.npy')
    differences = hamming_distances(units, queries)
    np.save('differences.npy', differences)

    f = open('differences.txt', 'w')
    f.write('\n'.join(map(str, differences)))
    f.close()






