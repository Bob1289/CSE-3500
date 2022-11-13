import os
import sys
import marshal
import itertools
import argparse
from operator import itemgetter
from functools import partial
from collections import Counter
import heapq

try:
    import cPickle as pickle
except:
    import pickle

termchar = 17 # you can assume the byte 17 does not appear in the input file

# This takes a sequence of bytes over which you can iterate, msg, 
# and returns a tuple (enc,\ ring) in which enc is the ASCII representation of the 
# Huffman-encoded message (e.g. "1001011") and ring is your ``decoder ring'' needed 
# to decompress that message. Implement this using the Huffman coding algorithm
class Node: # Create a node class to be used in the Huffman tree
    def __init__(self, data, freq): 
        self.data = data 
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq

    def __gt__(self, other):
        return self.freq > other.freq

def encode(msg):        
    # create a dictionary of characters and their frequencies
    freq = Counter(msg)
    # create a list of tuples of characters and their frequencies
    freq_list = [(k, v) for k, v in freq.items()] # list of tuples
    # sort the list by frequency and if the frequencies are the same, sort by character
    freq_list = sorted(freq_list, key=lambda x: (x[1], x[0])) # sort by frequency and then by character
    # create a list of nodes
    nodes = [] # list of nodes
    for i in range(len(freq_list)): # iterate through the list of tuples
        nodes.append(Node(freq_list[i][0], freq_list[i][1])) # append a node to the list of nodes

    # create a heap of nodes
    heapq.heapify(nodes)
    # create a tree

    while len(nodes) > 1:
        # get the two nodes with the lowest frequencies
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        # create a new node with the sum of the frequencies of the two nodes
        new_node = Node(None, left.freq + right.freq)
        # set the left and right children of the new node to the two nodes with the lowest frequencies
        new_node.left = left
        new_node.right = right
        # add the new node to the heap
        heapq.heappush(nodes, new_node)


    # create a dictionary of characters and their codes by traversing the tree using depth-first search
    codes = {}
    def traverse(node, code): # traverse the tree
        if node.left is None and node.right is None: # if the node is a leaf
            codes[node.data] = code # add the character and its code to the dictionary
        else: # if the node is not a leaf
            traverse(node.left, code + '0') # traverse the left child
            traverse(node.right, code + '1') # traverse the right child

    traverse(nodes[0], '') # traverse the tree

    # flip the dictionary so that the keys are the codes and the values are the characters
    flipped_codes = {} 
    for k, v in codes.items():
        flipped_codes[v] = k
    
    # create a string of encoded message using flipped_codes
    encoded_msg = ''
    for i in range(len(msg)):
        encoded_msg += codes[msg[i]]

    return (encoded_msg, flipped_codes)   
    
# This takes a string, cmsg, which must contain only 0s and 1s, and your 
# representation of the ``decoder ring'' ring, and returns a bytearray msg which 
# is the decompressed message. 
def decode(cmsg, decoderRing):
    # Creates an array with the appropriate type so that the message can be decoded.
    byteMsg = bytearray()
    curr = '' # current code
    for i in range(len(cmsg)):
        curr += cmsg[i] # add the next bit to the current code
        if curr in decoderRing: # if the current code is in the decoder ring
            byteMsg.append(decoderRing[curr]) # add the character to the message
            curr = '' # reset the current code
    return byteMsg # return the message

# This takes a sequence of bytes over which you can iterate, msg, and returns a tuple (compressed, ring) 
# in which compressed is a bytearray (containing the Huffman-coded message in binary, 
# and ring is again the ``decoder ring'' needed to decompress the message.
def compress(msg, useBWT): 
    if useBWT: 
        msg = bwt(msg)
        msg = mtf(msg)

    # here, compressed message should be the return value from encode()
    compressedMsg, decoderRing = encode(msg)
    # Add padding to the end of the compressed message so that it is a multiple of 8 and keep track of the number of padding bits
    padding = 8 - len(compressedMsg) % 8
    compressedMsg += '0' * padding
    # Convert the compressed message to a bytearray
    compressedMsg = bytearray(int(compressedMsg[i:i+8], 2) for i in range(0, len(compressedMsg), 8))
    # Add the number of padding bits to the beginning of the bytearray
    compressedMsg.insert(0, padding)
    return (compressedMsg, decoderRing)

    

# This takes a sequence of bytes over which you can iterate containing the Huffman-coded message, and the 
# decoder ring needed to decompress it.  It returns the bytearray which is the decompressed message. 
def decompress(msg, decoderRing, useBWT):
    # Remove the number of padding bits from the beginning of the bytearray
    padding = msg[0] # number of padding bits
    msg = msg[1:] # compressed message
    # Convert the bytearray to a string of 0s and 1s
    compressedMsg = ''
    for i in range(len(msg)):
        compressedMsg += '{0:08b}'.format(msg[i])
    # Remove the padding from the end of the compressed message
    compressedMsg = compressedMsg[:-padding]
    # here, byteMsg should be the return value from decode()
    byteMsg = decode(compressedMsg, decoderRing)
    if useBWT:
        byteMsg = imtf(byteMsg)
        byteMsg = ibwt(byteMsg)
    return byteMsg



# memory efficient iBWT
# WORKS
def ibwt(msg):
    orginal = bytearray()
    # create 2 lists, one for the BWT and one for the index
    BWT_list = list(msg)
    index_list = list(range(len(msg)))
    # sort the lists
    BWT_list, index_list = zip(*sorted(zip(BWT_list, index_list)))
    # get the index of the termchar
    index = BWT_list.index(termchar)
    # get the original message
    for i in range(len(BWT_list)):
        orginal.append(BWT_list[index])
        index = index_list[index]

    return orginal[1:]

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