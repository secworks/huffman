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
import sys




#-------------------------------------------------------------------
# Constants.
#-------------------------------------------------------------------
VERBOSE = False
DEBUG = True


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
#
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
        # Find the two elements with the least weight

    # 3. Create symbol table based on the tree

    # 4. Emit symbol table as header for file.
    
    # 5. Second pass. Read file and emit symbols.

    # 6. Done!

    
#-------------------------------------------------------------------
#-------------------------------------------------------------------
def huffman_decode(filename):
    '''Decode huffman decoded file.'''


#-------------------------------------------------------------------
#-------------------------------------------------------------------
def main():
    # Create an argument parser with a file name reader.
    parser = argparse.ArgumentParser()
    parser.add_argument ('-f', '--file', action='store')
    filename = parser.parse_args().file

    # Call the decryption with the given filename.
    huffman_encode(filename)


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
