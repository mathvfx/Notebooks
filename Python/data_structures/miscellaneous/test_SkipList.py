#!env python3
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 

from random import sample, seed, choice
from SkipList import SkipList

def test():
    #seed(421)  # check case
    #seed(3421) # check case
    #seed(2441) # check case
    #seed(241)  # check case
    L = sample(range(10, 99), 17)
    chosen = choice(L)
    print(f" >> BUILD_LIST: {L}")
    SL = SkipList(L)
    print(SL)
    print(f" >> Search Path for item {chosen}: {SL.path_to_target(chosen)}")
    print("\n\n")

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    seed(12344)
    L2 = sample(letters, 13)
    print(f" >> BUILD_LIST: {L2}")
    SL2 = SkipList(L2)
    print(SL2)
    print(f" >> Search Path for item 'q': {SL2.path_to_target('q')}")
    print(f" >> SL2.pop() = {SL2.pop()}")
    print(f" >> SL2.pop('K') = {SL2.pop('K')}")
    print(f" >> .... now pushing 'j'... ")
    SL2.push("j")
    print(f" >> .... now iddd '33' and add '102'... ")
    SL2 += "33"
    SL2 = SL2 + '102'
    print("\n\n")
    print(SL2)
    print(f"SL2.find_range('H', 'c') = {SL2.find_range('H', 'c')}")
    print(f"SL2.find_range('I', 'c') = {SL2.find_range('I', 'c')}")
    print(f"SL2.find_range('I', 'T') = {SL2.find_range('I', 'T')}")
    print(f"SL2.find_range('I', 'K') = {SL2.find_range('I', 'K')}")
    print(f"SL2.find_range('102', 'q') = {SL2.find_range('102', 'q')}")
    print(f" >> Is 'Z' in Skip List? {'Z' in SL2}")
    print(f" >> Is 'O' in Skip List? {'O' in SL2}")


if __name__ == "__main__":
    test()
