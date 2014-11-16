#!/usr/bin/python
#!encoding: UTF-8

class CityHash:
    """
    Python implementation of Google's CityHash.
    https://code.google.com/p/cityhash/
    All the logics are being reproduced as it was in original implementation.
    Additional source comments are added as and when required.
    """

    def __init__(self, arg):
        super(CityHash, self).__init__()
        self.arg = arg
        

# Some primes between 2^63 and 2^64 for various usage.
K0 = 0xc3a5c85c97cb3127 #14097894508562428199
K1 = 0xb492b66fbe98f273 #13011662864482103923
K2 = 0x9ae16a3b2f90404f #11160318154034397263
K3 = 0xc949d7c7509e6557 #14504361325974414679

def lower32(candidate):
    """
    Returns last 32 bits from candidate.
    """
    return candidate & 0xffffffff

def lower64(candidate):
    """
    Returns last 64 bits from candidate.
    """
    return candidate & 0xffffffffffffffff

def higher64(candidate):
    """
    Returns higher than 64 bits from candidate, by shifting lower end to right.
    """
    return candidate >> 64

def bytes(candidate):
    """
    Returns the hex-equivalent of byte-string.
    """
    result = 0x0

    # Reversed the candidate, and builds a list of characters returned as their corresponding Unicode code point.
    # https://docs.python.org/2/library/functions.html#ord
    characters = list(ord(character) for character in candidate[::-1])

    for character in characters:
        # Left shift 8 bits, and then add the current character. Automatically
        # assumes the ASCII input of string.
        result <<= 8
        result |= character

    return result

def hash128to64(candidate):
    """
    Hashes 128 input bits down to 64 bits of output.
    """
    pass