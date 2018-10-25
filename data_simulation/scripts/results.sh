#!/bin/bash

g_dir="/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation"

#$ -b y
#$ -w e
#$ -e /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/err/results
#$ -o /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/std/results
#$ -N results_ref  # job's name
#$ -hold_jid phase_ref

#$ -t 1
# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -R y

module load hdf5/1.8.19
module load python36/3.6.3

python3 /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/py_scripts/get_results.py $1 $2 $3 $4
