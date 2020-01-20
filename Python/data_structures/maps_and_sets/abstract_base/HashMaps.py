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


from abc import abstractmethod
from random import randrange

from Maps import MapBase


# Note that much of the implementations here have been following Goodrich et al
# as my basis and learning. The much more interesting aspect of this particular
# topic has been regarding hash function and its behavior. 
#
# Compared to ListMaps ADT, the key concept here is that we attempt to exploit 
# the speed of random access of List/array as our underlying storage system 
# by hashing any objects into suitable array/List indices.


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
        self._n += 1

    def __delitem__(self, key):
        # Override MapBase (MutableMapping) ABC
        '''Delete Item by 'key'. Raise KeyError if 'key' is not exist.'''
        idx = self._hash_map(key)
        self._bucket_delitem(idx, key)
        self._n -= 1
    
    @abstractmethod
    def __iter__(self): 
        # From MapBase (MutableMapping) ABC
        ...

    def __len__(self):
        # Override MapBase (MutableMapping) ABC
        return self._n

    @abstractmethod
    def _bucket_getitem(self, hash_idx, key):
        ...

    @abstractmethod
    def _bucket_setitem(self, hash_idx, key, value):
        ...

    @abstractmethod
    def _bucket_delitem(self, hash_idx, key):
        ...
