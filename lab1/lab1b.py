import numpy as np
import hashlib
import scipy.spatial
import time
import multiprocessing
import SimHash


def hash2int(band, _hash):
    return hash(_hash[band*16:band*16+16].tostring())


if __name__ == '__main__':

    units, queries = SimHash.generate_units('lab1B_primjer/test0/R.in')

    t1 = time.time()
    '''
    procs = []
    manager1 = multiprocessing.Manager()
    md1 = manager1.dict()
    for proc_num in range(4):
        procs.append(multiprocessing.Process(target=simhash, args=(units[12500*proc_num:12500*(proc_num+1)], md1, proc_num)))
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    hashes = []
    for num in range(len(md1)):
        hashes += md1[num]

    np.save('lab1b_0_hash.npy', hashes)
    '''
    hashes=np.load('lab1b_0_hash.npy')

    t2 = time.time()
    t_simhash = t2-t1
    print('simhash 50k', t_simhash)

    ## hashes_bands
    t1 = time.time()
    hashes_bands = []
    for _hash in hashes:
        hashes_bands.append([hash2int(i, _hash) for i in range(8)])
    t2 = time.time()
    t_hashes_bands = t2-t1
    print('{} hashes to band hashes: {}'.format(len(hashes), t_hashes_bands))



    t1 = time.time()
    # candidates - collection of 8 dicts. each dict is one band, eg. candidates[0] contain dict of similarity of first band
    candidates = dict()
    for band_num in range(8):
        temp = dict()
        for _iter, _hash in enumerate(hashes):
            band_hash = hash2int(band_num, _hash)
            if band_hash not in temp:
                temp[band_hash] = set()
            temp[band_hash].add(_iter)
        candidates[band_num] = temp

    t2 = time.time()
    t_candidates = t2-t1
    print('candidates', t_candidates)




    t1 = time.time()
    differences = []
    for qnum, maxbits in queries:
        similar_num = 0
        checked = set()
        for i in range(8):
            #print('band {},  {}'.format(i, qnum))
            #print(candidates[i][hashes_bands[qnum][i]])
            for candidate in candidates[i][hashes_bands[qnum][i]]:
                if candidate not in checked:
                    if SimHash.hd2(hashes[qnum], hashes[candidate], maxbits):
                        similar_num += 1
                    checked.add(candidate)
                else:
                    #print(' {} check!'.format(candidate))
                    pass
        #print('similars my: {}'.format(similar_num))
        differences.append(similar_num-1)

    t2 = time.time()
    t_each_query = t2-t1
    print('t_each_query', t_each_query)



    with open('lab1b_differences.txt', 'w') as f:
        for item in differences:
            f.write('%s\n' % item)


'''
    candidates = dict({})
    b = 8 #bands
    for band in range(b):
        buckets = dict({})
        for current_id in range(N-1):
            _hash = hashes[current_id]
            val = hash2int(band, _hash)
            texts_in_buckets = dict({})
            if buckets[val] != {}:
                texts_in_buckets = buckets[val]
                for text_id in texts_in_buckets:
                    candidates[current_id].append(text_id)
                    candidates[text_id].append(current_id)
            else:
                texts_in_buckets = {}
            texts_in_buckets.append(current_id)
            buckets[val] = texts_in_buckets

'''

'''
    procs = []
    manager = multiprocessing.Manager()
    md = manager.dict()
    for proc_num in range(4):
        procs.append(multiprocessing.Process(target=hamming_distances, args=(units, queries[12500*proc_num:12500*(proc_num+1)], hashes, md, proc_num)))
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    differences = []
    for num in range(len(md)):
        differences += md[num]

    #np.save('differences.npy', differences)
    #differences=np.load('differences.npy')

    t3 = time.time()

    print('simhash time', t2-t1)
    print('differences time', t3-t2)
    print('all time', t3-t1)

    with open('differences.txt', 'w') as f:
        for item in differences:
            f.write('%s\n' % item)

'''
