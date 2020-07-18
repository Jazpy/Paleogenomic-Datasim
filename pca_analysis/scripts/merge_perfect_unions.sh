#!/bin/bash

#$ -b y
#$ -w e
#$ -e ./logs/merge_perf_err
#$ -o ./logs/merge_perf_std

#$ -t 1
# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -l vf=15G
#$ -R y

module load hdf5
module load python36
module load finestructure
module load chromopainter

gen=$2
suffix="$gen"

top_dir=$(pwd)
fs_dir="$top_dir"/chromo_"$1"

# Test if empty haps
if ! [ -s "$fs_dir"/perfect_merged/PREANC_"$suffix".haps ];then
  exit
fi

# Create idfile
tail --line=+3 "$fs_dir"/perfect_merged/PREANC_"$suffix".sample | awk '{ print $1 }' > "$fs_dir"/perfect_chromo/chromo_"$suffix".id
python3 "$top_dir"/py_scripts/make_pop.py "$fs_dir"/perfect_chromo/chromo_"$suffix".id "$fs_dir"/perfect_chromo/chromo_"$suffix".pop
inds=$(wc -l < "$fs_dir"/perfect_chromo/chromo_"$suffix".id)

impute2chromopainter2.pl -r $inds "$fs_dir"/perfect_merged/PREANC_"$suffix".haps "$fs_dir"/perfect_chromo/chromo_"$suffix"
python3 "$top_dir"/py_scripts/make_chromo_haps.py "$fs_dir"/perfect_chromo/chromo_"$suffix".haps

perl "$top_dir"/scripts/makeuniformrecfile.pl "$fs_dir"/perfect_chromo/chromo_"$suffix".haps "$fs_dir"/perfect_chromo/chromo_"$suffix".recombfile
