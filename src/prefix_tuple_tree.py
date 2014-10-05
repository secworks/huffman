#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#=======================================================================
#
# prefix_tuple_tree.py
# --------------------
# An attempt at building a prefix tree in Python.
# This implementation uses tuples for nodes.
#
#
# Author: Joachim Strömbergson
# Copyright (c) 2014, Secworks Sweden AB
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or 
# without modification, are permitted provided that the following 
# conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer. 
# 
# 2. Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in 
#    the documentation and/or other materials provided with the 
#    distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#=======================================================================

#-------------------------------------------------------------------
# Python module imports.
#-------------------------------------------------------------------
import sys
import random


#-------------------------------------------------------------------
# Constants.
#-------------------------------------------------------------------
VERBOSE = False


#-------------------------------------------------------------------
# get_node_codes()
#
# Get a list of tuples with the prefix codes for a char in a
# given node as well as for its subnodes.
#-------------------------------------------------------------------
def get_node_codes(prefix, ptree):
    (char, weight, children, left_tree, right_tree) = ptree

    if char == None:
        left_list = []
        right_list = []

        if left_tree != None:
          left_list = get_node_codes(prefix + '0', left_tree)

        if right_tree != None:
          right_list = get_node_codes(prefix + '1', right_tree)

        return left_list + right_list

    else:
        return [(char, weight, prefix)]


#-------------------------------------------------------------------
# extract_prefix_codes()
#
# Given a prefix tree, extracts the prefix codes for all
# leaves. The prefix codes are returned as a dictionary.
#-------------------------------------------------------------------
def extract_prefix_codes(ptree):
    (char, weight, children, left_tree, right_tree) = ptree

    left_list = get_node_codes('0', left_tree)
    right_list = get_node_codes('1', right_tree)

    prefix_dict = {}

    for (char, weight, prefix) in left_list:
        prefix_dict[char] = (weight, prefix)

    for (char, weight, prefix) in right_list:
        prefix_dict[char] = (weight, prefix)

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
            print("node1 weigth: %d" % node1[1])
            print("node2 weigth: %d" % node2[1])

        new_weight = node1[1] + node2[1]
        new_children = 2 + node1[2] + node2[2]
        new_node = (None, new_weight, new_children, node1, node2)
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
# main()
#
# Generates a list of different (frequency, char) tuples and feed
# the list to the prefix tree generator. The prefix codes for
# each character is then extracted. Finally the list, the tree
# and the codes are printed.
#-------------------------------------------------------------------
def main():
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
# __name__
# Python thingy which allows the file to be run standalone as
# well as parsed from within a Python interpreter.
#-------------------------------------------------------------------
if __name__=="__main__": 
    # Run the main function.
    sys.exit(main())

#=======================================================================
# EOF prefix_tuple_tree.py
#=======================================================================
