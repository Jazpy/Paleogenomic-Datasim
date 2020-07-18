import sys

def main():
  leg_file = sys.argv[1]
  hap_file = sys.argv[2]
  moderns = int(sys.argv[3])
  ancients = int(sys.argv[4])
  anc_vcf = sys.argv[5]
  out_vcf = sys.argv[6]

  out_lines = ['##fileformat=VCFv4.2\n']
  out_lines.append('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
  header_line = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT'

  for i in range(moderns):
    header_line += f'\tMOD{i + 1}'

  for i in range(ancients):
    header_line += f'\tANC{i + 1}'

  out_lines.append(header_line + '\n')

  # Build anc dict
  anc_dict = {}
  with open(anc_vcf, 'r') as vcf:
    for line in vcf:
      if line[0] == '#':
        continue
      toks = line.split()
      site = int(toks[1])

      if toks[4] == '.':
        alleles = [toks[3], toks[3]]
      else:
        alleles = [toks[3], toks[4]]

      fields = toks[9:]
      haps = [x.split(':')[0] for x in fields]

      anc_dict[site] = [alleles, haps]

  with open(leg_file, 'r') as leg, open(hap_file, 'r') as hap:
    leg_lines = leg.readlines()[1:]
    hap_lines = hap.readlines()

  for leg, hap in zip(leg_lines, hap_lines):
    leg_toks = leg.split()
    hap_toks = hap.split()

    site = int(leg_toks[1])
    ref_alleles = [leg_toks[2], leg_toks[3]]
    anc_data = anc_dict.get(site, None)

    if not anc_data:
      continue

    anc_alleles = anc_data[0]
    anc_haps = anc_data[1]

    if ref_alleles == anc_alleles:
      inverted = False
    elif ref_alleles == anc_alleles[::-1]:
      inverted = True
    elif ref_alleles[0] == ref_alleles[1] and ref_alleles[0] == anc_alleles[0]:
      inverted = False
    elif ref_alleles[0] == ref_alleles[1] and ref_alleles[0] == anc_alleles[1]:
      inverted = True
    else:
      continue

    new_hap_line = ''
    for h0, h1 in zip(hap_toks[0::2], hap_toks[1::2]):
      if h0 == h1:
        to_add = f'{h0}/{h1}\t'
      else:
        to_add = '0/1\t'

      if inverted:
        to_add = to_add.replace('1', '2')
        to_add = to_add.replace('0', '1')
        to_add = to_add.replace('2', '0')

      new_hap_line += to_add

    for anc_hap in anc_haps:
      new_hap_line += f'{anc_hap}\t'

    if anc_alleles[0] == anc_alleles[1]:
      vcf_alleles = [anc_alleles[0], '.']
    else:
      vcf_alleles = anc_alleles

    new_vcf_line = f'sim\t{site}\t.\t{vcf_alleles[0]}\t{vcf_alleles[1]}\t200\t.\t.\tGT\t'
    new_vcf_line += f'{new_hap_line.strip()}\n'
    out_lines.append(new_vcf_line)

  with open(out_vcf, 'w') as out:
    out.writelines(out_lines)

if __name__ == '__main__':
  main()
