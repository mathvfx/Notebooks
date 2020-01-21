#!env python3
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
# 1. Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley
# 2  Wikipedia contributors. "Associative array." Wikipedia, The Free Encyclopedia. 
#      Wikipedia, The Free Encyclopedia, 12 Jan. 2020. Web. 20 Jan. 2020.
# 3. Wikipedia contributors. "Salt (cryptography)." Wikipedia, The Free Encyclopedia. 
#      Wikipedia, The Free Encyclopedia, 8 Jan. 2020. Web. 20 Jan. 2020.
#
#
# Note that much of the implementations here have been following Goodrich et al
# as my basis and learning. The much more interesting aspect of this particular
# topic has been regarding hash function and its behavior. 
#
# Compared to ListMaps ADT, the key concept here is that we attempt to exploit 
# the speed of random access of List/array as our underlying storage system 
# by hashing any objects into suitable array/List indices.


from abc import abstractmethod
from random import randrange

from .Maps import MapBase


class HashMapBase(MapBase):
    '''An abstract base Hash Map using Python's List as underlying storage.'''
    def __init__(self, capacity=13, prime=354158293127159):
        self._data = [None]*capacity
        self._prime = prime
        self._n = 0
        self._scale_factor = randrange(1, prime-1)  # uniform random
        self._shift_factor = randrange(prime-1)     # uniform random

    def _hash_map(self, obj):
        '''Hash Map utilizes Python's default hash() to generate hash code for
        any given objects. Hash code here is an affine function with simple
        salt applied.

        Hash code of an object itself may be unique for any given Python 
        session, but compression of hash code into an optimally sized array may 
        not be unique and will thus cause hash collision. Given the requirement
        of speed rather than cryptographic security, such hash collision may be 
        unavoidable simply due to fundamental fact of how integer modulo n works
        in mathematics^. Therefore, a seperate collision resolution is needed
        to determine a suitable methods for handling hash collision. 

        Having prime numbers from affine function is by no mean guarantee
        collision-free hashing, but combining with uniform random distribution,
        it supposedly reduces the amount of clustered collision, statistically. 
        
        ^ Interested reader may want to study up on elementary number theory, or
        Group and Ring Theory to learn more interesting behaviors of integral
        number, prime numbers, and their structures.
        '''
        affine = hash(obj)*self._scale_factor + self._shift_factor
        return (affine % self._prime) % len(self._data)

    def __getitem__(self, key):
        # Override MapBase (MutableMapping) ABC
        '''Get item by 'key'. Raise KeyError if 'key' is not exist.'''
        idx = self._hash_map(key)
        return self._bucket_getitem(idx, key)

    def __setitem__(self, key, value):
        # Override MapBase (MutableMapping) ABC
        '''Set key-value pairs.
        Value associated with 'key' will be updated if item already exists.
        '''
        idx = self._hash_map(key)
        self._bucket_setitem(idx, key, value)
        # We wish to keep load factor at certain threshold and resize to some
        # prime number capacity in order to minimize hash collision. 
        #
        # _next_prime() is an O(n^2) operation and there may be potential issue
        # with large prime gap when n is significantly large, but for academic
        # purposes here, we'll gloss over this issue.
        #
        # 2n is an even number and will never be prime except when n = 1.
        #
        # Load factors will have statistical effects on hash collision
        # frequencies at the expense of storage. Control this accordingly.
        if self._n > len(self._data)//2:  # Load Factor of ~0.5
            self._resize(self._next_prime(2*len(self._data)-1))

    def __delitem__(self, key):
        # Override MapBase (MutableMapping) ABC
        '''Delete Item by 'key'. Raise KeyError if 'key' is not exist.'''
        idx = self._hash_map(key)
        self._bucket_delitem(idx, key)
    
    def __len__(self):
        # Override MapBase (MutableMapping) ABC
        return self._n

    def __repr__(self):
        return repr([x for x in self.items()])

    def __str__(self):
        return str({x:y for x,y in self.items()})

    @abstractmethod
    def __iter__(self): 
        # From MapBase (MutableMapping) ABC
        ...

    @abstractmethod
    def _bucket_getitem(self, hash_idx, key):
        ...

    @abstractmethod
    def _bucket_setitem(self, hash_idx, key, value):
        ...

    @abstractmethod
    def _bucket_delitem(self, hash_idx, key):
        ...

    def _resize(self, capacity):
        # We desire 'capacity' to be a prime number to minimize hash collision
        saved = list(self.items())   # items() is from Mapping ABC
        self._data = [None]*capacity
        self._n = 0
        for k,v in saved:  # restore to new storage space
            self[k] = v

    @staticmethod
    def _next_prime(n):
        '''Find the next prime integer from n. O(n^2) time operation.'''
        assert n >= 0
        def _is_prime(n):
            if n < 2:
                return False
            if n == 2:  # the only even prime
                return True
            for i in range(3, int(n**0.5)+1, 2):
                if n % i == 0:
                    return False
            return True
        while True:
            if n & 1 == 0: # n is even integer, skip.
                n += 1
                continue
            if _is_prime(n):
                return n
            n += 1

    def DEBUG_DATASET(self):
        '''Debug view of the entire allocated memory capacity. Good for
        checking behaviors of hash collision.
        '''
        print("~~~~~~~~~~~~~~~~~~~  DEBUG ENTIRE DATASET  ~~~~~~~~~~~~~~~~~~~")
        collision_count = 0
        line = 0
        for bucket in self._data:
            if bucket:
                collision_count += 1 if len(bucket) > 1 else 0
                print(f"Bucket {line} [{len(bucket)}]:  {bucket}")
            line += 1
        print(f"Total collision buckets: {collision_count}")
        print(f" Total storage capacity: {len(self._data)}")
        print(f"            Load Factor: {self._n/len(self._data)}")
        print("~~~~~~~~~~~~~~~~~  END DEBUG ENTIRE DATASET  ~~~~~~~~~~~~~~~~~")
