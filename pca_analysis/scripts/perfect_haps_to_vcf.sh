#!/bin/bash

#$ -b y
#$ -w e
#$ -e ./logs/vcf_err
#$ -o ./logs/vcf_std
#$ -hold_jid extract_perfect_haps

#$ -t 1
# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -l vf=50G
#$ -R y

module load hdf5
module load python36

vcf_dir=$2
gen=$3
num_anc=100
suffix="$gen"

top_dir=$(pwd)
pha_dir="$top_dir"/"$1"
fs_dir="$top_dir"/chromo_"$1"
ref_dir="$top_dir"/"$1"/"$gen"/reference

python3 "$top_dir"/py_scripts/merge_perfect_haps.py $ref_dir $fs_dir $gen $num_anc

# Test if empty haps
if ! [ -s "$fs_dir"/perfect_merged/PREANC_"$suffix".haps ];then
  exit
fi

python3 "$top_dir"/py_scripts/haps_to_vcf.py "$fs_dir"/perfect_merged/PREANC_"$suffix" "$top_dir"/"$vcf_dir"/"$suffix".vcf
