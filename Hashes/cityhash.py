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
    kMul = 0x9ddfea08eb382d69
    a = lower64((lower64(candidate) ^ higher64(candidate)) * kMul)
    a ^= (a >> 47)
    b = lower64((higher64(candidate) ^ a) * kMul)
    b ^= (b >> 47)
    b = b * kMul
    return lower64(b)

def rotate(val, shift):
    """
    Bitwise right rotate.
    """
    return val if shift == 0 else (val >> shift) | lower64((val << (64 - shift)))

def rotateByAtleast1(val, shift):
    """
    Bitwise right rotate, same as rotate, but requires shift to be non-zero.
    """
    return (val >> shift) | lower64((val << (64 - shift)))

def shiftMix(val):
    """
    """
    return lower64(val ^ (val >> 47))

def hashLen16(u, v):
    """
    """
    uv = (v << 64) | u
    return hash128to64(uv)

def hashLen0to16(candidate):
    length = len(candidate)
    if length > 8:
        a = bytes(candidate[0:8])
        b = bytes(candidate[-8:-1] + candidate[-1])
        return hashLen16(a, rotateByAtleast1(b + length, length)) ^ b
    elif length >= 4:
        a = bytes(candidate[0:4])
        return hashLen16(length + (a << 3), bytes(candidate[-4:-1] + candidate[-1]))
    elif length > 0:
        a = bytes(candidate[0])
        b = bytes(candidate[length >> 1])
        c = bytes(candidate[length - 1])
        y = lower32(a + (b << 8))
        z = length + c * 4
        return lower64(shiftMix(lower64(y * K2 ^ z * K3)) * K2)
    else:
        "Won't reach here."

def hashLen17To32(candidate):
    a = lower64(bytes(candidate[0:8]) * K1)
    b = bytes(candidate[8:16])
    c = lower64(bytes(candidate[-8:-1] + candidate[-1]) * K2)
    d = lower64(bytes(candidate[-16:-8]) * K0)
    return int(str(hashLen16(lower64(rotate(lower64(a - b), 43) + rotate(c, 30) + d))) +
               str(lower64(a + rotate(b ^ K3, 30) - c) + len(candidate)))

def _weakHashLen32WithSeeds(w, x, y, z, a, b):
    a += w
    b = rotate(lower64(b + a + z), 21)
    c = a
    a += x
    a = lower64(a + y)
    b += rotate(a, 44)
    return lower64(a+z) << 64 | lower64(b + c)

def weakHashLen32WithSeeds(candidate, a, b):
    return _weakHashLen32WithSeeds(bytes(candidate[0:8]),
                                   bytes(candidate[8:16]),
                                   bytes(candidate[16:24])
                                   bytes(candidate[24:32]),
                                   a,
                                   b)

def hashLen33To64(candidate):
    length = len(candidate)
    z = bytes(candidate[24:32])
    a = bytes(candidate[0:8]) + (length + bytes(candidate[-16:-8])) * K0
    a = lower64(a)
    b = rotate(lower64(a + z), 52)
    c = rotate(a, 37)
    a = lower64(a + bytes(candidate[8:16]))
    c = lower64(c + rotate(a, 7))
    a = lower64(a + bytes(candidate[16:24]))
    vf = lower64(a + z)
    vs = lower64(b + rotate(a, 31) + c)
    a = bytes(candidate[16: 24]) + bytes(candidate[-32:-24])
    z = bytes(candidate[-8:-1] + candidate[-1])
    b = rotate(lower64(a + z), 52)
    c = rotate(a, 37)
    a = lower64(a + bytes(candidate[-24:-16]))
    c = lower64(c + rotate(a, 7))
    a = lower64(a + bytes(candidate[-16:-8]))
    wf = lower64(a + z)
    ws = lower64(b + rotate(a, 31) + c)
    r = shiftMix(lower64((vf + ws) * K2 + (wf + vs) + K0))
    return lower64(shiftMix(lower64(r * K0 + vs)) * K2)

