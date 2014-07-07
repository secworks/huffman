#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#=======================================================================
#
# prefix_tuple_tree.py
# --------------------
# An attempt at building a prefix tree using tuples in Python.
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
VERBOSE = True


#-------------------------------------------------------------------
# class Node
#
# Our basic node class (struct) used to create the tree.
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
        return [(ptree.char, prefix)]


#-------------------------------------------------------------------
# extract_prefix_codes()
#
# Given a prefix tree, extracts the prefix codes for all
# leaves. The prefix codes are returned as a dictionary.
#-------------------------------------------------------------------
def extract_prefix_codes(ptree):
    left_list = get_node_codes(prefix + '1', ptree.lchild)
    right_list = get_node_codes(prefix + '0', ptree.rchild)


#-------------------------------------------------------------------
# gen_prefix_tree()
#
# Given a list of tuples with frequency (weight) for a character
# the function returns the corresponding tuple based prefix tree.
#-------------------------------------------------------------------
def gen_prefix_tree(nlist):
    while (len(nlist) > 1):
        print("Length of prefix list: %d" % len(nlist))
        nlist = sort_node_list(nlist)
        node1 = nlist.pop()
        node2 = nlist.pop()
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
    print("Length of given list: %d" % len(nlist))
    for i in range(len(nlist)):
        node = nlist.pop()
        nodes += 1
        if len(new_list) == 0:
            new_list.append(node)
        else:
            i = 0
            while ((i < len(new_list) and (node.weight < new_list[i].weight))):
                i += 1
            new_list = new_list[:i] + [node] + new_list[i:]
    print(len(new_list))
    return new_list


#-------------------------------------------------------------------
# gen_node_list()
#
# Generates a list of max_types numbder of nodes. Each tuple
# contains a randomly selected frequency of a character from the
# set of characters [chr(0) .. chr((max_types - 1))]
#-------------------------------------------------------------------
def gen_node_list(max_types, max_nums):
    my_list = []
    for i  in range(max_types):
        my_node = Node(chr(i), random.randint(0,max_nums))
        my_list.append(my_node)
    return my_list


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
    
    max_types = 199
    max_nums  = 10000
    my_list = gen_node_list(max_types, max_nums)
#    print("List before sort:")
#    for element in my_list:
#        element.print_fields()
#    print("")

    my_list = sort_node_list(my_list)
    print("Length of sorted list: %d" % len(my_list))
    print("List after sort:")
    for element in my_list:
        element.print_fields()
    print("")

    my_tree = gen_prefix_tree(my_list)
    my_codes = extract_prefix_codes(my_tree)
    
    print("The generated node list:")
    for element in my_list:
        element.print_fields()
    print("")
    
    print("The generated prefix tree:")
    my_tree.print_fields()
    print("")
    print("The corresponding prefix codes:")
    print(my_codes)
    print("")


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
