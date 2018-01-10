import msprime
import subprocess
import shutil
import os

########################
# Important parameters #
########################

# Number of bases to simulate
num_bases = 1000

# Numer of present day individuals (excluding contaminant)
present_individuals = 11
# Number of ancient individuals
ancient_individuals = 5

# Our samples, 12 modern genomes and
# 5 ancient genomes sampled 25, 50, 100, 200, and
# 400 generations ago.
samples = [
        # Present samples

        # Contamination individual - 2 chromosomes
        msprime.Sample(0, 0), # index 0
        msprime.Sample(0, 0),

        # Mapping reference individual - 2 chromosomes
        msprime.Sample(0, 0), # index 2
        msprime.Sample(0, 0),

        # Phasing individuals, 10 individuals - 20 chromosomes
        msprime.Sample(0, 0), # index 4
        msprime.Sample(0, 0),
        msprime.Sample(0, 0), # index 6
        msprime.Sample(0, 0),
        msprime.Sample(0, 0), # index 8
        msprime.Sample(0, 0),
        msprime.Sample(0, 0), # index 10
        msprime.Sample(0, 0),
        msprime.Sample(0, 0), # index 12
        msprime.Sample(0, 0),
        msprime.Sample(0, 0), # index 14
        msprime.Sample(0, 0),
        msprime.Sample(0, 0), # index 16
        msprime.Sample(0, 0),
        msprime.Sample(0, 0), # index 18
        msprime.Sample(0, 0),
        msprime.Sample(0, 0), # index 20
        msprime.Sample(0, 0),
        msprime.Sample(0, 0), # index 22
        msprime.Sample(0, 0),

        # 5 ancient individuals, 2 chromosomes per individual
        msprime.Sample(0, 25), # index 24
        msprime.Sample(0, 25),

        msprime.Sample(0, 50), # index 26
        msprime.Sample(0, 50),

        msprime.Sample(0, 100), # index 28
        msprime.Sample(0, 100),

        msprime.Sample(0, 200), # index 30
        msprime.Sample(0, 200),

        msprime.Sample(0, 400), # index 32
        msprime.Sample(0, 400)
        ]

#####################################
# Simulate chromosomes with msprime #
#####################################
 
# Run simulation and extract results
tree_seq = msprime.simulate(recombination_rate=2e-8,
        mutation_rate=2e-8, Ne=1e4, length=num_bases, samples=samples)

print("Total mutations = ", tree_seq.get_num_mutations())

for variant in tree_seq.variants():
    print(variant.index, variant.position, variant.genotypes, sep="\t")

############################################
# Transform data for seq-gen compatibility #
############################################
tree_filepath = 'tree_data'
tree_seq.dump(tree_filepath)

# Get Newick format tree and partitions
newick_filepath = 'newick_tree'
newick_file = open(newick_filepath, 'w')
subprocess.run(['msp', 'newick', tree_filepath], stdout=newick_file)
newick_file.close()

# Get each tree's interval, this needs to be appended to the beginning
# of each Newick tree described in the file. Intervals are used by seq-gen
# to merge the multiple trees that result from recombination
intervals = []
for tree in tree_seq.trees():
    intervals.append(int(round(tree.get_length())))

print('\nInterval total sum: ' + str(sum(intervals)) + '\n')

# TODO: Fix this thing
# Exit gracefully if intervals are wrong
if sum(intervals) != num_bases:
    print('Messed up intervals')
    quit()

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

# 0.00045 taken from Gargammel example. msprime does not
# use coalescence units so we divide by 40k to convert
branch_scale = 0.00045 / 40000
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

##############################################
# Split seq-gen output into individual files #
##############################################

# Directory constants
con_dir = './contaminant/'
pre_dir = './present/'
anc_dir = './ancient/'

# Create clean directories
if os.path.exists(con_dir):
    shutil.rmtree(con_dir)

if os.path.exists(pre_dir):
    shutil.rmtree(pre_dir)

if os.path.exists(anc_dir):
    shutil.rmtree(anc_dir)

os.makedirs(con_dir)
os.makedirs(pre_dir)
os.makedirs(anc_dir)

# Split individuals
with open(seqgen_filepath, 'r') as seqgen_file:
    chr_sequences = seqgen_file.readlines()
    chr_index = 0
    
    #####################
    # Split contaminant #
    #####################

    # First contaminant chromosome
    filename = 'cont_1_.fa'
    with open(con_dir + filename, 'w') as f:
        # Write header
        f.write('>cont_1' + '\n')
        # Write only the sequence, no chromosome index
        f.write(chr_sequences[chr_index])

        # Move onto next chromosome
        chr_index += 1

    # Second contaminant chromosome
    filename = 'cont_2_.fa'
    with open(con_dir + filename, 'w') as f:
        # Write header
        f.write('>cont_2' + '\n')
        # Write only the sequence, no chromosome index
        f.write(chr_sequences[chr_index])

        chr_index += 1


    #################################
    # Split present day individuals #
    #################################

    for i in range(present_individuals):

        # Individual string
        ind_string = 'individual_' + str(i)
        
        # First chromosome
        filename = ind_string + '_1.fa'

        with open(pre_dir + filename, 'w') as f:
            # Write header
            f.write('>' + ind_string + '_1' + '\n')
            # Write sequence
            f.write(chr_sequences[chr_index])

            chr_index += 1

        # First chromosome
        filename = ind_string + '_2.fa'

        with open(pre_dir + filename, 'w') as f:
            # Write header
            f.write('>' + ind_string + '_2' + '\n')
            # Write sequence
            f.write(chr_sequences[chr_index])

            chr_index += 1

    #############################
    # Split ancient individuals # 
    #############################

    for i in range(ancient_individuals):

        # Individual string
        ind_string = 'ancient_' + str(i)
        
        # First chromosome
        filename = ind_string + '_1.fa'

        with open(anc_dir + filename, 'w') as f:
            # Write header
            f.write('>' + ind_string + '_1' + '\n')
            # Write sequence
            f.write(chr_sequences[chr_index])

            chr_index += 1

        # First chromosome
        filename = ind_string + '_2.fa'

        with open(anc_dir + filename, 'w') as f:
            # Write header
            f.write('>' + ind_string + '_2' + '\n')
            # Write sequence
            f.write(chr_sequences[chr_index])

            chr_index += 1

###########
# Cleanup #
###########
if os.path.exists(seqgen_filepath):
    os.remove(seqgen_filepath)