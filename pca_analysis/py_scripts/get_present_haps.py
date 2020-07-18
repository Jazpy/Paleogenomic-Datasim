import os

curr_dir = os.getcwd()

ref_leg = f'{curr_dir}/reference/ref_panel.leg'
ref_hap = f'{curr_dir}/reference/ref_panel.hap'
out_hap = f'{curr_dir}/reference/combined.haps'
out_sam = f'{curr_dir}/reference/combined.sample'
moderns = 500

# Build SAMPLE file
sam_lines = []
sam_lines.append('ID_1 ID_2 missing\n')
sam_lines.append('0 0 0\n')
for i in range(500):
  sam_lines.append(f'PRE{i + 1} PRE{i + 1} 0\n')

with open(out_sam, 'w') as out_f:
  out_f.writelines(sam_lines)

# Get sites and haps for modern individual
with open(ref_leg, 'r') as leg_f, open(ref_hap, 'r') as hap_f, open(out_hap, 'w') as out_f:
  # Skip header for leg file
  leg_f.readline()

  # Iterate over SNPs and modern individuals, reconstructing one site at a time
  for leg_line, hap_line in zip(leg_f, hap_f):
    leg_line = leg_line.strip()
    hap_line = hap_line.strip()

    # Combine both lines and write
    new_line = f'ref_1 {leg_line} {hap_line}\n'
    out_f.write(new_line)
