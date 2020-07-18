import sys

def main():
  prefix = sys.argv[1]
  out_vcf = sys.argv[2]

  if len(sys.argv) > 3 and sys.argv[3].lower() == 'true':
    phased_output = True
  else:
    phased_output = False

  moderns = 0
  ancients = 0

  with open(prefix + '.sample', 'r') as sam:
    for line in sam:
      if 'PRE' in line:
        moderns += 1
      elif 'ANC' in line:
        ancients += 1

  sites = []
  hap_lines = []
  alleles = []
  with open(prefix + '.haps', 'r') as hap:
    for line in hap:
      toks = line.split()

      sites.append(toks[2])

      hap_line = ''
      for h0, h1 in zip(toks[5::2], toks[6::2]):
        if phased_output or h0 == h1:
          to_add = f'{h0}/{h1}\t'
        else:
          to_add = '0/1\t'
        hap_line += to_add

      hap_lines.append(hap_line.strip())

      alleles.append(toks[3:5])

  out_lines = ['##fileformat=VCFv4.2\n']
  out_lines.append('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
  header_line = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT'

  for i in range(moderns):
    header_line += f'\tMOD{i + 1}'
  for i in range(ancients):
    header_line += f'\tANC{i + 1}'

  out_lines.append(header_line + '\n')

  for site, haps, als in zip(sites, hap_lines, alleles):
    if als[0] == als[1]:
      out_lines.append(f'sim\t{site}\t.\t{als[0]}\t.\t999\t.\t.\tGT\t{haps}\n')
    else:
      out_lines.append(f'sim\t{site}\t.\t{als[0]}\t{als[1]}\t999\t.\t.\tGT\t{haps}\n')

  with open(out_vcf, 'w') as out:
    out.writelines(out_lines)

if __name__ == '__main__':
  main()
