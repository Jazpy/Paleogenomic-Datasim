import msprime
import sys
import subprocess
import shutil
import os
import math

########################
# Important parameters #
########################

# Global dir
g_dir = '/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation'

# Gens of ancient individuals
gens = int(sys.argv[1])
# Number of contamination individuals
contamination_individuals = 1
# Number of ancient individuals
ancient_individuals = int(sys.argv[2])
# Numer of present day individuals (excluding contaminant)
present_individuals = int(sys.argv[3]) + 1
# Number of bases to simulate
num_bases = int(sys.argv[4])
# Time of population split
pop_split = int(sys.argv[5])
# Time of bottleneck
bottleneck_time = int(sys.argv[6])

#####################################
# Simulate chromosomes with msprime #
#####################################

# Simulate mass migration with the given split argument
if(pop_split > 0):
    pop_configs = [
	msprime.PopulationConfiguration(initial_size=1e4),
	msprime.PopulationConfiguration(initial_size=1e4)
    ]

    dem_events = [
	msprime.MassMigration(time=pop_split, source=0, destination=1, proportion=0.5)
    ]
elif(bottleneck_time > 0):
    pop_configs = [
	msprime.PopulationConfiguration(initial_size=1e4),
    ]

    dem_events = [
	msprime.PopulationParametersChange(time=bottleneck_time, initial_size=100, population_id=0)
    ]

# Create sample list
samples = []

for _ in range(contamination_individuals + present_individuals):
        samples.append(msprime.Sample(0, 0))
        samples.append(msprime.Sample(0, 0))

# If there was a population split, we'll use 2 different populations
if(pop_split > 0):
	ancient_pop = 1
else:
	ancient_pop = 0

for _ in range(ancient_individuals):
	samples.append(msprime.Sample(ancient_pop, gens))
	samples.append(msprime.Sample(ancient_pop, gens))

# Run simulation and extract results
if(pop_split > 0 or bottleneck_time > 0):
	tree_seq = msprime.simulate(
		samples=samples, recombination_rate=2e-8,
        	mutation_rate=2e-8, length=num_bases,
		population_configurations=pop_configs,
		demographic_events=dem_events)
else:
	tree_seq = msprime.simulate(
		samples=samples, recombination_rate=2e-8,
        	mutation_rate=2e-8, length=num_bases, Ne=1e4)

total_mutations = tree_seq.get_num_mutations()

############################################
# Transform data for seq-gen compatibility #
############################################

tree_filepath = 'tree_data'
tree_seq.dump(tree_filepath)

# Get Newick format tree and partitions
newick_filepath = 'newick_tree'
newick_file = open(newick_filepath, 'w')
subprocess.run(['msp', 'newick', '--precision', '14', tree_filepath], stdout=newick_file)
newick_file.close()

# Get each tree's interval, this needs to be appended to the beginning
# of each Newick tree described in the file. Intervals are used by seq-gen
# to merge the multiple trees that result from recombination
intervals = []
for tree in tree_seq.trees():
    length = tree.get_length()
    intervals.append(int(length))

# Fix rounding error
diff = num_bases - sum(intervals)

if diff != 0:
    intervals[len(intervals) - 1] += diff

# Get number of partitions and add intervals
partitions = 0
added_intervals = []
with open(newick_filepath, 'r') as newick_file:
    
    for line, interval in zip(newick_file, intervals):
        added_intervals.append('[' + str(interval) + '] ' + line)
        partitions += 1

# Overwrite Newick file with added intervals
with open(newick_filepath, 'w') as newick_file:
    newick_file.writelines(added_intervals)

##############################
# Run seq-gen on Newick tree #
##############################

if gens <= 100:
    branch_scale = 80e-9
elif gens <= 200:
    branch_scale = 73e-9
else:
    branch_scale = 60e-9

seqgen_filepath = 'sequence_data'

with open(seqgen_filepath, 'w') as seqgen_file:
    subprocess.run(['seq-gen', '-mHKY', '-l' + str(num_bases),
        '-s' + str(branch_scale), '-p', str(partitions),
        newick_filepath], stdout=seqgen_file)

# Sort sequences, msprime does not output chromosomes in order.
# We will also remove the header, since this sequence file will be split
# into several files representing our individuals

# Small auxiliary function for sorting with key
def get_key(s):
    return int(s.split()[0])

chr_sequences = []
with open(seqgen_filepath, 'r') as seqgen_file:
    chr_sequences = seqgen_file.readlines()

# Remove header and sort
chr_sequences.pop(0)
chr_sequences.sort(key=get_key)

# Write only sequence to file
with open(seqgen_filepath, 'w') as seqgen_file:
    for line in chr_sequences:
        seqgen_file.write(line.split()[1] + '\n')

# Remove Newick and HDF 5 files
if os.path.exists(newick_filepath):
    os.remove(newick_filepath)
if os.path.exists(tree_filepath):
    os.remove(tree_filepath)

sites = 0
with open(seqgen_filepath, 'r') as seqgen_file:
    chr_lines = seqgen_file.readlines()

    for i in range(num_bases):

        start = chr_lines[0][i]

        for line in chr_lines:
            if line[i] != start:
                sites += 1
                break

print('Segregating sites: ' + str(sites))

##############################################
# Split seq-gen output into individual files #
##############################################

# Directory constants
con_dir = g_dir + '/contaminant/'
pre_dir = g_dir + '/present/'
anc_dir = g_dir + '/ancient/'
ref_dir = g_dir + '/reference/'

# Create clean directories
if os.path.exists(con_dir):
    shutil.rmtree(con_dir)

if os.path.exists(pre_dir):
    shutil.rmtree(pre_dir)

if os.path.exists(anc_dir):
    shutil.rmtree(anc_dir)

if os.path.exists(ref_dir):
    shutil.rmtree(ref_dir)

os.makedirs(con_dir)
os.makedirs(pre_dir)
os.makedirs(anc_dir)
os.makedirs(ref_dir)

# Split individuals
with open(seqgen_filepath, 'r') as seqgen_file:
    chr_sequences = seqgen_file.readlines()

chr_index = 0
    
#####################
# Split contaminant #
#####################

# First contaminant chromosome
filename = 'cont.1.fa'
with open(con_dir + filename, 'w') as f:
    # Write header
    f.write('>cont_1' + '\n')
    # Write only the sequence, no chromosome index
    f.write(chr_sequences[chr_index])

    # Move onto next chromosome
    chr_index += 1

# Second contaminant chromosome
filename = 'cont.2.fa'
with open(con_dir + filename, 'w') as f:
    # Write header
    f.write('>cont_1' + '\n')
    # Write only the sequence, no chromosome index
    f.write(chr_sequences[chr_index])

    chr_index += 1

#################################
# Split present day individuals #
#################################

for i in range(present_individuals):

    # Individual string
    ind_string = 'individual.' + str(i + 1)
        
    # First chromosome
    filename = ind_string + '.1.fa'

    with open(pre_dir + filename, 'w') as f:
        # Write header
        f.write('>individual_' + str(i + 1) + '\n')
        # Write sequence
        f.write(chr_sequences[chr_index])

    chr_index += 1

    # First chromosome
    filename = ind_string + '.2.fa'

    with open(pre_dir + filename, 'w') as f:
        # Write header
        f.write('>individual_' + str(i + 1) + '\n')
        # Write sequence
        f.write(chr_sequences[chr_index])

    chr_index += 1

#############################
# Split ancient individuals # 
#############################

for i in range(ancient_individuals):

    # Individual string
    ind_string = 'ancient.' + str(i + 1)
        
    # First chromosome
    filename = ind_string + '.1.fa'

    with open(anc_dir + filename, 'w') as f:
        # Write header
        f.write('>ancient_' + str(i + 1) + '\n')
        # Write sequence
        f.write(chr_sequences[chr_index])

    chr_index += 1

    # First chromosome
    filename = ind_string + '.2.fa'

    with open(anc_dir + filename, 'w') as f:
        # Write header
        f.write('>ancient_' + str(i + 1) + '\n')
        # Write sequence
        f.write(chr_sequences[chr_index])

    chr_index += 1

###########
# Cleanup #
###########
if os.path.exists(seqgen_filepath):
    os.remove(seqgen_filepath)

#####################
# Output statistics #
#####################

print("\n**************************")
print("gen_genomes.py statistics:")
print("**************************\n")
print("Total mutations = ", total_mutations)
