import os
import sys
import bio_utils

def main():
    ref_dir = sys.argv[1]
    ibd_dir = sys.argv[2]
    gen = sys.argv[3]
    cases = int(sys.argv[4])

    filenames = []
    for i in range(cases):
        case_index = i + 1
        filename = f'{ibd_dir}/perfect_haps/{gen}_{case_index}.haps'

        if os.path.isfile(filename):
            filenames.append(filename)

    # Merge into out dir
    preanc_out_file = f'{ibd_dir}/perfect_merged/PREANC_{gen}'
    ref_prefix = f'{ref_dir}/combined'
    bio_utils.merge_pre_haps(ref_prefix, filenames, preanc_out_file)

if __name__ == '__main__':
    main()
