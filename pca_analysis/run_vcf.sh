rm -rf logs
mkdir logs

vcf_dir=vcfs_$1
rm -rf $vcf_dir
mkdir $vcf_dir

declare -a gens=( "0gen" "25gen" "50gen" "100gen" "200gen" "400gen" )
declare -a covs=( "10x" "5x" )
declare -a pers=( "0" "2" "5" "10" )

for gen in "${gens[@]}"
do
  for cov in "${covs[@]}"
  do
    for per in "${pers[@]}"
    do
      suffix="$gen"_"$cov"_"$per"
      qsub -N merge_vcf_"$suffix" \
        ./scripts/merge_vcfs.sh $1 $gen $cov $per
    done
  done
done
