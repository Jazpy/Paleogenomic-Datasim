import os
import sys

curr_dir = os.getcwd()

chr1_file = f'{curr_dir}/chr.1.fa'
chr2_file = f'{curr_dir}/chr.1.fa'
ref_hap = f'{curr_dir}/../../reference/combined.haps'
out_sam = f'{curr_dir}/perfect.sample'
out_hap = f'{curr_dir}/perfect.haps'
anc_id = sys.argv[1]

# Build SAMPLE file
'''
sam_lines = []
sam_lines.append('ID_1 ID_2 missing\n')
sam_lines.append('0 0 0\n')
sam_lines.append(f'ANC{anc_id} ANC{anc_id} 0')

with open(out_sam, 'w') as out_f:
  out_f.writelines(sam_lines)
'''

# Get chromosome files
with open(chr1_file, 'r') as chr1_f, open(chr2_file, 'r') as chr2_f:
  chr1 = chr1_f.readlines()[1]
  chr2 = chr2_f.readlines()[1]

with open(ref_hap, 'r') as ref_f, open(out_hap, 'w') as out_f:
  for line in ref_f:
    line = line.strip()
    line_toks = line.split()
    site = int(line_toks[2])
    a0 = line_toks[3]
    a1 = line_toks[4]

    c1 = chr1[site - 1]
    c2 = chr2[site - 1]

    # Ignore mono or triallelic sites
    if a0 == a1:
      continue
    if (c1 != a0 and c1 != a1) or (c2 != a0 and c2 != a1):
      continue

    h0 = 0 if c1 == a0 else 1
    h1 = 0 if c2 == a0 else 1

    out_f.write(f'{line_toks[0]} {line_toks[1]} {line_toks[2]} {line_toks[3]} {line_toks[4]} {h0} {h1}\n')
