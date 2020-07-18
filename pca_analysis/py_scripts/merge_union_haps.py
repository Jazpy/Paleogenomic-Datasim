import os
import sys
import bio_utils

def main():
  ref_dir = sys.argv[1]
  ibd_dir = sys.argv[2]
  gen = sys.argv[3]
  cov = sys.argv[4]
  per = sys.argv[5]
  cases = int(sys.argv[6])
  offset = int(sys.argv[7]) * cases

  filenames = []
  for i in range(cases):
    case_index = offset + i + 1
    filename = f'{ibd_dir}/haps/{gen}_{cov}_{per}_{case_index}.haps'

    if os.path.isfile(filename):
      filenames.append(filename)

  # Merge into out dir
  preanc_out_file = f'{ibd_dir}/merged/PREANC_{gen}_{cov}_{per}'
  ref_prefix = f'{ref_dir}/combined'
  bio_utils.merge_pre_haps(ref_prefix, filenames, preanc_out_file)

if __name__ == '__main__':
  main()
