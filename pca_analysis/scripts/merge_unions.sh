#!/bin/bash

#$ -b y
#$ -w e
#$ -e ./logs/merge_err
#$ -o ./logs/merge_std

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
module load finestructure
module load chromopainter

gen=$2
cov=$3
per=$4
num_anc=$5
offset=$6
clean=$7
suffix="$gen"_"$cov"_"$per"

top_dir=$(pwd)
pha_dir="$top_dir"/"$1"
fs_dir="$top_dir"/chromo_"$1"
ref_dir="$top_dir"/"$1"/"$gen"/reference

python3 "$top_dir"/py_scripts/merge_union_haps.py $ref_dir $fs_dir $gen $cov $per $num_anc $offset

# Test if empty haps
if ! [ -s "$fs_dir"/merged/PREANC_"$suffix".haps ];then
  exit
fi

# Create idfile
tail --line=+3 "$fs_dir"/merged/PREANC_"$suffix".sample | awk '{ print $1 }' > "$fs_dir"/chromo/chromo_"$suffix".id
python3 "$top_dir"/py_scripts/make_pop.py "$fs_dir"/chromo/chromo_"$suffix".id "$fs_dir"/chromo/chromo_"$suffix".pop
inds=$(wc -l < "$fs_dir"/chromo/chromo_"$suffix".id)

impute2chromopainter2.pl -r $inds "$fs_dir"/merged/PREANC_"$suffix".haps "$fs_dir"/chromo/chromo_"$suffix"
python3 "$top_dir"/py_scripts/make_chromo_haps.py "$fs_dir"/chromo/chromo_"$suffix".haps

perl "$top_dir"/scripts/makeuniformrecfile.pl "$fs_dir"/chromo/chromo_"$suffix".haps "$fs_dir"/chromo/chromo_"$suffix".recombfile
