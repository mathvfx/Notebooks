#!env python3


from random import randrange
from ADT_UnsortedListMaps import UnsortedMap


def test_maps():
    my_map = UnsortedMap()
    my_map["greet"] = "Hello world"
    my_map["age"] = 243
    my_map["place"] = "SF"
    my_map["country"] = "United States"
    my_map["animal"] = "eagle"
    print(f"LEN: {len(my_map)}")
    for item in my_map:
        print(f"{item} : {my_map[item]}")
    print(my_map.pop('place'))
    del my_map["animal"]
    print(f"LEN: {len(my_map)}")
    print(my_map)

    

if __name__ == "__main__":
    test_maps()
