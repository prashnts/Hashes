#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
#!encoding: UTF-8

from Hashes import cityhash
import sys

if __name__ == "__main__":
    for i in sys.argv[1:]:
        print(cityhash.hash64(i))