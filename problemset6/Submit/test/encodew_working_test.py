import os
import sys
import marshal
import itertools
import argparse
from operator import itemgetter
from functools import partial
from collections import Counter
import heapq

def get_huffman_codes(current_node, code):
    ring = {}

    # Edge case, only one char type
    if type(current_node) == int:
        ring[current_node] = "0"
        return ring

    # Ring the left subtree
    if type(current_node[0]) == int:
        ring[current_node[0]] = code + "0"
    else:
        ring.update(get_huffman_codes(current_node[0], code + "0"))

    # Ring the right subtree
    if type(current_node[1]) == int:
        ring[current_node[1]] = code + "1"
    else:
        ring.update(get_huffman_codes(current_node[1], code + "1"))
    
    return ring

class huffman_node:
    def __init__(self, freq, data):
        self.freq = freq
        self.data = data

    def __gt__(self, other):
        return self.freq > other.freq

    def __lt__(self, other):
        return self.freq < other.freq

def encode(msg):
    # Calculate the frequencies of the characters
    count_dict = dict()
    for char in msg:
        if char not in count_dict:
            count_dict[char] = 1
        else:
            count_dict[char] += 1
    
    # Build the frequency heap
    count_nodes = []
    for char in count_dict:
        heapq.heappush(count_nodes, huffman_node(count_dict[char], char))

    # Build the huffman tree using heaps.
    heapq.heapify(count_nodes)
    while len(count_nodes) > 1:
        minimum1 = heapq.heappop(count_nodes)
        minimum2 = heapq.heappop(count_nodes)
        heapq.heappush(count_nodes, huffman_node(minimum1.freq + minimum2.freq, (minimum1.data, minimum2.data)))
    
    # Build the decoder ring.
    encoder_ring = get_huffman_codes(count_nodes[0].data, "")

    # Replace the characters with binary strings.
    encoded_string = ""
    for char in msg:
        encoded_string = encoded_string + encoder_ring[char]
    # Build the decoding ring from the encoding ring
    decoder_ring = dict()
    for key in encoder_ring:
        decoder_ring[encoder_ring[key]] = key

    return encoded_string, decoder_ring

def decode(cmsg, ring):
    # Creates an array with the appropriate type so that the message can be decoded.
    byteMsg = bytearray()

    current_code = ""
    for i in range(len(cmsg)):
        current_code = current_code + cmsg[i]
        if current_code in ring:
            byteMsg.append(ring[current_code])
            current_code = ""
    
    return byteMsg

arr = 'BANANA.'.encode()
msg, ring = encode(arr)
print(msg,ring)
print(decode(msg, ring))
