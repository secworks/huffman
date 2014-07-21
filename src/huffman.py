#!/usr/bin/env python
# -*- coding: utf-8 -*-
#=======================================================================
# huffman.py
# ---------
# Test implementation of huffman encoder and decoder. Just to see
# that I actually understand it. Also good practice to learn to write
# bit patterns from Python.
#
#
# (c) 2012 Secworks
# JoachimS
#=======================================================================

#-------------------------------------------------------------------
# Imports.
#-------------------------------------------------------------------
import argparse
import random
import sys


#-------------------------------------------------------------------
# Constants.
#-------------------------------------------------------------------
VERBOSE = False
DEBUG = True

VERSION = '0.1 Beta'


#-------------------------------------------------------------------
# class Node
#
# A basic node class (struct) used to create the prefix tree.
#-------------------------------------------------------------------
class Node:
    def __init__(self, char, weight):
        self.char = char
        self.weight = weight
        self.lchild = None
        self.rchild = None
        self.children = 0

    def print_fields(self):
        if self.char != None:
            print("Char: %c, weight = %d" % (self.char, self.weight))
        else:
            print("Inner node with %d children and total weight %d" %\
                  (self.children, self.weight))

        if self.lchild != None:
            print("Left child contains subtree")
        else:
            print("Left child contains no subtree")

        if self.rchild != None:
            print("Right child contains subtree")
        else:
            print("Right child contains no subtree")



#-------------------------------------------------------------------
# get_node_codes()
#
# Get a list of tuples with the prefix codes for a char in a
# given node as well as for its subnodes.
#-------------------------------------------------------------------
def get_node_codes(prefix, ptree):
    if ptree.char == None:
        left_list = []
        right_list = []
        if ptree.lchild != None:
          left_list = get_node_codes(prefix + '1', ptree.lchild)
        if ptree.rchild != None:
          right_list = get_node_codes(prefix + '0', ptree.rchild)
        return left_list + right_list
    else:
        return [(ptree.char, prefix, ptree.weight)]


#-------------------------------------------------------------------
# extract_prefix_codes()
#
# Given a prefix tree, extracts the prefix codes for all
# leaves. The prefix codes are returned as a dictionary.
#-------------------------------------------------------------------
def extract_prefix_codes(ptree):
    left_list = get_node_codes('1', ptree.lchild)
    right_list = get_node_codes('0', ptree.rchild)
    prefix_dict = {}

    for (char, prefix, weight) in left_list:
        prefix_dict[char] = (prefix, weight)

    for (char, prefix, weight) in right_list:
        prefix_dict[char] = (prefix, weight)

    return prefix_dict


#-------------------------------------------------------------------
# gen_prefix_tree()
#
# Given a list of tuples with frequency (weight) for a character
# the function returns the corresponding tuple based prefix tree.
#-------------------------------------------------------------------
def gen_prefix_tree(nlist):
    while (len(nlist) > 1):
        if VERBOSE:
            print("Length of prefix list: %d" % len(nlist))

        nlist = sort_node_list(nlist)
        node1 = nlist.pop()
        node2 = nlist.pop()

        if VERBOSE:
            print("node1 weigth: %d" % node1.weight)
            print("node2 weigth: %d" % node2.weight)

        new_node = Node(None, (node1.weight + node2.weight))
        new_node.lchild = node1
        new_node.rchild = node2
        new_node.children = 2 + node1.children + node2.children
        nlist.append(new_node)

    return nlist.pop()


#-------------------------------------------------------------------
# sort_node_list()
#
# Given a list of nodes returns a list with the nodes
# sorted by weight in decreasing order.
#-------------------------------------------------------------------
def sort_node_list(nlist):
    nodes = 0
    new_list = []
    if VERBOSE:
        print("Length of given list: %d" % len(nlist))
    for i in range(len(nlist)):
        node = nlist.pop()
        nodes += 1
        if len(new_list) == 0:
            new_list.append(node)
        else:
            i = 0
            while ((i < len(new_list) and (node[1] < new_list[i][1]))):
                i += 1
            new_list = new_list[:i] + [node] + new_list[i:]

    return new_list


#-------------------------------------------------------------------
# print_prefix_codes()
#
# Given a db with prefix codes for a set of keys (chars) will
# print the contents of the db as well as some interesting
# statistics.
#-------------------------------------------------------------------
def print_prefix_codes(prefix_codes):
    min_len = 100000000
    max_len = 0
    num_raw_bits = 0
    num_prefix_bits = 0

    if VERBOSE:
        print("The generated prefix codes:")
    for key in prefix_codes:
        char = key
        (weight, prefix) = prefix_codes[key]
        num_prefix_bits += len(prefix) * weight
        num_raw_bits +=  weight * 8
        if VERBOSE:
            print("Char: %03d, prefix: %015s, prefix length: %02d, weight %010d" %\
                  (char, prefix, len(prefix), weight))

        if len(prefix) < min_len:
            min_len = len(prefix)
            min_char = char
            min_prefix = prefix
            min_weight = weight

        if len(prefix) > max_len:
            max_len = len(prefix)
            max_char = char
            max_prefix = prefix
            max_weight = weight

    reduction = int((1 - (num_prefix_bits / num_raw_bits)) * 100)

    print("")
    print("Minimum prefix length %02d for char %03d and prefix %015s with weight %010d" %\
          (min_len, min_char, min_prefix, min_weight))
    print("Maximum prefix length %02d for char %03d and prefix %015s with weight %010d" %\
          (max_len, max_char, max_prefix, max_weight))

    print("")
    print("Total number of bits in raw data:             %016d" % num_raw_bits)
    print("Total number of bits to prefix code all data: %016d" % num_prefix_bits)
    print("Reduction:                                    %02d percent" % reduction)
    print("")


#-------------------------------------------------------------------
# huffman_encode()
#
# Huffman encode a file with a given filename.
# Note: We assume that the file contains bytes.
#-------------------------------------------------------------------
def huffman_encode(filename):
    '''Encode the contents of the file using Huffman coding.'''

    # 1. First pass. Scan the file and build byte
    # frequency statistics.
    byte_freq = [0] * 256
    with open(filename, 'rb') as my_file:
        byte = my_file.read(1)
        bytectr = 1
        while byte:
            byteval = ord(byte)
            byte_freq[byteval] = byte_freq[byteval] + 1
            byte = my_file.read(1)
            bytectr = bytectr + 1
            
    if DEBUG:
        print "Encode step one."
        print "Number of bytes read: %d" % bytectr
        print byte_freq
        print ""


    # 2. Build weighted binary tree for all bytes in the file.
    alphabet = []
    for i in range(256):
        if (byte_freq[i] > 0):
            alphabet.append([i, byte_freq[i], 0, 0, 0])

    if DEBUG:
        print "Number of symbols in the alphabet: %d" % len(alphabet)
        print "The collected alphabet with weighs:"
        print alphabet

    elements_left = len(alphabet)
    while elements_left:
        pass
        # Find the two elements with the least weight

    # 3. Create symbol table based on the tree

    # 4. Emit symbol table as header for file.
    
    # 5. Second pass. Read file and emit symbols.

    # 6. Done!
    return 0

    
#-------------------------------------------------------------------
# huffman_decode()
#
# Huffman decode a file with the given filename.
#-------------------------------------------------------------------
def huffman_decode(filename):
    pass


#-------------------------------------------------------------------
# gen_node_list()
#
# Generates a list of max_types numbder of nodes. Each tuple
# contains a randomly selected frequency of a character from the
# set of characters [chr(0) .. chr((max_types - 1))]
#
# The nodes are tuples with the contents:
# (char, weight, left subtree, right subtree)
#
# For leaf nodes the subtrees are None. For all other nodes
# the char is None."
#-------------------------------------------------------------------
def gen_node_list(max_types, max_nums):
    return [(i, random.randint(0,max_nums), 0, None, None) for i in range(max_types)]


#-------------------------------------------------------------------
# encdec_huffman()
#
# Perform huffman encoding or decoding for the given infile
# as given by the arguments.
#-------------------------------------------------------------------
def encdec_huffman(args):
    pass


#-------------------------------------------------------------------
# test_huffman()
#
# Test mode. Generates data, builds prefix tree, performs
# encoding and then decoding and presents the results.
#-------------------------------------------------------------------
def test_huffman():
    print("Generating a tuple based prefix tree")
    print("====================================")
    print

    max_types = 256
    max_nums  = int(1E8)

    print("Generating %d nodes with up to %d instances." %\
          (max_types, max_nums))
    my_list = gen_node_list(max_types, max_nums)

    if VERBOSE:
        print("List of nodes before sort:")

    my_list = sort_node_list(my_list)

    if VERBOSE:
        print("List of nodes after sort:")
        print(my_list)
        print("")

    print("Generating prefix tree and extracting db for prefix codes.")
    my_tree = gen_prefix_tree(my_list)
    if VERBOSE:
        print("The generated prefix tree:")
        print(my_tree)

    my_codes = extract_prefix_codes(my_tree)
    if VERBOSE:
        print("The generated code db:")
        print(my_codes)

    print_prefix_codes(my_codes)


#-------------------------------------------------------------------
# main()
#
# Create an argument parser as needed to get input and output
# filenames as well as commands and options. Perform huffman
# encoding or decoding based on the given arguments.
#-------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--infile',
                        help='The input file to be encoded or decoded.')

    parser.add_argument('-o', '--outfile',
                        help='The outputfile the processed file data will be saved to.')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose processing.')

    parser.add_argument('-t', '--test', action='store_true',
                        help='Perform test processing.')

    parser.add_argument('-d', '--decode', action='store_true',
                        help='Perform Huffman decoding.')

    parser.add_argument('-e', '--encode', action='store_true',
                        help='Perform Huffman encoding.')

    parser.add_argument('--version', action='version', version=VERSION)

    args = parser.parse_args()

    if args.infile==None and not args.test:
        print "Error: No input file given and not in test mode."
        exit(1)

    if args.test:
        test_huffman()
    else:
        huffman_encdec(args)


#-------------------------------------------------------------------
# __name__
# Python thingy which allows the file to be run standalone as
# well as parsed from within a Python interpreter.
#-------------------------------------------------------------------
if __name__=="__main__": 
    # Run the main function.
    sys.exit(main())


#=======================================================================
# EOF huffman.py
#=======================================================================
