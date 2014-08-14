#!/usr/local/bin/python

'''
This script reads in an hdf5 file from a westpa simulation and produces a
first passage time distribution, given a target state and an iteration.

It uses the w_trace tool provided in westpa to trace every segment remaining
in the given iteration and find when it first entered the target.

You will have to set the variable trace_path to be the path to
westpa/bin/w_trace on your system.

Written by Rory Donovan
'''

# deal with arguements
import argparse

parser = argparse.ArgumentParser(description='This script for extracting pcoords and weights from a WESTPA hdf5 file for a desired iteration.')
parser.add_argument('-i','--iter', help='iteration number',required=True)
parser.add_argument('-f','--file', help='Input file name',required=True)
parser.add_argument('-t','--target', help='comma seperated boundaries for target state: [b1,b2]',required=True)
args = parser.parse_args()

#import pdb
#pdb.set_trace()


# import necessary libraries
import h5py
import numpy
import os
import subprocess
from string import maketrans

# read input args to variables
f = h5py.File(args.file, "r")
basename = os.path.splitext(args.file)[0]
iternum = int(args.iter)
target = args.target.translate(maketrans("",""),"[]{}() \t")
target = numpy.asarray(target.split(","), dtype=numpy.float32)
target = numpy.sort(target)

# find number of segs in desired iteration
summary = f['/summary']
numsegs = summary[iternum][0]

# path to the w_trace tool
trace_path='/net/roos/home3/zuckerman/donovanr/westpa/bin/w_trace'
h5outname = basename + '_traj.h5'
trace_call_args = [trace_path, '--quiet', '-W', args.file, '-o', h5outname]

# append numseg number of args to the w_trace call, one for each seg to trace
for x in range(0, numsegs):
  seg_to_trace = str(iternum+1) + ':' + str(x) # +1 becaue end of iter = more segs than started, prob
  trace_call_args.append(seg_to_trace)

# make the call to w_run and trace all segs in the final iter
subprocess.call(trace_call_args)

# open the traj file
f_traj = h5py.File(h5outname, "r")

# look through the traj file, once for each seg
# for each seg, save out the sequence of pcoord values into a list of lists
allsegfinalweights = numpy.zeros(numsegs)
allsegtrajs = []
for n in range(0,numsegs):
  path_to_seg_traj = '/trajectories/traj_' + str(iternum+1) + '_' + str(n) + '/segments'
  traj_info = f_traj[path_to_seg_traj]
  allsegfinalweights[n] = traj_info[iternum][2] # also grab the weight in the desired iter
  segtraj = []
  for i in range(0,iternum - 1): # -1 because v last iter has all zeros in pcoord spot for some reason
    pcoord = traj_info[i][-1][0]
    segtraj.append(pcoord)
  allsegtrajs.append(segtraj)

# for each seg, find the iter at which it first reaches the target
# return infinity if it never reaches the target
fpts = []
for n in range(0,numsegs):
  fpt = next((i for i, v in enumerate(allsegtrajs[n]) if target[0] <= v <= target[1]), float('inf'))
  fpts.append(fpt)
fpts = numpy.array(fpts)

# pair up the weights and first passage times in an array
weighted_fptd = numpy.column_stack((fpts, allsegfinalweights))

# print out array to file
fname = 'fpt_weights_' + basename + '_iter_' + str(iternum) + '_targ_' + str(int(target)) +  '.txt'
numpy.savetxt(fname, weighted_fptd, header='                  fpts                  weights') 

# print out a version without the infinities
finite_weighted_fptd = weighted_fptd[~numpy.isinf(weighted_fptd).any(1)]
fname = 'fpt_weights_' + basename + '_iter_' + str(iternum) + '_targ_' + str(int(target)) +  '_finite.txt'
numpy.savetxt(fname, finite_weighted_fptd, header='                  fpts                  weights')

# remove all of the text files that w_trace generates
subprocess.Popen('rm traj_*', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
