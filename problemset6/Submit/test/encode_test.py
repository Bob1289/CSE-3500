import os
import sys
import marshal
import itertools
import argparse
from operator import itemgetter
from functools import partial
from collections import Counter
import heapq

# Use huffman encoding to encode the message of bytes msg
# and return a tuple (enc, ring) where enc is the encoded message and
# ring is the decoder ring needed to decode the message.

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

    # Encode the message using the Huffman codes and pad the encoded message with 0's then add the length of the padding into the decoder ring
    encoded = ""
    for c in msg:
        encoded += huff[c]

    # pad the encoded message
    pad = 8 - len(encoded) % 8
    for i in range(pad):
        encoded += '0'

    # Create the decoder ring
    decoderRing = {}
    for c in huff:
        decoderRing[huff[c]] = c
    decoderRing['pad'] = pad

    return (encoded, decoderRing)
    
# This takes a string, cmsg, which must contain only 0s and 1s, and your 
# representation of the ``decoder ring'' ring, and returns a bytearray msg which 
# is the decompressed message. 

def decode(cmsg, decoderRing):
    # Remove the padding from the encoded message using the decoder ring
    pad = decoderRing['pad']
    cmsg = cmsg[:-pad]

    # Decode the message using the decoder ring
    decoded = bytearray()
    code = ""
    for c in cmsg:
        code += c
        if code in decoderRing:
            decoded.append(decoderRing[code])
            code = ""

    return decoded
    


    

arr = 'BANNANA'.encode()
msg, ring = encode(arr)
print(msg,ring)
print(decode(msg, ring))


