#!env python3

import random
from ADT_HashMaps import ChainHashMap

def test_ChainHashMap():
    cmaps = ChainHashMap()
    print(">> Adding give key-value pairs")
    cmaps["vehicle"] = "Honda"
    cmaps["year"] = 1990
    cmaps["state"] = "CA"
    cmaps["plane"] = "Boeing"
    cmaps["animal"] = "Cats"
    print(cmaps)
    print(f"cmaps.items():  {cmaps.items()}")
    print(f"cmaps['animal']:  {cmaps['animal']}")
    print(f"Current length:  {len(cmaps)}")
    print("\n>> Now iterate through cmaps...")
    for item in cmaps:
        print(f"ITEM: {item}")
    print()
    print(">> Changing cmaps['plane']...")
    cmaps["plane"] = "Lockheed Martin"
    print(">> Deleting cmaps['animal']...")
    del cmaps["animal"]
    print(cmaps)
    print(f"Current length:  {len(cmaps)}")
    print(f"Key 'vehicle' in cmaps? {'vehicle' in cmaps}")
    print("\n>> Debug...")
    cmaps.DEBUG_DATASET()


def test_ChainHashMap2():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstuvwxyz"
    item_len = 30
    my_keys = random.sample(letters, item_len)
    my_vals = random.sample(range(1000, 9000), item_len)
    cmaps = ChainHashMap()
    for k,v in zip(my_keys, my_vals):
        cmaps[k] = v
    print(f"Current length:  {len(cmaps)}")
    print(f"Contents:  {cmaps}")
    print("\n>> Debug...")
    cmaps.DEBUG_DATASET()


if __name__ == "__main__":
    print("\n")
    test_ChainHashMap()
    print("\n\n")
    test_ChainHashMap2()
