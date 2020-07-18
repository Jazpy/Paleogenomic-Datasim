#!/bin/bash

#$ -b y
#$ -w e
#$ -e ./logs/ex_perf_haps_err
#$ -o ./logs/ex_perf_haps_std
#$ -N extract_perfect_haps  # job's name
#$ -hold_jid perfect_haps

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

top_dir=$(pwd)
gen=$2

hap_dir="$top_dir""/"$1"/""$gen""/cases/case_""$SGE_TASK_ID""/"
cd "$hap_dir"
cp perfect.haps "$top_dir""/chromo_""$1""/perfect_haps/""$gen""_""$SGE_TASK_ID"".haps"
