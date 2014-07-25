#!/usr/local/bin/python

'''
This script reads in an hdf5 file output from the w_fluxanl tool in WESTPA and
outputs a list of the fluxes to stdout.

Written by Rory Donovan
'''

# deal with arguements
import argparse

parser = argparse.ArgumentParser(description='This script for checking on the flux of a WESTPA simulation. As input, it needs the output of w_fluxanal.')
parser.add_argument('-f','--file', help='Input file name',required=True)
args = parser.parse_args()

# import necessary libraries
import h5py
import numpy
import os

# read input args to variables
f = h5py.File(args.file, "r")
flux = f['/target_flux/target_0/flux']

for i in range(len(flux)):
    print i, flux[i]
