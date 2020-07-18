rm -rf logs
mkdir logs

num_anc=$2
clean=$3
offset=$4

if [ "$clean" = "true" ]
then
  rm -rf chromo_"$1"
  mkdir chromo_"$1"
  mkdir chromo_"$1"/haps
  mkdir chromo_"$1"/merged
  mkdir chromo_"$1"/chromo
  mkdir chromo_"$1"/work
  mkdir chromo_"$1"/fs
fi

rm chromo_"$1"/merged/*
rm chromo_"$1"/chromo/*

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

      qsub -N merge_unions_"$suffix" \
        -hold_jid build_unions_"$suffix" \
        ./scripts/merge_unions.sh $1 $gen $cov $per $num_anc $offset

      qsub -N finestructure_"$suffix" -e ./logs/finestructure_"$suffix" \
        -o ./logs/finestructure_"$suffix" \
        -hold_jid merge_unions_"$suffix" \
        ./scripts/run_finestructure.sh $1 $suffix $offset
    done
  done
done
