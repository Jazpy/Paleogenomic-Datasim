import msprime

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

# Run simulation and extract results
#tree_seq = msprime.simulate(recombination_rate=2e-8, mutation_rate=2e-8,
        #Ne=1e4, length=46e6, samples=samples)
tree_seq = msprime.simulate(recombination_rate=2e-8, mutation_rate=2e-8,
        Ne=1e4, length=500, samples=samples)

# Extract sequence data
