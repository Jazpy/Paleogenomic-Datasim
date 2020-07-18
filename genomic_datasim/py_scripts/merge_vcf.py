import sys

def write(out_vcf, out_lines):
	with open(out_vcf, 'w') as out:
		out.writelines(out_lines)

def main():
	ref_vcf = sys.argv[1]
	anc_vcf = sys.argv[2]
	out_vcf = sys.argv[3]
	anc_id = int(sys.argv[4])

	with open(ref_vcf, 'r') as ref_f, open(anc_vcf, 'r') as anc_f:
		ref_lines = ref_f.readlines()
		anc_lines = anc_f.readlines()

	out_lines = ['##fileformat=VCFv4.2\n']
	out_lines.append('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
	out_lines.append(ref_lines[2].strip() + f'\tANC{anc_id}\n')

	anc_counter = 0
	while '#' in anc_lines[anc_counter]:
		anc_counter += 1
		
		# Empty vcf
		if anc_counter >= len(anc_lines):
			write(out_vcf, ref_lines)
			return

	for line in ref_lines[3:]:
		ref_toks = line.split()
		site = int(ref_toks[1])

		# Advance anc line to match with the current one
		synced = True
		while anc_counter < len(anc_lines) and f'\t{site}\t' not in anc_lines[anc_counter]:
			if site < int(anc_lines[anc_counter].split()[1]):
				synced = False
				break

			anc_counter += 1		

		if anc_counter >= len(anc_lines):
			break

		if not synced:
			continue

		anc_toks = anc_lines[anc_counter].split()
		anc_gt = anc_toks[-1].split(':')[0]

		# Add to ref vcf
		if anc_toks[3] == ref_toks[3] and anc_toks[4] == ref_toks[4]:
			ref_toks.append(anc_gt)
		elif anc_toks[3] == ref_toks[4] and anc_toks[4] == ref_toks[3]:
			if anc_gt == '0/0':
				ref_toks.append('1/1')
			elif anc_gt == '1/1':
				ref_toks.append('0/0')
			else:
				ref_toks.append('0/1')
		elif anc_toks[4] == '.':
			if anc_toks[3] == ref_toks[3]:
				ref_toks.append('0/0')
			elif anc_toks[3] == ref_toks[4]:
				ref_toks.append('1/1')
			else:
				continue
		else:
			continue

		out_lines.append('\t'.join(ref_toks) + '\n')

	write(out_vcf, out_lines)
	
if __name__ == '__main__':
	main()
