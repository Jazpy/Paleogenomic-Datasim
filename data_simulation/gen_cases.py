import subprocess
import shutil
import os

########################
# Important parameters #
########################

# Number of cases, one for each ancient individual
num_cases = int(len(os.listdir('./ancient/')) / 3)

#######################
# Directory structure #
#######################

# Directory constants
main_dir = './cases/'

# Create clean directories, one for each case
if os.path.exists(main_dir):
    shutil.rmtree(main_dir)

os.makedirs(main_dir)

for i in range(num_cases):
    dir_string = main_dir + 'case_' + str(i + 1) + '/'
    os.makedirs(dir_string)

    # Directories for contaminant and endogenous data
    endo_dir = dir_string + 'endo/'
    cont_dir = dir_string + 'cont/'
    bact_dir = dir_string + 'bact/'

    os.makedirs(endo_dir)
    os.makedirs(cont_dir)
    os.makedirs(bact_dir)

#################
# Data movement #
#################

# Make copies of contaminant and reference for each case
for i in range(num_cases):
    case_index = i + 1
    dir_string = main_dir + 'case_' + str(case_index) + '/'

    con_dir = './contaminant/'
    shutil.copyfile(con_dir + 'cont.1.fa', dir_string + 'cont/cont.1.fa')
    shutil.copyfile(con_dir + 'cont.2.fa', dir_string + 'cont/cont.2.fa')

    ref_dir = './reference/'
    shutil.copyfile(ref_dir + 'ref.fa', dir_string + 'ref.fa')

# Move each ancient human (and segsites) to its own case directory
for ancient in os.listdir('./ancient/'):
    filepath = './ancient/' + ancient
    case_index = ancient.split('.')[1]

    # Special case for segsites
    if 'segsites' in ancient:
        # Simply move it to its case folder
        dir_string = main_dir + 'case_' + case_index + '/'
        shutil.move(filepath, dir_string + 'endo/segsites')
        continue

    # Get case number (individual's index) and chr index
    chr_index = ancient.split('.')[2]

    # Move file to case folder
    dir_string = main_dir + 'case_' + case_index + '/'
    shutil.move(filepath, dir_string + 'endo/endo.' + str(chr_index) + '.fa')

###########
# Cleanup #
###########
if os.path.exists('./ancient'):
    shutil.rmtree('./ancient')

if os.path.exists('./reference'):
    shutil.rmtree('./reference')

if os.path.exists('./contaminant'):
    shutil.rmtree('./contaminant')
