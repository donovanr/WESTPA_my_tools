#!/usr/local/bin/python

'''
This script reads in an hdf5 file from a westpa simulation and produces a 
text file with three columns: [iteration, pcood, weight].

Written by Rory Donovan
'''

# deal with arguements
import argparse

parser = argparse.ArgumentParser(description='This script for extracting pcoords and weights from a WESTPA hdf5 file for a desired iteration.')
parser.add_argument('-f','--file', help='Input file name',required=True)
args = parser.parse_args()

# import necessary libraries
import h5py
import numpy
import os


# read input args to variables
f = h5py.File(args.file, "r")
basename = os.path.splitext(args.file)[0]
summary = f['/summary']
tot_iters = len(summary) - 1 # 0 indexing

print 'total number of iterations in h5 file = ' + str(tot_iters)

alliterinfo = numpy.zeros((1,3)) # placeholder first line - delete after all appends

for iternum in xrange(1,tot_iters+1): 
	
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
	
        # make a list of the iter number
        iter_nums = iternum*numpy.ones(len(weights))

	# put pcoords and weights into one two-column array
	iterinfo = numpy.column_stack((iter_nums,final_pcoord,weights))
	
	alliterinfo = numpy.append(alliterinfo, iterinfo, axis = 0)
	
	print 'finished iteration' + str(iternum)
	
# delete placeholder first line
alliterinfo = numpy.delete(alliterinfo, (0) ,axis=0)

#print out to file
fname = basename + '_all_iters_pcoords_and_weights.txt'
numpy.savetxt(fname, alliterinfo, header = '             iteration                   pcoords                  weights')
