#!/bin/bash

#$ -b y
#$ -w e
#$ -e ./logs/perf_err
#$ -o ./logs/perf_std
#$ -N perfect_haps  # job's name
#$ -hold_jid present_haps

#$ -t 1-100
# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -l vf=2G
#$ -R y

module load hdf5
module load python36

top_dir=$(pwd)
gen=$2

case_dir="$top_dir""/"$1"/""$gen""/cases/case_""$SGE_TASK_ID""/"
cd "$case_dir"

python3 "$top_dir/py_scripts/perfect_haps.py" "$SGE_TASK_ID"
