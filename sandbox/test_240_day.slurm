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
for i in {30..99}
do
  python -m main_serial --mode fast --num_procs 16 --num_days 240 --seed $i --log_path sandbox/days240_seed$i.txt
done
date
