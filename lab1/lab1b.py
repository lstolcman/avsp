import numpy as np
import hashlib
import scipy.spatial
import time
import multiprocessing
import SimHash


def hash2int(band, _hash):
    return hash(_hash[band*16:band*16+16].tostring())


if __name__ == '__main__':

    t_num = 'test2'
    units, queries = SimHash.generate_units('lab1B_primjer/'+t_num+'/R.in')

    t1 = time.time()
    #'''
    procs = []
    manager1 = multiprocessing.Manager()
    md1 = manager1.dict()
    for proc_num in range(4):
        procs.append(multiprocessing.Process(target=SimHash.simhash, args=(units[12500*proc_num:12500*(proc_num+1)], md1, proc_num)))
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    hashes = []
    for num in range(len(md1)):
        hashes += md1[num]

    np.save('lab1b_hash_'+t_num+'.npy', hashes)
    #'''
    #hashes=np.load('lab1b_hash_'+t_num+'.npy')
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

    np.save('lab1b_candidates_'+t_num+'.npy', hashes)
    #'''
    #candidates=np.load('lab1b_candidates_'+t_num+'.npy')
    t2 = time.time()
    t_candidates = t2-t1
    print('candidates', t_candidates)



    t1 = time.time()
    differences = []
    for qnum, maxbits in queries:
        similar_num = 0
        checked = set()
        checked.add(qnum)
        for i in range(8):
            #print('band {},  {}'.format(i, qnum))
            #print(candidates[i][hashes_bands[qnum][i]])
            for candidate in candidates[i][hashes_bands[qnum][i]]:
                if candidate not in checked:
                    #print('candidate {}  qnum {}'.format(candidate, qnum))
                    if SimHash.hd2(hashes[qnum], hashes[candidate], maxbits):
                        similar_num += 1
                    checked.add(candidate)
        #print('similars my: {}'.format(similar_num))
        differences.append(similar_num)

    np.save('lab1b_differences_'+t_num+'.npy', hashes)
    #'''
    #differences=np.load('lab1b_differences_'+t_num+'.npy')
    t2 = time.time()
    t_each_query = t2-t1
    print('t_each_query', t_each_query)



    with open('lab1b_differences_'+t_num+'.txt', 'w') as f:
        for item in differences:
            f.write('%s\n' % item)



