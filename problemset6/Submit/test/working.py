import os
import sys
import marshal
import itertools
import argparse
from operator import itemgetter
from functools import partial
from collections import Counter

import heapq
import math

try:
    import cPickle as pickle
except:
    import pickle

termchar = 17 # you can assume the byte 17 does not appear in the input file

# Recursive function for traversing the huffman tree.
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

# This takes a sequence of bytes over which you can iterate, msg, 
# and returns a tuple (enc,\ ring) in which enc is the ASCII representation of the 
# Huffman-encoded message (e.g. "1001011") and ring is your ``decoder ring'' needed 
# to decompress that message.
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

# This takes a string, cmsg, which must contain only 0s and 1s, and your 
# representation of the ``decoder ring'' ring, and returns a bytearray msg which 
# is the decompressed message. 
def decode(cmsg, ring):
    # Creates an array with the appropriate type so that the message can be decoded.
    byteMsg = bytearray()

    current_code = ""
    for i in range(len(cmsg) - ring["PAD"]):
        current_code = current_code + cmsg[i]
        if current_code in ring:
            byteMsg.append(ring[current_code])
            current_code = ""
    
    return byteMsg
    

# This takes a sequence of bytes over which you can iterate, msg, and returns a tuple (compressed, ring) 
# in which compressed is a bytearray (containing the Huffman-coded message in binary, 
# and ring is again the ``decoder ring'' needed to decompress the message.
def compress(msg, useBWT):
    if useBWT:
        msg = bwt(msg)
        msg = mtf(msg)

    huffman_encoded, ring = encode(msg)
    ring["PAD"] = (8-len(huffman_encoded)%8)%8

    huffman_encoded = huffman_encoded + "0" * ring["PAD"] # pad to byte boundary
    huffman_bytes = int(huffman_encoded, 2).to_bytes(len(huffman_encoded)//8, byteorder="big") # convert to bytes
    compressed = bytearray() # convert to bytearray

    for byte in huffman_bytes: # convert to bytearray
        compressed.append(byte) # append to bytearray

    return (compressed, ring)

# This takes a sequence of bytes over which you can iterate containing the Huffman-coded message, and the 
# decoder ring needed to decompress it.  It returns the bytearray which is the decompressed message. 
def decompress(msg, decoderRing, useBWT):
    msg_str = ""
    for byte in msg:
        bits = []
        for i in range(8):
            bits.append('1' if byte%2 else '0')
            byte = byte>>1
        msg_str = msg_str + "".join(bits[::-1])

    decompressedMsg = decode(msg_str, decoderRing)

    # before you return, you must invert the move-to-front and BWT if applicable
    # here, decompressed message should be the return value from decode()
    if useBWT:
        decompressedMsg = imtf(decompressedMsg)
        decompressedMsg = ibwt(decompressedMsg)

    return decompressedMsg

# memory efficient iBWT
def ibwt(msg):

    indexed_msg = sorted(zip(msg, range(len(msg))))

    # Find the term char, because it might not come first in the sorted list.
    for i in range(len(indexed_msg)):
        if indexed_msg[i][0] == termchar:
            term_index = i
            break
    
    # Step 3
    original_msg = bytearray()
    element = indexed_msg[term_index]
    while element[1] != term_index:
        original_msg.append(element[0])
        element = indexed_msg[element[1]]
    original_msg.append(element[0])

    # Remember to put the terminating string at the end.
    # By default it is at the start because it is lexographically smaller than regular characters.
    return original_msg[1:]

# Burrows-Wheeler Transform fncs
def radix_sort(values, key, step=0):
    sortedvals = []
    radix_stack = []
    radix_stack.append((values, key, step))

    while len(radix_stack) > 0:
        values, key, step = radix_stack.pop()
        if len(values) < 2:
            for value in values:
                sortedvals.append(value)
            continue

        bins = {}
        for value in values:
            bins.setdefault(key(value, step), []).append(value)

        for k in sorted(bins.keys()):
            radix_stack.append((bins[k], key, step + 1))
    return sortedvals
            
# memory efficient BWT
def bwt(msg):
    def bw_key(text, value, step):
        return text[(value + step) % len(text)]

    msg = msg + termchar.to_bytes(1, byteorder='big')

    bwtM = bytearray()

    rs = radix_sort(range(len(msg)), partial(bw_key, msg))
    for i in rs:
        bwtM.append(msg[i - 1])

    return bwtM[::-1]

# move-to-front encoding fncs
def mtf(msg):
    # Initialise the list of characters (i.e. the dictionary)
    dictionary = bytearray(range(256))
    
    # Transformation
    compressed_text = bytearray()
    rank = 0

    # read in each character
    for c in msg:
        rank = dictionary.index(c) # find the rank of the character in the dictionary
        compressed_text.append(rank) # update the encoded text
        
        # update the dictionary
        dictionary.pop(rank)
        dictionary.insert(0, c)

    #dictionary.sort() # sort dictionary
    return compressed_text # Return the encoded text as well as the dictionary

# inverse move-to-front
def imtf(compressed_msg):
    compressed_text = compressed_msg
    dictionary = bytearray(range(256))

    decompressed_img = bytearray()

    # read in each character of the encoded text
    for i in compressed_text:
        # read the rank of the character from dictionary
        decompressed_img.append(dictionary[i])
        
        # update dictionary
        e = dictionary.pop(i)
        dictionary.insert(0, e)
        
    return decompressed_img # Return original string

if __name__=='__main__':

    # argparse is an excellent library for parsing arguments to a python program
    parser = argparse.ArgumentParser(description='<Insert a cool name for your compression algorithm> compresses '
                                                 'binary and plain text files using the Burrows-Wheeler transform, '
                                                 'move-to-front coding, and Huffman coding.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', action='store_true', help='Compresses a stream of bytes (e.g. file) into a bytes.')
    group.add_argument('-d', action='store_true', help='Decompresses a compressed file back into the original input')
    group.add_argument('-v', action='store_true', help='Encodes a stream of bytes (e.g. file) into a binary string'
                                                       ' using Huffman encoding.')
    group.add_argument('-w', action='store_true', help='Decodes a Huffman encoded binary string into bytes.')
    parser.add_argument('-i', '--input', help='Input file path', required=True)
    parser.add_argument('-o', '--output', help='Output file path', required=True)
    parser.add_argument('-b', '--binary', help='Use this option if the file is binary and therefore '
                                               'do not want to use the BWT.', action='store_true')

    args = parser.parse_args()

    compressing = args.c
    decompressing = args.d
    encoding = args.v
    decoding = args.w


    infile = args.input
    outfile = args.output
    useBWT = not args.binary

    assert os.path.exists(infile)

    if compressing or encoding:
        fp = open(infile, 'rb')
        sinput = fp.read()
        fp.close()
        if compressing:
            msg, tree = compress(sinput,useBWT)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(tree), msg), fcompressed)
            fcompressed.close()
        else:
            msg, tree = encode(sinput)
            print(msg)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(tree), msg), fcompressed)
            fcompressed.close()
    else:
        fp = open(infile, 'rb')
        pck, msg = marshal.load(fp)
        tree = pickle.loads(pck)
        fp.close()
        if decompressing:
            sinput = decompress(msg, tree, useBWT)
        else:
            sinput = decode(msg, tree)
            print(sinput)
        fp = open(outfile, 'wb')
        fp.write(sinput)
        fp.close()