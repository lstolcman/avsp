import math
import fileinput

class DGIM():
    def __init__(self, window_size):
        self.window_size = int(window_size)
        self.buckets = {}
        self.current_timestamp = 0

    def __add_bucket(self, size, timestamp):
        if size not in self.buckets:
            self.buckets[size] = []
        self.buckets[size].append(timestamp)

    def __combine_buckets(self):
        for size, _ in sorted(self.buckets.items()):
            if size in self.buckets and len(self.buckets[size]) > 2:
                # pop(0) pops first element from list
                elem_1st = self.buckets[size].pop(0)
                elem_2nd = self.buckets[size].pop(0)
                self.__add_bucket(2*size, elem_2nd)

    def __check_last_bucket(self):
        '''
        loop for checking if any bucket had to be deleted because it doesn't fit
        into widnow size anymore
        algorithm:
        iterate from the biggest bucket to the smallest bucket
            in a bucket, iterate one by one from the first element
            (first element in the buggest bucket is the first candidate to delete
            due to being too old for a window size)
        '''
        try:
            for size, items in reversed(sorted(self.buckets.items())):
                for inum, item in enumerate(items):
                    if (self.current_timestamp - self.window_size) >= item:
                        del self.buckets[size][inum]
                    else:
                        # found first buckets which is within window - do not continue
                        raise Exception
        except Exception:
            pass

    def add_stream(self, stream):
        for bit in stream:
            self.current_timestamp += 1
            self.__check_last_bucket()
            if bit is '1':
                self.__add_bucket(1, self.current_timestamp)
                self.__combine_buckets()

    def calculate_ones(self, k):
        k = int(k)
        if k > self.window_size:
            raise ValueError('k ({}) larger than window size ({})'.format(k, self.window_size))

        ones = []

        try:
            for key, bucket in sorted(self.buckets.items()):
                for bucket_element in reversed(bucket):
                    # check if we are not going beyond query size
                    if bucket_element >= (self.current_timestamp-k):
                        ones.append(key)
                    # if we are beyond, jump out of the loops by 'exception' trick
                    else:
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

    _input = []
    result = []

    firstline = True

    for i, v in enumerate(fileinput.input()):
        if firstline:
            dgim = DGIM(int(v))
            firstline = False
            continue

        if v.startswith('q'):
            result.append(dgim.calculate_ones(v.split(' ')[1]))
        else:
            dgim.add_stream(v)

    for elem in result:
        print(elem)

