sim=$1

#rm -rf logs
#mkdir logs

mkdir chromo_$1
mkdir chromo_$1/haps
mkdir chromo_$1/fs
mkdir chromo_$1/merged
mkdir chromo_$1/chromo
mkdir chromo_$1/work

declare -a gens=( "0gen" "25gen" "50gen" "100gen" "200gen" "400gen" )
declare -a covs=( "10x" "5x" )
declare -a pers=( "0" "2" "5" "10" )

for gen in "${gens[@]}"
do
  # Get combined present haps
  qsub ./scripts/present_haps.sh $sim $gen

  for cov in "${covs[@]}"
  do
    for per in "${pers[@]}"
    do
      # Build union haps
      suffix="$gen"_"$cov"_"$per"

      qsub -N build_unions_"$suffix" \
        ./scripts/build_unions.sh $1 $gen $cov $per
    done
  done
done
