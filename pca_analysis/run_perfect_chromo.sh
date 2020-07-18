rm -rf chromo_"$1"/perfect_chromo
mkdir chromo_"$1"/perfect_chromo
rm -rf chromo_"$1"/perfect_work
mkdir chromo_"$1"/perfect_work
rm -rf chromo_"$1"/perfect_fs
mkdir chromo_"$1"/perfect_fs

declare -a gens=( "0gen" "25gen" "50gen" "100gen" "200gen" "400gen" )

for gen in "${gens[@]}"
do
  suffix="$gen"

  qsub -N merge_perfect_unions_"$suffix" \
    ./scripts/merge_perfect_unions.sh $1 $gen

  qsub -N perf_finestructure_"$suffix" -e ./logs/perf_finestructure_"$suffix" \
    -o ./logs/perf_finestructure_"$suffix" \
    -hold_jid merge_perfect_unions_"$suffix" \
    ./scripts/run_perfect_finestructure.sh $1 $suffix
done
