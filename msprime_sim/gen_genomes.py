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
num_bases = 46e6

# Run simulation and extract results
tree_seq = msprime.simulate(recombination_rate=2e-8, mutation_rate=2e-8,
        Ne=1e4, length=num_bases, samples=samples)

# Dump data for seq-gen compatibility
tree_seq.dump('tree_data')

# Get Newick format tree
newick_filepath = 'newick_tree'
newick_file = open(newick_filepath, 'w')
subprocess.run(['msp', 'newick', 'tree_data'], stdout=newick_file)

# Run seq-gen on Newick tree
seqgen_filepath = 'sequence_data'
seqgen_file = open(seqgen_filepath, 'w')
subprocess.run(['seq-gen', '-mHKY', '-l' + str(num_bases), newick_filepath], stdout=seqgen_file)
