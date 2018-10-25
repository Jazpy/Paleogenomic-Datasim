import statistics
import os
import sys

# Parameters
# Gens of ancient individuals
gens = int(sys.argv[1])
# Number of ancient individuals
ancients = int(sys.argv[2])
# Numer of present day individuals (excluding contaminant)
references = int(sys.argv[3])
# Number of bases to simulate
num_bases = int(sys.argv[4])

# Global dir
g_dir = '/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation/'
data_dir = g_dir + 'cases/'

# Output path and list to store output
out_paths = []

# Iterate over all directories in data_dir
gen_dirs = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if
	os.path.isdir(os.path.join(data_dir, f))]

data_dirs = []
for dir in gen_dirs:
	coverages = [os.path.join(dir, f) for f in os.listdir(dir) if
		os.path.isdir(os.path.join(dir, f))]
	for coverage in coverages:
		percents = [os.path.join(coverage, f) 
			for f in os.listdir(coverage) if 
			os.path.isdir(os.path.join(coverage, f))]
		for percent in percents:
			data_dirs.append(percent)

case_dict = {}
for dir in data_dirs:
	dir_split = dir.split('/')
	case_file = '{}_{}'.format(dir_split[-2], dir_split[-1])
	case_dict[case_file] = []
		
for dir in data_dirs:
	dir_split = dir.split('/')
	case_file = '{}_{}'.format(dir_split[-2], dir_split[-1])

	with open(dir + '/phasing_results.txt', 'r') as res_f:
		res_line = res_f.readlines()[-1]
	with open(dir + '/vcf_stats.txt', 'r') as vcf_f:
		vcf_lines = vcf_f.readlines()
		vcf_depth_line = vcf_lines[-3]
		vcf_variants_line = vcf_lines[-1]
	with open(dir + '/depth', 'r') as dep_f:
		dep_lines = dep_f.readlines()
		dep_line = '0'

		if len(dep_lines) > 0:
			dep_line = dep_lines[0]

	accuracy = float(res_line.split()[2])
	vcf_depth = float(vcf_depth_line)
	vcf_variants = float(vcf_variants_line)
	raw_depth = float(dep_line)

	case_dict[case_file].append(accuracy)
	case_dict[case_file].append(vcf_depth)
	case_dict[case_file].append(vcf_variants)
	case_dict[case_file].append(raw_depth)

result_files = []
run_file_prefix = 'gargammel_{}_{}gen_{}MB_{}Ref_'.format(ancients, gens, int(num_bases / 1000000), references)

for key, value in case_dict.items():
	acc_file = g_dir + run_file_prefix + key + '_acc'
	fil_file = g_dir + run_file_prefix + key + '_fil_depth'
	var_file = g_dir + run_file_prefix + key + '_var'
	raw_file = g_dir + run_file_prefix + key + '_raw_depth'

	result_files.extend((acc_file, fil_file, var_file, raw_file))

	with open(acc_file, 'w') as out_f:
		for line in value[0::4]:
			out_f.write('{}\n'.format(line))
	with open(fil_file, 'w') as out_f:
		for line in value[1::4]:
			out_f.write('{}\n'.format(line))
	with open(var_file, 'w') as out_f:
		for line in value[2::4]:
			out_f.write('{}\n'.format(line))
	with open(raw_file, 'w') as out_f:
		for line in value[3::4]:
			out_f.write('{}\n'.format(line))

# Get ms - seqgen difference in segsites
with open(g_dir + 'logs/std/pre_gargammel', 'r') as seg_file:
	seg_lines = seg_file.readlines()
	seqgen_seg = seg_lines[-7].split()[-1]
	msprime_seg = seg_lines[-1].split()[-1]

# Write summary file
summary_lines = []
summary_lines.append('msprime segsites: {}'.format(msprime_seg))
summary_lines.append('seqgen segsites: {}'.format(seqgen_seg))

for f in result_files:
	
	# Get stats
	with open(f, 'r') as curr_f:
		lines = [float(x) for x in curr_f.readlines()]

		curr_min = min(lines)
		curr_max = max(lines)
		curr_avg = statistics.mean(lines)
		curr_sd = statistics.pstdev(lines)

	summary_lines.append('\nStats for {}:\nMin = {}\nMax = {}\nAvg = {}\nSD = {}'.format(f.split('/')[-1],
		curr_min, curr_max, curr_avg, curr_sd))

with open(g_dir + run_file_prefix + 'summary', 'w') as out_f:
	for line in summary_lines:
		out_f.write('{}\n'.format(line))
