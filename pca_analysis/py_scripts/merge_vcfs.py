import sys
import os
import vcf_utils

def main():
  ref_vcf = sys.argv[1]
  out_vcf = sys.argv[2]
  anc_filenames = sys.argv[3:]

  anc_vcfs = []
  for filename in anc_filenames:
    if os.path.isfile(filename):
      anc_vcfs.append(filename)

  # Merge into out dir
  vcf_utils.merge_vcfs(ref_vcf, anc_vcfs, out_vcf)

if __name__ == '__main__':
  main()
