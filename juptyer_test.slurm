#!/bin/bash
#SBATCH --job-name="Jupyter"                # Job name
#SBATCH --mail-user=kaellis@stanford.edu  # Email address
#SBATCH --mail-type=NONE                    # Mail notification type (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --partition=normal                  # Node partition
#SBATCH --nodes=1                           # Number of nodes requested
#SBATCH --ntasks=1                          # Number of processes
#SBATCH --time=01:00:00                     # Time limit request

date
module purge
module load intel/psxe-2020
EXEC_DIR=$HOME/covid19_air_travel_threat_modeling/
hostname && jupyter-notebook --no-browser --notebook-dir=$EXEC_DIR

