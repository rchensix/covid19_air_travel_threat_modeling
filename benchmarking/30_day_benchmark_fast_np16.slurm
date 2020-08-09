#!/bin/bash
#SBATCH --job-name="30_day_benchmark_fast_np16"               # Job name
#SBATCH --mail-user=rchensix@stanford.edu # Email address 
#SBATCH --mail-type=NONE                    # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH -N 1                           # Number of nodes requested
#SBATCH -n 16                         # Number of processors
#SBATCH --time=10:00:00                     # Time limit request
#SBATCH -o 30_day_benchmark_fast_np16.out

date
module purge
module load intel/psxe-2020
cd ~/covid19_air_travel_threat_modeling
pyinstrument main.py --sim_param_file benchmarking/30_day_benchmark_fast_np16.json
date
