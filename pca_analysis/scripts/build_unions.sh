#!/bin/bash

#$ -b y
#$ -w e
#$ -e ./logs/unions_err
#$ -o ./logs/unions_std
#$ -hold_jid present_haps

#$ -t 1
# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -l vf=5G
#$ -R y

module load hdf5
module load python36

gen=$2
cov=$3
per=$4
suffix="$gen"_"$cov"_"$per"

top_dir=$(pwd)
pha_dir="$top_dir"/"$1"
fs_dir="$top_dir"/chromo_"$1"
ref_dir="$top_dir"/"$1"/"$gen"/reference

python3 "$top_dir"/py_scripts/fill_union.py $pha_dir $gen $cov $per \
        "$top_dir"/perf_sites_"$cov".txt

for (( i = 1; i <= 100; i++ ))
do
  per_dir="$top_dir"/"$1"/"$gen"/cases/case_"$i"/"$cov"/"$per"percent/phased/
  cd $per_dir
  cp union.phased.haps "$top_dir"/chromo_"$1"/haps/"$suffix"_"$i".haps
done
