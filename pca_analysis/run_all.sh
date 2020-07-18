sim=$1
num_anc=20

./setup.sh $sim

# Run chromopainter
./run_chromo.sh $sim $num_anc true 0
for (( i = 1; i < 5; i++ ))
do
  while qstat | grep "finestruct" > /dev/null;
  do
    echo "sleeping... (finestructure)"
    sleep 20m
  done
  sleep 2m

  echo "Done with offset $i"

  ./run_chromo.sh $sim $num_anc false $i
done
