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


from abstract_base.HashMaps import HashMapBase
from ADT_UnsortedListMaps import UnsortedMap


class ChainHashMap(HashMapBase):
    '''A Hash Map with Separate Chaining method for collision resolution.'''
    def __iter__(self):
        # Override HashMapBase ABC
        for bucket in self._data:
            if bucket is not None:
                for item in bucket:
                    yield item

    def _bucket_getitem(self, hash_idx, key):
        # Override HashMapBase ABC
        bucket = self._data[hash_idx]
        if bucket is None:
            raise KeyError(f"{repr(key)} is not found.")
        return bucket[key]   # O(k) time. Utilize UnsortedMap linear search

    def _bucket_setitem(self, hash_idx, key, value):
        # Override HashMapBase ABC
        #
        # We utilize our own UnsortedMap implementation as bucket storage.
        # Keep in mind that if key already exists, associated value will be 
        # updated rather than creating a new key-value pair. Therefore, we must
        # also remember to update data size records accordingly.
        #
        # It is at this point we see why data entry in Hash Map is also called
        # "Hash Table": each array indices contain another array entry for 
        # handling hash collision, and thereby creating an overall hash table.
        if self._data[hash_idx] is None:
            self._data[hash_idx] = UnsortedMap()  # also can be LinkedList, etc
        old_size = len(self._data[hash_dx])
        self._data[hash_idx][key] = value   # O(k) time. 
        if len(self._data[hash_idx]) > old_size:
            self._n += 1

    def _bucket_delitem(self, hash_idx, key):
        # Override HashMapBase ABC
        bucket = self._data[hash_idx]
        if bucket is None:
            raise KeyError(f"{repr(key)} is not found.")
        del bucket[key]   # O(k) time. Utilize UnsortedMap linear search
        self._n -= 1


#TODO
class LinearHashMap(HashMapBase):
    '''A Hash Map with Linear Probing method for collision resolution.'''
    pass


#TODO
class ReHashMap(HashMapBase):
    '''A Hash Map with Rehash method for collision resolution.'''
    pass
