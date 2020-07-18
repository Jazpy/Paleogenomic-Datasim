#rm -rf logs
#mkdir logs

vcf_dir=vcfs_perfect_$1
rm -rf $vcf_dir
mkdir $vcf_dir

rm -rf chromo_"$1"/perfect_merged/
mkdir chromo_"$1"/perfect_merged/
rm -rf chromo_"$1"/perfect_haps/
mkdir chromo_"$1"/perfect_haps/

declare -a gens=( "0gen" "25gen" "50gen" "100gen" "200gen" "400gen" )

for gen in "${gens[@]}"
do
  suffix="$gen"

  # Get the perfect haps
  qsub ./scripts/perfect_haps.sh $1 $gen

  # Extract the perfect haps
  qsub ./scripts/extract_perfect_haps.sh $1 $gen

  qsub -N perfect_haps_to_vcf_"$suffix" \
    ./scripts/perfect_haps_to_vcf.sh $1 $vcf_dir $gen
done
