import sys

def main():
  filename = sys.argv[1]

  with open(filename, 'r') as f:
    lines = f.readlines()

  lines.insert(0, '0\n')
  lines[1] = f'{int(int(lines[1]) / 2)}\n'

  with open(filename, 'w') as f:
    f.writelines(lines)

if __name__ == '__main__':
  main()
