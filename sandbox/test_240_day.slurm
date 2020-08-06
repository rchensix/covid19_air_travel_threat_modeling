#!/bin/bash
#SBATCH --job-name="hello_world_mpi"               # Job name
#SBATCH --mail-user=rchensix@stanford.edu # Email address 
#SBATCH --mail-type=NONE                    # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --nodes=1                           # Number of nodes requested
#SBATCH --ntasks=1                         # Number of processes
#SBATCH --time=1:00:00                     # Time limit request

date
module purge
module load intel/psxe-2020
cd ~/covid19_air_travel_threat_modeling
python3 ~/covid19_air_travel_threat_modeling/main_serial.py
date
