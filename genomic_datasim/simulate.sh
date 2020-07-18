# Found empirically, don't question them
gens=( "0" "25" "50" "100" "200" "400" )
branch_lengths=( "8.03" "7.90" "7.80" "7.58" "7.20" "6.55" )

event="split"
e_time="200"
bases=2000000
ancs=100
mods=500
method="ref"

sleep_fn () {
  while qstat | grep "results" > /dev/null;
  do
    echo "sleeping... (phase)"
    sleep 20m
  done
  sleep 3m
}

for ((i=0; i<${#gens[@]}; i++))
do
  gen=${gens[$i]}
  branch=${branch_lengths[$i]}
  if [ $event == "canon" ]
  then
    ./run_scripts.sh $gen $ancs $mods $bases "$branch"e-08 $method
  else
    ./run_scripts.sh $gen $ancs $mods $bases "$branch"e-08 $method $event $e_time
  fi
  sleep_fn
done

mkdir "$method"_"$event""$e_time"
mv *gen "$method"_"$event""$e_time"