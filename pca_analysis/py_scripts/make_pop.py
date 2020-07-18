import os
import sys

def main():
	in_id = sys.argv[1]
	out_pop = sys.argv[2]

	out_str = 'PRE1('
	with open(in_id, 'r') as f:
		for line in f:
			if 'PRE' in line:
				out_str += f'{line.strip()},'

	out_str = out_str[:-1] + ')\n'

	'''
	out_str += 'ANC1('
	with open(in_id, 'r') as f:
		for line in f:
			if 'ANC' in line:
				out_str += f'{line.strip()},'

	out_str = out_str[:-1] + ')'
	'''
	
	with open(out_pop, 'w') as out:
		out.write(out_str)

if __name__ == '__main__':
	main()
