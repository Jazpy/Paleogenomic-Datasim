import os
import random

######################################################
# This script will find create a reference panel     #
# based on the individuals in the present/ directory #
######################################################

# Global dir
g_dir = '/mnt/Cromosoma/mavila/jmedina/Paleogenomic-Datasim/data_simulation'
out_dir = g_dir + '/reference/'
pre_dir = g_dir + '/present/'

# Lists where file output will be stored, included headers
sam_f = ['sample population group sex']
leg_f = ['id position a0 a1']
hap_f = []

# Make sure directory exists
if not os.path.exists(pre_dir):
    print('present sequence folder not present, '
            'try running gen_genomes.py first')
    quit()

# Get file list
files = [os.path.join(pre_dir, f) for f in os.listdir(pre_dir) if
        os.path.isfile(os.path.join(pre_dir, f))]

# Make sure it has the correct format, we need two chromosomes
# per individual
if len(files) % 2 != 0:
    print('Odd number of present chromosomes')
    quit()

# Calculate total individuals
individuals = int(len(files) / 2)

# List where all haplotypes will be stored
haplotypes = []

for i in range(individuals):
    # Add to SAMPLE file, dummy values for population
    # and group, random sex
    sam_f.append('IND' + str(i + 1) + ' FOO BAR ' + random.choice(['1', '2']))

    # Individual string
    ind_string = 'individual.' + str(i + 1)

    # Build both filepaths
    chr_path_1 = pre_dir + ind_string + '.1.fa'
    chr_path_2 = pre_dir + ind_string + '.2.fa'

    # Open both chromosome files
    with open(chr_path_1, 'r') as chr1, open(chr_path_2, 'r') as chr2:
        # Extract sequences
        haplotypes.append(chr1.readlines()[1])
        haplotypes.append(chr2.readlines()[1])

# List with SNPs (index, [alleles])
snps = []

for site in range(len(haplotypes[0])):
    ref_site = haplotypes[0][site]

    if ref_site == '\n':
        continue

    alleles = [ref_site]
    snp = (site, alleles)

    for hap in haplotypes:
        #if hap[site] != ref_site and not hap[site] in alleles:
        if not hap[site] in alleles:
            alleles.append(hap[site])

    # TO REMOVE
    if len(snp[1]) == 1:
        alleles.append(ref_site)

    # Ignore triallelic+ sites
    if len(snp[1]) == 2:
        snps.append(snp)

# Begin output creation of legend and hap files

# LEGEND and HAP file
for (snp_index, snp) in zip(range(1, len(snps) + 1), snps):

    # LEGEND file
    leg_line = 'SNP' + str(snp_index) + ' '
    leg_line += str(snp[0] + 1) + ' '
    leg_line += snp[1][0] + ' ' + snp[1][1]
    leg_f.append(leg_line)

    # HAP file
    hap_line = ''

    for hap in haplotypes:
        hap_base = hap[snp[0]]

        if hap_base == snp[1][0]:
            hap_line += '0 '
        elif hap_base == snp[1][1]:
            hap_line += '1 '

    # Remove trailing space
    hap_f.append(hap_line[:-1])

# Write to files
with open(out_dir + 'ref_panel.sam', 'w') as out_sam, open(out_dir + 'ref_panel.leg', 'w') as out_leg, open(out_dir + 'ref_panel.hap', 'w') as out_hap:

    for line in sam_f:
        out_sam.write(line + '\n')

    for line in leg_f:
        out_leg.write(line + '\n')

    for line in hap_f:
        out_hap.write(line + '\n')
