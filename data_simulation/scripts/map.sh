#!/bin/bash

# Declare bash variables
g_dir="/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation"
ref="/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/reference/ref.fa"

#$ -b y
#$ -w e
#$ -e /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/err/map
#$ -o /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/std/map
#$ -N map_ref  # job's name
#$ -hold_jid pre_map_ref

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
module load trimgalore/0.4.2
module load bwa/0.7.15
module load samtools/1.2

# 5x and 10x coverage with 0, 2, 5, 10% contamination
declare -a dirs=(
		"$g_dir""/cases/case_"$SGE_TASK_ID"/1x/0percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/5x/0percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/10x/0percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/1x/2percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/5x/2percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/10x/2percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/1x/5percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/5x/5percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/10x/5percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/1x/10percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/5x/10percent/"
		"$g_dir""/cases/case_"$SGE_TASK_ID"/10x/10percent/"
		)

for dir in "${dirs[@]}"
do
	cd "$dir"

	# Rename files for later use
	mv endo.1.fa chr.1.fa
	mv endo.2.fa chr.2.fa

	###################
	# Adapter removal #
	###################

	# Extract compressed reads
	gunzip frags_s1.fq.gz
	gunzip frags_s2.fq.gz

	# Trim reads
	trim_galore --paired --length 25 frags_s1.fq frags_s2.fq

	# Cleanup
	mv *val_1.fq clean_R1.fastq
	mv *val_2.fq clean_R2.fastq
	rm frags*

	###########
	# Mapping #
	###########

	# BWA assembly
	bwa mem "$ref" clean_R1.fastq clean_R2.fastq > readset.sam
	samtools view -S readset.sam -b -o readset.bam

	# Sort and remove duplicates
	samtools sort readset.bam readset_sort
	samtools rmdup -s readset_sort.bam readset_sort_nodup.bam

	# Create index
	samtools index readset_sort_nodup.bam

	# Cleanup
	rm clean_R*
	rm readset.bam readset.sam readset_sort.bam
done
