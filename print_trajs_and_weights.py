#!/usr/local/bin/python

'''
This script reads in an hdf5 file from a westpa simulation and produces a
pair of files: one with the weights of each trajectory, and one with a
matrix of all the trajectories, each as a column vector.

The trajectories are traced back to the begining of the simulation from the
specified iteration using w_trace, so you'll have to change trace_path to
point to where westpa/bin/w_trace lives.

Currently this script only works if called from the directory where the
h5 file lives.

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
import subprocess

# read input args to variables
f = h5py.File(args.file, "r")
basename = os.path.splitext(args.file)[0]
iternum = int(args.iter)

# find number of segs in desired iteration
summary = f['/summary']
numsegs = summary[iternum][0]

# path to the w_trace tool
trace_path='/net/roos/home3/zuckerman/donovanr/westpa/bin/w_trace'
h5outname = basename + '_iter_' + str(iternum) + '_traj.h5'

# only try to run w_trace if the traj file hasn't been constructed yet
if not os.path.isfile(h5outname):
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

# convert to numpy array and transpose
allsegtrajs = numpy.asarray(allsegtrajs)
allsegtrajs = numpy.transpose(allsegtrajs)

# print out array to file
fname = 'alltrajs_iter_' + str(iternum) + '_' +basename + '.txt'
numpy.savetxt(fname, allsegtrajs, header='             ^-iters-v                <-segs->') 

# print out weights
fname_w = 'weights_iter_' + str(iternum) + '_' + basename + '.txt'
numpy.savetxt(fname_w, allsegfinalweights, header='                weight')

# remove all of the text files that w_trace generates
subprocess.Popen('rm traj_*.txt', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
