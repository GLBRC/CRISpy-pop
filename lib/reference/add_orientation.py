#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser(description='add orientation to gene name for display track')
parser.add_argument('-bed', help='bed file to concatenate orientation and name')
args = parser.parse_args()

with open(args.bed,'r') as bedfile:
	for line in bedfile:
		lineparts = line.split()
		name = ''
		if lineparts[4] == '+':
			name = lineparts[3] + ':Forward_Strand'
		else:
			name = lineparts[3] + ':Reverse_Strand'
		print(lineparts[0],lineparts[1],lineparts[2],name,sep=' ')