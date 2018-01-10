import msprime
import subprocess

# Specify our samples, 11 modern genomes and
# 5 ancient genomes taken 25, 50, 100, 200, and
# 400 generations ago.
samples = [
        # Present samples
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),
        msprime.Sample(0, 0),

        # Ancient samples
        msprime.Sample(0, 25),
        msprime.Sample(0, 50),
        msprime.Sample(0, 100),
        msprime.Sample(0, 200),
        msprime.Sample(0, 400)
        ]

# Number of bases to simulate
num_bases = 1000

# Run simulation and extract results
tree_seq = msprime.simulate(recombination_rate=2e-8,
        mutation_rate=2e-8, Ne=1e4, length=num_bases, samples=samples)

print("Total mutations = ", tree_seq.get_num_mutations())

for variant in tree_seq.variants():
    print(variant.index, variant.position, variant.genotypes, sep="\t")

# Dump data for seq-gen compatibility
tree_seq.dump('tree_data')

# Get Newick format tree and partitions
newick_filepath = 'newick_tree'
newick_file = open(newick_filepath, 'w')
subprocess.run(['msp', 'newick', 'tree_data'], stdout=newick_file)
newick_file.close()

# Get each tree's interval
intervals = []
for tree in tree_seq.trees():
    intervals.append(int(round(tree.get_length())))

print('\nInterval total sum: ' + str(sum(intervals)) + '\n')

# Get number of partitions and add intervals
partitions = 0
added_intervals = []
with open(newick_filepath, 'r') as newick_file:
    
    for line, interval in zip(newick_file, intervals):
        added_intervals.append('[' + str(interval) + '] ' + line)
        partitions = partitions + 1

# Overwrite Newick file
with open(newick_filepath, 'w') as newick_file:
    newick_file.writelines(added_intervals)

# Run seq-gen on Newick tree
branch_scale = 0.00045 / 40000
seqgen_filepath = 'sequence_data'

seqgen_file = open(seqgen_filepath, 'w')
subprocess.run(['seq-gen', '-mHKY', '-l' + str(num_bases),
    '-s' + str(branch_scale), '-p', str(partitions), newick_filepath], stdout=seqgen_file)
