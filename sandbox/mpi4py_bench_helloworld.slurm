#!/bin/bash
#SBATCH --job-name="benchmark_hello_world_mpi"               # Job name
#SBATCH --mail-user=rchensix@stanford.edu # Email address 
#SBATCH --mail-type=NONE                    # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --nodes=3                           # Number of nodes requested
#SBATCH --ntasks=48                         # Number of processes
#SBATCH --time=00:20:00                     # Time limit request

date
module purge
module load intel/psxe-2020

srun -N 3 mpirun -n 48 python -m mpi4py.bench helloworld
date
