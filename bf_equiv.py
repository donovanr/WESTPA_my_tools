#!/usr/local/bin/python

'''
This script reads in an hdf5 file from a westpa simulation and returns the 
number of brute force trajectories that would be an equivalent use of computation,
in terms of the total dynamics time simulated.

Written by Rory Donovan
'''

# deal with arguements
import argparse

parser = argparse.ArgumentParser(description='This script for extracting pcoords and weights from a WESTPA hdf5 file for a desired iteration.')
parser.add_argument('-f','--file', help='Input file name',required=True)
parser.add_argument('-i','--iters', help='number of WE iterations your simulation time is divided into',required=True)
args = parser.parse_args()

# import necessary libraries
import h5py
import numpy
import os

# read input args to variables
f = h5py.File(args.file, "r")
summary = f['/summary']

# tally the number of segs in each iter to make a total
numsegs = 0
for i in xrange(1,len(summary)):
    numsegs += summary[i][0]

rat = float(args.iters)
print numsegs/rat
