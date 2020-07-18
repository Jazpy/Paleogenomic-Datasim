#!/bin/bash

#$ -b y
#$ -w e
#$ -e ./logs/vcf_err
#$ -o ./logs/vcf_std
#$ -hold_jid present_haps

#$ -t 1
# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -l vf=60G
#$ -R y

module load hdf5
module load python36

gen=$2
cov=$3
per=$4
prefix="$gen"_"$cov"_"$per"

top_dir=$(pwd)
pha_dir="$top_dir"/"$1"
hap_dir="$top_dir"/chromo_"$1"/
ref_dir="$top_dir"/"$1"/"$gen"/reference

hap_prefix="$top_dir"/chromo_"$1"/merged/PREANC_"$prefix"
out_vcf="$top_dir"/vcfs_"$1"/"$prefix".vcf

python3 "$top_dir"/py_scripts/merge_union_haps.py $ref_dir $hap_dir $gen $cov $per 100 0
python3 "$top_dir"/py_scripts/haps_to_vcf.py $hap_prefix $out_vcf
