#!/bin/bash

# Declare bash variables
g_dir=$1
ref_dir=$g_dir/reference

#$ -b y
#$ -w e
#$ -N pre_phase_pop  # job's name
#$ -hold_jid call_variants

# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -l vf=50G
#$ -R y

module load hdf5/1.8.19
module load python36/3.6.3
module load htslib/1.2.1
module load samtools/1.2

cd $ref_dir
python3 $g_dir/py_scripts/make_modern_vcf.py $2
