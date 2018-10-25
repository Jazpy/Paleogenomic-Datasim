#!/bin/bash

g_dir="/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation"
size_freq_path="/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/size_freq"
mat_file="/cm/shared/apps/gargammel/6oct2017/src/matrices/double-"

#$ -b y
#$ -w e
#$ -e /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/err/gargammel
#$ -o /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/std/gargammel
#$ -N gargammel_ref  # job's name
#$ -hold_jid pre_gargammel_ref

#$ -t 1-100
# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -R y

module load htslib/1.2.1
module load samtools/1.2
module load seq-gen/1.3.4
module load gargammel/6oct2017

# 1x coverage with 0, 2, 5, 10% contamination
gargammel.pl -c 1 --comp 0,0,1 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/1x/0percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &
gargammel.pl -c 1 --comp 0,0.02,0.98 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/1x/2percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &
gargammel.pl -c 1 --comp 0,0.05,0.95 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/1x/5percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &
gargammel.pl -c 1 --comp 0,0.1,0.9 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/1x/10percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &

# 5x coverage with 0, 2, 5, 10% contamination
gargammel.pl -c 5 --comp 0,0,1 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/5x/0percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &
gargammel.pl -c 5 --comp 0,0.02,0.98 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/5x/2percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &
gargammel.pl -c 5 --comp 0,0.05,0.95 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/5x/5percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &
gargammel.pl -c 5 --comp 0,0.1,0.9 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/5x/10percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &

# 10x coverage with 0, 2, 5, 10% contamination
gargammel.pl -c 10 --comp 0,0,1 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/10x/0percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &
gargammel.pl -c 10 --comp 0,0.02,0.98 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/10x/2percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &
gargammel.pl -c 10 --comp 0,0.05,0.95 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/10x/5percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &
gargammel.pl -c 10 --comp 0,0.1,0.9 -f "$size_freq_path" -matfile "$mat_file" -o "$g_dir"/cases/case_$SGE_TASK_ID/10x/10percent/frags "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/ &

# Copy original haplotypes to analyze later
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/1x/0percent/
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/1x/2percent/
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/1x/5percent/
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/1x/10percent/

cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/5x/0percent/
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/5x/2percent/
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/5x/5percent/
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/5x/10percent/

cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/10x/0percent/
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/10x/2percent/
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/10x/5percent/
cp "$g_dir"/gargammel/cases/case_$SGE_TASK_ID/endo/*.fa "$g_dir"/cases/case_$SGE_TASK_ID/10x/10percent/

wait
