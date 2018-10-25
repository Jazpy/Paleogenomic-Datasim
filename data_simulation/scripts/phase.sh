#!/bin/bash

g_dir="/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation"

#$ -b y
#$ -w e
#$ -e /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/err/phase
#$ -o /mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/logs/std/phase
#$ -N phase_ref  # job's name
#$ -hold_jid call_variants_ref

#$ -t 1-100
# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -R y

module load shapeit/2r837
module load hdf5/1.8.19
module load python36/3.6.3

# Declare bash variables
ref_panel_hap="$g_dir""/reference/ref_panel.hap"
ref_panel_leg="$g_dir""/reference/ref_panel.leg"
ref_panel_sam="$g_dir""/reference/ref_panel.sam"

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
	mkdir phased
	mkdir phased/logs

	#########
	# Phase #
	#########

	# Get sites to exclude because of misalignment
	shapeit -check \
		--input-vcf variants_biallelic.vcf.gz \
		--input-ref "$ref_panel_hap" "$ref_panel_leg" "$ref_panel_sam" \
		--output-log readset.alignments

	# Phase, ignoring sites in exclude file
	if [ -f readset.alignments.snp.strand.exclude ]; then
		shapeit --input-vcf variants_biallelic.vcf.gz \
			--input-ref "$ref_panel_hap" "$ref_panel_leg" "$ref_panel_sam" \
			--exclude-snp readset.alignments.snp.strand.exclude \
			--rho 0.00000002 \
			-O readset.phased	
	else
		shapeit --input-vcf variants_biallelic.vcf.gz \
			--input-ref "$ref_panel_hap" "$ref_panel_leg" "$ref_panel_sam" \
			--rho 0.00000002 \
			-O readset.phased	
	fi


	# Cleanup
	mv readset.alignments* phased/
	mv readset.phased* phased/
	mv shapeit* phased/logs

	# Get results
	python3 "$g_dir"/py_scripts/get_accuracy.py
done
