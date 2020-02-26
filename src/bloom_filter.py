import math
import mmh3
from bitarray import bitarray
from random import shuffle, sample


class BloomFilter(object):

    def __init__(self, n_items, fp_prob):
        '''
        n_items : Number of items expected to be stored in bloom filter
        fp_prob : False Positive probability in decimal
        '''
        # False posible probability in decimal
        self.fp_prob = fp_prob

        # Size of bit array to use
        self.size = self.get_bit_array_size(n_items, fp_prob)

        # number of hash functions to use
        self.hash_count = self.get_number_of_hash_functions(self.size, n_items)

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

    def len(self):
        return self.size

    def add(self, item):  # add an element to the filter

        hash_values = []
        for i in range(self.hash_count):

            # create hash_value for given item.
            # i work as seed to mmh3.hash() function
            # With different seed, the hash_value created is different

            hash_value = mmh3.hash(bytes(item), i) % self.size
            hash_values.append(hash_value)

            # set the bit True in bit_array
            self.bit_array[hash_value] = True

    def isContained(self, item):  # check for element existence

        for i in range(self.hash_count):
            hash_value = mmh3.hash(bytes(item), i) % self.size
            if self.bit_array[hash_value] is False:

                # if any of bit is False then,its not present
                # in filter
                # else there is probability that it exist
                return False
        return True

    @classmethod
    def get_bit_array_size(self, n_items, prob):
        '''
        Return the size of bit array(m) to used using
        following formula
        m = -(n * lg(p)) / (lg(2)^2)
        n : int
            number of items expected to be stored in filter
        p : float
            False Positive probability in decimal
        '''
        bit_size = -(n_items * math.log(prob))/(math.log(2)**2)
        return int(bit_size)

    @classmethod
    def get_number_of_hash_functions(self, bit_size, n_items):
        '''
        Return the hash function(k) to be used using
        following formula
        k = (m/n) * lg(2)

        m : int
            size of bit array
        n : int
            number of items expected to be stored in filter
        '''
        n_hash_functions = (bit_size/n_items) * math.log(2)
        return int(n_hash_functions)


def range_query(numbers_in, numbers_not_in):
    shuffle(numbers_in)
    shuffle(numbers_not_in)
    # test_numbers = numbers_in[:int(math.floor(len(numbers_in)/2))] + numbers_not_in
    # shuffle(test_numbers)

    bloom_range = sorted(sample(numbers_in, 2))

    for number in range(bloom_range[0], bloom_range[1]+1):
        if bloomf.isContained(number):
            if number in numbers_not_in:
                print("'{}' is a false positive!".format(number))
            else:
                print("'{}' is probably present!".format(number))
        else:
            print("'{}' is definitely not present!".format(number))


if __name__ == "__main__":

    # numbers to be added
    numbers_in = list(
        map(int, input("Enter a list of number separated by a space: ").split()))
    n_items = len(numbers_in)  # no of items to add
    print("The number of items you want to add is: %s" % n_items)
    # false positive probability
    prob = float(input("Enter the false positive probability you wouold like (eg: 0.05): "))

    bloomf = BloomFilter(n_items, prob)
    # prints the parameters
    print("With %s items and the False Positive Probability of %s the following parameters have been derived: " % (
        n_items, bloomf.fp_prob))
    print("Size of bit array: {}".format(bloomf.size))
    print("Number of hash functions: {}".format(bloomf.hash_count))

    # numbers not added for testing
    print("For testing purpose, please give me some numbers (different from the others) that will not be added in the filter!")
    numbers_not_in = list(
        map(int, input("Enter a list of number separated by a space: ").split()))

    for item in numbers_in:
        bloomf.add(item)

    range_query(numbers_in, numbers_not_in)
