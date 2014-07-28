# What these scripts do

## all_iters_pcoords_weights.py

This script reads in an hdf5 file from a westpa simulation and produces a text file with three columns: [iteration, pcood, weight].

This can be a vary large text file.

## iter_info.py

Same as all_iters_pcoords_weights.py, but only for one iteration, so only two columns.

## bf_equiv.py

This script reads in an hdf5 file from a westpa simulation and returns the number of brute force trajectories that would be an equivalent use of computation, in terms of the total dynamics time simulated.

## fptd.py

This script reads in an hdf5 file from a westpa simulation and produces a first passage time distribution, given a target state and an iteration.

## print_trajs_and_weights.py

This script reads in an hdf5 file from a westpa simulation and produces a pair of files: one with the weights of each trajectory, and one with a matrix of all the trajectories, each as a column vector.

## test title

did cloning on laptop work? 
