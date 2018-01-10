import numpy as np
import sys

if len(sys.argv) < 2:
    print("Usage: diff_sequences <SEQ-GEN OUTPUT FILE>")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    lines.pop(0)
    raw_lines = []
    chromosomes = len(lines)

    matrix = np.zeros(shape = (chromosomes + 1, chromosomes + 1)).astype('int')

    # Get nucleotides and format matrix
    counter = 1
    for line in lines:
        individual = line.split()[0]
        raw_lines.append(line.split()[1])
        matrix[0][counter] = individual
        matrix[counter][0] = individual
        counter = counter + 1

    # Find differences
    for i in range(len(raw_lines)):
        A = raw_lines[i]

        for j in range(len(raw_lines)):
            B = raw_lines[j]

            # Compare char by char
            differences = 0
            for x, y in zip(A, B):

                if x != y:
                    differences = differences + 1

            matrix[i + 1][j + 1] = differences

    print(matrix)
