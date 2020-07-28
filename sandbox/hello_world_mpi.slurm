#!/bin/bash
#SBATCH --job-name="hello_world_mpi"               # Job name
#SBATCH --mail-user=rchensix@stanford.edu # Email address 
#SBATCH --mail-type=NONE                    # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --nodes=3                           # Number of nodes requested
#SBATCH --ntasks=3                         # Number of processes
#SBATCH --time=00:20:00                     # Time limit request

date
module purge
module load intel/psxe-2020

mpiexec -n 16 python3 ~/covid19_air_travel_threat_modeling/sandbox/hello_world_mpi.py
date
