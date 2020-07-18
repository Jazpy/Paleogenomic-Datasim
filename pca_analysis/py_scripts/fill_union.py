import os
import sys

class Sample:
  def __init__(self, chr1_file, chr2_file, haps_file,
               cov_file, out_file):
    with open(chr1_file, 'r') as chr1_f, open(chr2_file, 'r') as chr2_f:
      self.hap1 = chr1_f.readlines()[1]
      self.hap2 = chr2_f.readlines()[1]

    with open(cov_file, 'r') as cov_f:
      self.not_cov = [int(x) for x in cov_f.readlines()]

    self.site_dict = {}

    with open(haps_file, 'r') as haps_f:
      for line in haps_f:
        toks = line.split()
        self.site_dict[int(toks[2])] = toks[3:]

    self.out_file = out_file

  def real_haps(self, site, alleles):
    # Make sure that the site we're about to add
    # was actually covered
    if site in self.not_cov:
      return []

    s1 = self.hap1[site - 1]
    s2 = self.hap2[site - 1]

    if s1 == alleles[0]:
      h1 = 0
    elif s1 == alleles[1]:
      h1 = 1
    else:
      return []

    if s2 == alleles[0]:
      h2 = 0
    elif s2 == alleles[1]:
      h2 = 1
    else:
      return []

    return [h1, h2]

  def add_haps(self, site, alleles):
    # If dict already contains info for this site, do nothing
    if self.site_dict.get(site, None):
      return

    haps = self.real_haps(site, alleles)
    self.site_dict[site] = [alleles[0], alleles[1], haps[0], haps[1]]

  def sites(self):
    return sorted(self.site_dict.keys())

  def haps(self, site):
    return self.site_dict.get(site)

  def write_file(self):
    with open(self.out_file, 'w') as out_f:
      for site in self.sites():
        toks = self.site_dict[site]
        a1 = toks[0]
        a2 = toks[1]
        h1 = toks[2]
        h2 = toks[3]

        out_f.write(f'ref_1 . {site} {a1} {a2} {h1} {h2}\n')

def main():
  pha_dir = sys.argv[1]
  gen = sys.argv[2]
  cov = sys.argv[3]
  per = sys.argv[4]

  cases = 100

  samples = []
  for i in range(cases):
    case_index = i + 1

    haps = f'{pha_dir}/{gen}/cases/case_{case_index}/{cov}/{per}percent/phased/readset.phased.haps'
    not_cov = f'{pha_dir}/{gen}/cases/case_{case_index}/{cov}/{per}percent/not_covered'
    chr1 = f'{pha_dir}/{gen}/cases/case_{case_index}/chr.1.fa'
    chr2 = f'{pha_dir}/{gen}/cases/case_{case_index}/chr.2.fa'

    if not (os.path.isfile(haps) and os.path.getsize(haps) > 0 and
       os.path.isfile(chr1) and os.path.isfile(chr2)):
      continue

    out = f'{pha_dir}/{gen}/cases/case_{case_index}/{cov}/{per}percent/phased/union.phased.haps'

    samples.append(Sample(chr1, chr2, haps, not_cov, out))

  # Union of all sites
  all_sites = set()
  for sample in samples:
    for site in sample.sites():
      all_sites.add(site)

  # Add ref panel sites
  ref_leg = f'{pha_dir}/{gen}/reference/ref_panel.leg'
  with open(ref_leg, 'r') as ref:
    for line in ref:
      if 'position' in line:
        continue
      all_sites.add(int(line.split()[1]))

  all_sites = sorted(all_sites)

  for site in all_sites:
    valid_site = False
    found_site = False
    site_alleles = []

    # Find sample which has data for this site
    for sample in samples:
      curr_haps = sample.haps(site)

      if not curr_haps:
        continue

      curr_alleles = [curr_haps[0], curr_haps[1]]

      if not site_alleles:
        valid_site = True
        found_site = True
        site_alleles = curr_alleles
        continue

      # Else, check for triallelic site
      if curr_alleles != site_alleles and curr_alleles[::-1] != site_alleles:
        valid_site = False
        site_alleles = []
        break

    if not valid_site:
      continue

    # Confirm that it's not triallelic, by comparing to simulated fastas
    for sample in samples:
      curr_haps = sample.real_haps(site, site_alleles)

      if not curr_haps:
        valid_site = False
        site_alleles = []
        break

    # Skip this site, it's triallelic
    if not valid_site:
      print(f'triallelic site 2 {site}')
      continue

    # Finally, add valid site to all samples' site_dict
    for sample in samples:
      sample.add_haps(site, site_alleles)

  # Write all final data
  for sample in samples:
    sample.write_file()

if __name__ == '__main__':
  main()
