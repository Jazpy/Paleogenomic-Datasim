import os

def intersection(filenames):
  if len(filenames) < 2:
    return []

  with open(filenames[0], 'r') as f:
    inter = set([x.split()[2] for x in f.readlines()])

  for filename in filenames[1:]:
    with open(filename, 'r') as f:
      curr_list = [x.split()[2] for x in f.readlines()]
      inter = inter.intersection(curr_list)

  return sorted(list(inter))

# Class that describes a haps file
class _SampleHaps:
  def __init__(self, haps_file):
    self.site_dict = {}

    with open(haps_file, 'r') as haps_f:
      for line in haps_f:
        toks = line.split()
        self.site_dict[int(toks[2])] = toks[3:]

  def haps(self, site):
    return self.site_dict.get(site)

def _merge_haps(filenames):
  if len(filenames) < 2:
    return []

  # Begin merging haps file
  inter_sites = intersection(filenames)

  # Reduce first hap file
  with open(filenames[0], 'r') as f:
    inter_haps = [line.strip() for line in f.readlines() if line.split()[2] in inter_sites]

  # Load all other files into memory
  samples = []
  for filename in filenames[1:]:
    samples.append(_SampleHaps(filename))

  # Iterate over all other files
  hap_lines = []
  for hap in inter_haps:
    hap_toks = hap.split()
    hap_site = hap_toks[2]
    hap_alleles = [hap_toks[3], hap_toks[4]]
    added = ''

    for sample in samples:
        # Now we have synced lines
        curr_toks = sample.haps(int(hap_site))

        # Exit if site isn't in intersection
        if not curr_toks:
          added = ''
          break

        # Extract info
        curr_alleles = [curr_toks[0], curr_toks[1]]
        curr_haplo = [curr_toks[2], curr_toks[3]]

        # Determine if ANC is flipped
        if hap_alleles == curr_alleles:
          flip = False
        elif hap_alleles == curr_alleles.reverse():
          flip = True
        # Else, triallelic site, remove from intersection
        else:
          added = ''
          break

        # Append ANC's haplotype to merged hap
        if flip:
          added += f' {curr_haplo[1]} {curr_haplo[0]}'
        else:
          added += f' {curr_haplo[0]} {curr_haplo[1]}'

    if not added:
      continue
    else:
      hap_lines.append(f'{hap}{added}\n')

  return hap_lines

def _merge_map(filenames):
  # Iterate over all files
  map_lines = []
  for i, filename in enumerate(filenames):
    chr_code = f'sim_{i}'
    with open(filename, 'r') as f:
      for line in f:
        toks = line.split()
        map_lines.append(f'{chr_code} . {toks[2]} {toks[3]}\n')

  return map_lines

def _merge_ped(filenames):
  # First, add the first file as-is
  with open(filenames[0], 'r') as f:
    ped_lines = f.readlines()

  # Now iterate over the rest of the files
  for filename in filenames[1:]:
    with open(filename, 'r') as f:
      curr_lines = f.readlines()

    for i, curr_line in enumerate(curr_lines):
      genotype = ' '.join(curr_line.split()[6:])
      curr_ped = ped_lines[i].strip()
      ped_lines[i] = f'{curr_ped} {genotype}\n'

  return ped_lines

def _simple_merge(filenames, outname, merger):
  # Build merged file
  merged_lines = merger(filenames)
  # Write it out
  with open(outname, 'w') as out:
    out.writelines(merged_lines)

def merge_ped(filenames, out_prefix):
  _simple_merge(filenames, f'{out_prefix}.ped', _merge_ped)

def merge_map(filenames, out_prefix):
  _simple_merge(filenames, f'{out_prefix}.map', _merge_map)

def merge_anc_haps(filenames, out_prefix):
  sam_lines = []
  sam_lines.append(f'ID_1 ID_2 missing\n')
  sam_lines.append(f'0 0 0\n')
  for i in range(len(filenames)):
    sam_lines.append(f'ANC{i + 1} ANC{i + 1} 0\n')

  # Write sample file
  with open(f'{out_prefix}.sample', 'w') as out:
    out.writelines(sam_lines)

  # Build haps file
  _simple_merge(filenames, f'{out_prefix}.haps', _merge_haps)

def merge_pre_haps(pre_prefix, anc_filenames, out_prefix):
  # Get started on sample file
  ref_sam = f'{pre_prefix}.sample'

  with open(ref_sam, 'r') as f:
    sam_lines = f.readlines()
  for i in range(len(anc_filenames)):
    sam_lines.append(f'ANC{i + 1} ANC{i + 1} 0\n')

  # Write sample file
  with open(f'{out_prefix}.sample', 'w') as out:
    out.writelines(sam_lines)

  # Build haps file
  all_filenames = [f'{pre_prefix}.haps'] + anc_filenames
  _simple_merge(all_filenames, f'{out_prefix}.haps', _merge_haps)
