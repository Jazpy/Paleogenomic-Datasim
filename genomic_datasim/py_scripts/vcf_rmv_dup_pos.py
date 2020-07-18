import sys

filename = sys.argv[1]

# Get vcf data
new_lines = []
prev_pos = 0
with open(filename) as vcf_f:
  for line in vcf_f.readlines():
    if line.startswith('#'):
      new_lines.append(line)
      continue

    line_pos = int(line.split()[1])

    if line_pos == prev_pos:
      continue
    else:
      new_lines.append(line)
      prev_pos = line_pos

with open(filename, 'w') as vcf_f:
  for line in new_lines:
    vcf_f.write(line)
