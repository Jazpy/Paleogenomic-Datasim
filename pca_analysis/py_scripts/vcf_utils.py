import os

def _get_vcf_lines(filename):
  with open(filename, 'r') as vcf:
    return [x for x in vcf.readlines() if x[0] != '#']

def _intersection(filenames):
  if len(filenames) < 2:
    return []

  curr_lines = _get_vcf_lines(filenames[0])
  inter = set([int(x.split()[1]) for x in curr_lines])

  for filename, i in zip(filenames[1:], range(len(filenames[1:]))):
    print(f'INTERSECT {i}: {len(inter)}')
    curr_lines = _get_vcf_lines(filename)
    curr_list = [int(x.split()[1]) for x in curr_lines]

    if not curr_list:
      continue

    inter = inter.intersection(curr_list)

  return sorted(list(inter))

# Class that describes a vcf file
class _VCF:
  def __init__(self, vcf_lines):
    self.site_dict = {}

    for line in vcf_lines:
      toks = line.split()
      self.site_dict[int(toks[1])] = [[toks[3], toks[4]], toks[9].split(':')[0]]

  def toks(self, site):
    return self.site_dict.get(site)

def _merge_vcfs(filenames):
  if len(filenames) < 2:
    return []

  inter_sites = _intersection(filenames)

  print(len(inter_sites))

  # Reduce first vcf file
  curr_vcf_lines = _get_vcf_lines(filenames[0])
  ref_lines = [line.strip() for line in curr_vcf_lines if int(line.split()[1]) in inter_sites]

  # Load all other files into memory
  all_vcfs = []
  for filename in filenames[1:]:
    all_vcfs.append(_VCF(_get_vcf_lines(filename)))

  # Build VCF header
  out_vcf_lines = ['##fileformat=VCFv4.2\n']
  out_vcf_lines.append('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
  header_line = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT'

  moderns = 500
  ancients = len(all_vcfs)
  for i in range(moderns):
    header_line += f'\tMOD{i + 1}'
  for i in range(ancients):
    header_line += f'\tANC{i + 1}'

  out_vcf_lines.append(header_line + '\n')

  # Iterate over all other files
  for ref_line in ref_lines:
    ref_toks = ref_line.split()
    ref_site = int(ref_toks[1])
    ref_alleles = [ref_toks[3], ref_toks[4]]
    added = ''

    for vcf, i in zip(all_vcfs, range(len(all_vcfs))):
        print(f'Processing ANC {i}')
        # Now we have synced lines
        curr_toks = vcf.toks(int(ref_site))

        # Exit if site isn't in intersection
        if not curr_toks:
          print('None toks')
          added = ''
          break

        # Extract info
        curr_alleles = curr_toks[0]
        curr_gt = curr_toks[1]

        # Ignore triallelic
        if ref_alleles != curr_alleles and ref_alleles != curr_alleles.reverse():
          print('Allele mismatch')
          added = ''
          break

        # Append ANC's genotype to merged vcf
        added += f' {curr_gt}'

    if not added:
      continue
    else:
      out_vcf_lines.append(f'{ref_line}{added}\n')

  return out_vcf_lines

def _simple_merge(filenames, outname, merger):
  # Build merged file
  merged_lines = merger(filenames)
  # Write it out
  with open(outname, 'w') as out:
    out.writelines(merged_lines)

def merge_vcfs(pre_filename, anc_filenames, out_filename):
  all_filenames = [pre_filename] + anc_filenames
  _simple_merge(all_filenames, out_filename, _merge_vcfs)
