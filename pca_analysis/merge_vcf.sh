declare -a covs=( "10x" "5x" )
declare -a pers=( "0" "2" "5" "10" )

for cov in "${covs[@]}"
do
  for per in "${pers[@]}"
  do
    suffix="$cov"_"$per"
    bgzip -d variants_biallelic_"$suffix".vcf.gz
    bgzip variants_biallelic_"$suffix".vcf
    tabix -p vcf variants_biallelic_"$suffix".vcf.gz
  done
done
