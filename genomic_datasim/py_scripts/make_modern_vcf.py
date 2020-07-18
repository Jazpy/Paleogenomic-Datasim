import sys

def main():
  leg_file = 'ref_panel.leg'
  hap_file = 'ref_panel.hap'
  out_vcf = 'modern.vcf'

  moderns = int(sys.argv[1])

  leg_lines = []
  hap_lines = []
  with open(leg_file, 'r') as leg:
    for line in leg:
      if 'position' in line:
        continue

      toks = line.split()[1:4]
      leg_lines.append(toks)

  with open(hap_file, 'r') as hap:
    for line in hap:
      toks = line.split()

      hap_line = ''
      for h0, h1 in zip(toks[0::2], toks[1::2]):
        if h0 == h1:
          to_add = f'{h0}/{h1}\t'
        else:
          to_add = '0/1\t'
        hap_line += to_add

      hap_lines.append(hap_line.strip())

  out_lines = ['##fileformat=VCFv4.2\n']
  out_lines.append('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
  header_line = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT'

  for i in range(moderns):
    header_line += f'\tMOD{i + 1}'

  out_lines.append(header_line + '\n')

  for leg, haps in zip(leg_lines, hap_lines):
    out_lines.append(f'sim\t{leg[0]}\t.\t{leg[1]}\t{leg[2]}\t999\t.\t.\tGT\t{haps}\n')

  with open(out_vcf, 'w') as out:
    out.writelines(out_lines)

if __name__ == '__main__':
  main()
