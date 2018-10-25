g_dir="/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation"

rm "$g_dir"/logs/err/*
rm "$g_dir"/logs/std/*

rm -rf "$g_dir"/data/
rm -rf "$g_dir"/present/
rm -rf "$g_dir"/reference/

touch "$g_dir"/logs/err/pre_gargammel
touch "$g_dir"/logs/std/pre_gargammel

touch "$g_dir"/logs/err/gargammel
touch "$g_dir"/logs/std/gargammel

touch "$g_dir"/logs/err/pre_map
touch "$g_dir"/logs/std/pre_map

touch "$g_dir"/logs/err/map
touch "$g_dir"/logs/std/map

touch "$g_dir"/logs/err/call_variants
touch "$g_dir"/logs/std/call_variants

touch "$g_dir"/logs/err/phase
touch "$g_dir"/logs/std/phase

touch "$g_dir"/logs/err/results
touch "$g_dir"/logs/std/results

qsub "$g_dir"/scripts/pre_gargammel.sh $1 $2 $3 $4 $5
qsub "$g_dir"/scripts/gargammel.sh
qsub "$g_dir"/scripts/pre_map.sh
qsub "$g_dir"/scripts/map.sh
qsub "$g_dir"/scripts/call_variants.sh
qsub "$g_dir"/scripts/phase.sh
qsub "$g_dir"/scripts/results.sh $1 $2 $3 $4
