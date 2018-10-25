#!/bin/bash

#$ -b y
#$ -w e
#$ -e /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/err/pre_gargammel
#$ -o /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/std/pre_gargammel
#$ -N pre_gargammel_ref  # job's name

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
module load seq-gen/1.3.4

python3 /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/py_scripts/gen_genomes.py $1 $2 $3 $4 $5
python3 /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/py_scripts/segregating_sites.py
python3 /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/py_scripts/merge_reference.py
python3 /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/py_scripts/gen_cases.py
python3 /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/py_scripts/create_panel.py
