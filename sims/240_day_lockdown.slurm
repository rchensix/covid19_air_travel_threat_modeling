#!/bin/bash
#SBATCH --job-name="240_day_lockdown"               # Job name
#SBATCH --mail-user=rchensix@stanford.edu # Email address 
#SBATCH --mail-type=NONE                    # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --time=10:00:00                     # Time limit request
#SBATCH -o 240_day_lockdown.out

date
module purge
module load intel/psxe-2020
cd ~/covid19_air_travel_threat_modeling
python3 main.py --sim_param_file sims/240_day_lockdown.json
date
