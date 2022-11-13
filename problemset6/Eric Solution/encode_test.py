import os
import sys
import marshal
import itertools
import argparse
from operator import itemgetter
from functools import partial
# from collections import Counter
import heapq

try:
    import cPickle as pickle
except:
    import pickle

termchar = 17

def encode(msg):        
    freq = {}
    for c in msg:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    # Create a heap of tuples (freq, char)
    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)

    # Create a Huffman tree
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Create a dictionary of Huffman codes
    huff = {}
    for pair in heapq.heappop(heap)[1:]:
        huff[pair[0]] = pair[1]

    # Encode the message
    encoded = ""
    for c in msg:
        encoded += huff[c]

    return encoded, huff

def decode(cmsg, decoderRing):
    # flip the decoder ring
    decoderRing = {v: k for k, v in decoderRing.items()}
    # Decode the message
    byteMsg = bytearray()
    curr = ''
    for i in range(len(cmsg)):
        curr += cmsg[i]
        if curr in decoderRing:
            byteMsg.append(decoderRing[curr])
            curr = ''

    return byteMsg


arr = 'BANNANA'.encode()
msg, ring = encode(arr)
print(msg,ring)
print(decode(msg, ring))