from __future__ import print_function
import json
import os
import argparse
import shutil
from tqdm import tqdm
import sys

parser = argparse.ArgumentParser(description="")
parser.add_argument('infile', help="Input file")
parser.add_argument('outfile', help="Output file")
parser.add_argument('--filetype', help="Input file type (annotated/mined)")
args = parser.parse_args()

with open(args.infile, 'r', encoding='utf-8', errors='ignore') as fjson, \
     open(args.outfile, 'w', encoding='utf-8', errors='ignore') as fdump:
  
  if os.path.exists('tmp/'):
    shutil.rmtree('tmp/')
  
  os.mkdir('tmp')
  if args.filetype == 'annotated':
    examples = json.load(fjson)
    for i, example in tqdm(enumerate(examples),file=sys.stdout, desc='Reading {}'.format(args.infile)):
      with open('tmp/tmp-{}.py'.format(i), 'w', encoding='utf-8', errors='ignore') as fout:
        print(example['snippet'], file=fout)
    os.system('2to3 -x map -x zip -w tmp/')
    for i, example in tqdm(enumerate(examples),file=sys.stdout, desc='Writing {}'.format(args.outfile)):
      with open('tmp/tmp-{}.py'.format(i), 'r', encoding='utf-8', errors='ignore') as fin:
        example['snippet'] = ''.join(fin).strip()
    json.dump(examples, fdump, indent=2)
  elif args.filetype == 'mined':
    examples = []
    for i, line in tqdm(enumerate(fjson),file=sys.stdout, desc='Reading {}'.format(args.infile)):
      example = json.loads(line.strip())
      examples.append(example)
      with open('tmp/tmp-{}.py'.format(i), 'w', encoding='utf-8', errors='ignore') as fout:
        print(example['snippet'], file=fout)
    os.system('2to3 -x map -x zip -w tmp/')
    for i, example in tqdm(enumerate(examples),file=sys.stdout, desc='Writing {}'.format(args.outfile)):
      with open('tmp/tmp-{}.py'.format(i), 'r', encoding='utf-8', errors='ignore') as fin:
        example['snippet'] = ''.join(fin).strip()
      print(json.dumps(example), file=fdump)
  else:
    raise ValueError('Bad file type "{}"'.format(args.filetype))

