echo $$

declare -a gens=("0" "25" "50" "100" "200" "400")
declare -a splits=("0" "25" "50" "100" "200")

for split in "${splits[@]}"
do
	for gen in "${gens[@]}"
	do
		mkdir "$gen"gen

		echo "Running ""$gen""gen case..."
		./run_scripts.sh "$gen" 100 500 1000000 "$split"
		while [[ $(qstat | grep results_re) ]]
		do
			sleep 20m
		done
		sleep 5m
		mv gargammel* "$gen"gen
	done

	mkdir ../results/ref_panel_split"$split"
	mv *gen ../results/ref_panel_split"$split"
done
