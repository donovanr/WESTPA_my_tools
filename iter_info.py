#!/usr/local/bin/python

'''
This script reads in an hdf5 file from a westpa simulation and produces a 
histogram of bin weights for a specified iteration.

Written by Rory Donovan
'''

# deal with arguements
import argparse

parser = argparse.ArgumentParser(description='This script for extracting pcoords and weights from a WESTPA hdf5 file for a desired iteration.')
parser.add_argument('-i','--iter', help='iteration number',required=True)
parser.add_argument('-f','--file', help='Input file name',required=True)
args = parser.parse_args()

# import necessary libraries
import h5py
import numpy
import os


# read input args to variables
f = h5py.File(args.file, "r")
basename = os.path.splitext(args.file)[0]
iternum = int(args.iter)

# construct paths to iter info in the h5 file
segindex_path = '/iterations/iter_' + '{0:08d}'.format(iternum) + '/seg_index'
pcoord_path = '/iterations/iter_' + '{0:08d}'.format(iternum) + '/pcoord'

# get the vector of final pcoords
final_pcoord = f[pcoord_path][:,-1]
final_pcoord = numpy.array(final_pcoord,dtype='float32')
final_pcoord = numpy.squeeze(numpy.asarray(final_pcoord))

# get the weights
segindex = f[segindex_path]
weights = tuple(x[0] for x in segindex)
weights = numpy.array(weights,dtype='float32')

# make sure they have the same length
assert len(weights) == len(final_pcoord), "length mismatch"

# put pcoords and weights into one two-column array
iterinfo = numpy.column_stack((final_pcoord,weights))

# print out to file
fname = basename + '_iter_' + str(iternum).zfill(4) + '_pcoords_and_weights.txt'
numpy.savetxt(fname, iterinfo, header='               pcoords                  weights')
