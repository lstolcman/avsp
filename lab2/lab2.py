import math

class DGIM():
    def __init__(self, window_size):
        self.window_size = int(window_size)
        self.buckets = {}
        self.current_bit_position = 0

    def __add_bucket(self, key, position):
        if key not in self.buckets:
            self.buckets[key] = []
        self.buckets[key].append(position)

    def __combine_buckets(self):
        for key, val in sorted(self.buckets.items()):
            if key in self.buckets and len(self.buckets[key]) > 2:
                # pop(0) pops first element from list
                elem_1st = self.buckets[key].pop(0)
                elem_2nd = self.buckets[key].pop(0)
                self.__add_bucket(2*key, (elem_1st[0], elem_2nd[1]))

    def add_stream(self, stream):
        for bit in stream:
            if bit is '1':
                self.__add_bucket(1, (self.current_bit_position, self.current_bit_position+1))
                # if there are too many buckets - combine them to bigger level
                self.__combine_buckets()
            self.current_bit_position += 1

    def calculate_ones(self, k):
        k = int(k)
        if k > self.window_size:
            raise ValueError('k ({}) larger than window size ({})'.format(k, self.window_size))

        # number of ones from buckets
        ones = []

        try:
            for key, bucket in sorted(self.buckets.items()):
                for bucket_element in reversed(bucket):
                    if (bucket_element[1]-1) >= (self.current_bit_position-k+1):
                        ones.append(key)
                    else:
                        # found last bucket - jump out of the all loops
                        raise Exception
        except Exception:
            pass

        ''' 
        AVSP_05a_Data_Streams_2.pdf @ p.34
        Last bucket - add half the size of the last bucket
        '''
        if ones:
            ones[-1] = math.floor(ones[-1]/2)

        return sum(ones)


if __name__ == '__main__':
    l=[]
    expected=[]
    with open('t.out','r') as s:
        expected=s.readlines()
    for i,v in enumerate(expected):
        expected[i]=int(v.rstrip())

    res = []
    with open('t.in', 'r') as s:
        l=s.readlines()

    for i, v in enumerate(l):
        l[i]=v.rstrip()


    #l=l[:24]
    expected=expected[:7]
    dgim = DGIM(l.pop(0))
    for i,v in enumerate(l):
        print(i)
        if v.startswith('q'):
            res.append(dgim.calculate_ones(v.split(' ')[1]))
        else:
            dgim.add_stream(v)


    with open('oldbranch.t.out', 'w') as old:
        for l in res:
            old.write(str(l))
            old.write('\n')
    print('eq', res==expected)
