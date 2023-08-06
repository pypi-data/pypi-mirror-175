import shelve
import sys
from subprocess import call

'''
This file serves a dual purpose: 

(1) it provides a very simple means of generating files that can be supplied
    to Condor for the purpose of running many simulations in batch mode.

(2) it provides a simple script called by the Condor scheduler that actually
    runs the simulations.

The code in this file is agnostic as to the simulation tool used.
'''


def run_slurm_jobs(wrapper, params_list, email=None, queue=None):

  # write the files
  write_slurm_files(wrapper, params_list, email, queue)
  
  # submit all jobs to the condor scheduler
  # -----------------------------------------------

  # add a list of jobs to be executed
  for kk,pp in enumerate(params_list):
    runstring = "sbatch %s.slurm" % (pp.fname())
    print(runstring)
    call(runstring, shell=True)






# This function writes a condor jobs script, as well as a shelf file
def write_slurm_files(wrapper, params_list, email=None, queue=None):



  # write a python script to be called by Condor
  # -----------------------------------------------
  fstring = \
"""
import shelve
import sys
import pycraters.wrappers.GENERIC

# get arguments from stdin, supplied by SLURM
shelffile = sys.argv[1]
pindex = int(sys.argv[2])

# extract the wrapper and params from the shelf
f = shelve.open(shelffile)
wrapper = f['wrapper']
plist   = f['params_list']
params  = plist[pindex]
f.close()

# run the simulation
wrapper.go(params)
"""
  f = open('slurm_exec.py', "w")
  f.write(fstring)
  f.close()


  # store relevant data in shelf
  # ------------------------------------------
  f = shelve.open('slurm_plist.shelf')
  f['wrapper'] = wrapper ;
  f['params_list'] = params_list
  f.close()


  # write slurm jobfiles
  # ------------------------------------------

  # add a list of jobs to be executed
  for kk,pp in enumerate(params_list):


    f = open('%s.slurm' % (pp.fname()), "w")

    f.write("#!/bin/bash\n")
    f.write("#SBATCH -J %s           # job name\n" % (pp.fname()))
    f.write("#SBATCH -o %s.slog      # output/error file\n" % (pp.fname()))
    f.write("#SBATCH -p serial       # requested queue\n")
    f.write("#SBATCH --get-user-env  # user environment\n")

    #f.write("#SBATCH -t 1              # maximum runtime in minutes\n")
    f.write("python slurm_exec.py slurm_plist.shelf %d\n" % (kk))
    f.close()



  return

