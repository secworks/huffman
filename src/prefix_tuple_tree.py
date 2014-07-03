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
# extract_prefix_codes()
#
# Given a prefix tree, extracts the prefix codes for all
# leaves. The prefix codes are returned as a dictionary.
#-------------------------------------------------------------------
def extract_prefix_codes(tree):
    return {}


#-------------------------------------------------------------------
# gen_prefix_tree()
#
# Given a list of tuples with frequency (weight) for a character
# the function returns the corresponding tuple based prefix tree.
#-------------------------------------------------------------------
def gen_prefix_tree(tlist):
    while (len(tlist) > 1):
        print(len(tlist))
        tlist.sort(reverse=True)
        (w1, chr1) = tlist.pop()
        (w2, chr2) = tlist.pop()
        tlist.append((w1 + w2, ((w1, chr1), (w2, chr2))))
    return tlist.pop()


#-------------------------------------------------------------------
# gen_tuple_list()
#
# Generates a list of max_types tuples. Each tuple contains a
# randomly selected frequency of a character from the set of
# characters [chr(0) .. chr((max_types - 1))]
#-------------------------------------------------------------------
def gen_tuple_list(max_types, max_nums):
    return [(random.randint(0,max_nums), chr(i)) for i in range(max_types)]


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
    my_list = gen_tuple_list(max_types, max_nums)
    my_tree = gen_prefix_tree(my_list[:])
    my_codes = extract_prefix_codes(my_tree)
    
    my_list.sort(reverse=True)
    print("The generated tuple list:")
    print(my_list)
    print("")
    
    print("The generated prefix tree:")
    print(my_tree)
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
