#!/bin/bash

# Declare bash variables
g_dir=$1
ref_vcf=$g_dir/reference/modern.vcf

#$ -b y
#$ -w e
#$ -N phase_pop  # job's name
#$ -hold_jid pre_phase_pop

# run the job in the current working directory
#$ -cwd

# declares the shell that interprets the job script
#$ -S /bin/bash

# all environment variables in the qsub commands environment are to be exported to the batch job
#$ -V

# reserve all requested resources
#$ -l vf=9G
#$ -R y

module load shapeit/2r837
module load hdf5/1.8.19
module load python36/3.6.3
module load vcftools/0.1.14
module load htslib/1.2.1
module load samtools/1.2

# Extract contamination and coverage values
coverages=( "${@:3:$2}" ); shift "$(( $2 + 2 ))"
contaminations=( "${@:2:$1}" ); shift "$(( $1 + 1 ))"

# Transform into dirs
dirs=()
for cov in "${coverages[@]}"
do
  for cont in "${contaminations[@]}"
  do
    dirs+=("$g_dir""/cases/case_"$SGE_TASK_ID"/"$cov"x/"$cont"percent/")
  done
done

for dir in "${dirs[@]}"
do
  cd $dir
  mkdir phased
  mkdir phased/logs

  bgzip -d variants_biallelic.vcf.gz

  #########
  # Merge #
  #########

  python3 $g_dir/py_scripts/merge_vcf.py $ref_vcf variants_biallelic.vcf merged.vcf 1

  #########
  # Phase #
  #########

  bgzip variants_biallelic.vcf
  bgzip merged.vcf

  # Get sites to exclude because of misalignment
  shapeit -check \
    --input-vcf merged.vcf.gz \
    --output-log readset.alignments

  # Phase, ignoring sites in exclude file
  if [ -f readset.alignments.snp.strand.exclude ]; then
    shapeit --input-vcf merged.vcf.gz \
      --exclude-snp readset.alignments.snp.strand.exclude \
      --rho 0.00000002 \
      -O readset.phased
  else
    shapeit --input-vcf merged.vcf.gz \
      --rho 0.00000002 \
      -O readset.phased
  fi

  # Cleanup
  rm merged.vcf.gz
  rm readset.alignments*
  mv readset.phased* phased/
  mv shapeit* phased/logs

  # Get results
  python3 $g_dir/py_scripts/get_accuracy.py
  python3 $g_dir/py_scripts/get_switch_err.py
done
