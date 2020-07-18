#!/bin/bash

#$ -b y
#$ -w e

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
module load finestructure
module load chromopainter

top_dir=$(pwd)
fs_dir="$top_dir"/chromo_"$1"
suffix=$2

# Test if empty haps
if ! [ -s "$fs_dir"/perfect_chromo/chromo_"$suffix".haps ];then
        exit
fi

fs cp -a 0 0 -g "$fs_dir"/perfect_chromo/chromo_"$suffix".haps \
             -t "$fs_dir"/perfect_chromo/chromo_"$suffix".id \
             -r "$fs_dir"/perfect_chromo/chromo_"$suffix".recombfile \
             -o "$fs_dir"/perfect_work/"$suffix"

mv "$fs_dir"/perfect_work/"$suffix".chunkcounts.out "$fs_dir"/perfect_fs
rm "$fs_dir"/perfect_work/"$suffix"
