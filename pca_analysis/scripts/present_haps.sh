#!/bin/bash

#$ -b y
#$ -w e
#$ -e ./logs/present_haps_err
#$ -o ./logs/present_haps_std
#$ -N present_haps  # job's name

#$ -t 1
# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -l vf=20G
#$ -R y

module load hdf5
module load python36
module load htslib/1.2.1
module load samtools/1.6

top_dir=$(pwd)
gen=$2
cd "$top_dir""/""$1""/""$gen"
echo "Working on ""$1 $gen"
python3 "$top_dir"/py_scripts/get_present_haps.py
